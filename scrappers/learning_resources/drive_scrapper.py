import io
from sys import stdout

import apiclient
import googleapiclient
import httplib2
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from constants.constants import SCOPES, CREDENTIALS_PICKLE_FILEPATH
from dao.learning_resource import LearningResourceDAO
from dao.learning_resource_category_dao import LearningResourceCategoryDAO
from database.models.learning_resource import MaterialType, ResourceType
from database.sqlalchemy_extension import db
from utils.common import log_exception
from utils.credentials import obtain_credentials, refresh_token_if_expired
from utils.file import *
from utils.learning_resource_categorizer import (
    determine_category_name_by_filename,
    determine_resource_name_by_filename,
)
from utils.search import store_obj_in_es_index

GOOGLE_DRIVE_CREDENTIALS_PATH = "scrappers/learning_resources/creds.json"


def _get_file_props(file):
    file_id = file["id"]
    filename = file["name"]
    mime_type = file["mimeType"]
    shortcut_details = file.get("shortcutDetails", None)
    if shortcut_details is not None:
        file_id = shortcut_details["targetId"]
    return file_id, filename, mime_type, shortcut_details


def _download(downloader, filestream, filepath):
    done = False
    while done is False:
        try:
            status, done = downloader.next_chunk()
        except (googleapiclient.errors.HttpError, httplib2.HttpLib2Error) as e:
            filestream.close()
            remove(filepath)
            print(
                f"An error occurred during the download of the file [{filepath}. Error message: {e}"
            )
            break
        print(f"\rDownload {int(status.progress() * 100)}%.", end="")
        stdout.flush()
    print()
    return done


def _load(dao):
    data = set()
    for obj in dao.find_all():
        data.add(obj.name)
    return data


def _load_categories(dao):
    data = {}
    for obj in dao.find_all():
        data[obj.name] = obj
    return data


class DriveScrapper:
    def __init__(self):
        self._credentials = self._get_credentials()
        self._service = self._get_service()
        self._urls_file = None

        self._resource_dao = LearningResourceDAO()
        self._resource_category_dao = LearningResourceCategoryDAO()

        self._resources = _load(self._resource_dao)
        self._categories = _load_categories(self._resource_category_dao)

    @property
    def credentials(self):
        return self._credentials

    @property
    def service(self):
        return self._service

    def _get_credentials(self):
        if filepath_exists(CREDENTIALS_PICKLE_FILEPATH):
            token = get_pickle_file(CREDENTIALS_PICKLE_FILEPATH)
            credentials = load_pickle(token)
            token.close()
            refresh_token_if_expired(credentials)
        else:
            credentials = obtain_credentials(GOOGLE_DRIVE_CREDENTIALS_PATH, SCOPES)
            dump_pickle(CREDENTIALS_PICKLE_FILEPATH, credentials)
        return credentials

    def _get_service(self):
        if self._credentials is not None:
            return build("drive", "v3", credentials=self._credentials)
        raise ValueError(
            "Google Drive service cannot be created! Credentials are not set or valid!"
        )

    def scrape(self, dir_id, location, dir_name):
        dir_content = self._get_dir_content(dir_id)
        for file in dir_content:
            file_id, filename, mime_type, shortcut_details = _get_file_props(file)
            if mime_type == "application/vnd.google-apps.folder":
                self._scrape_resources_dir(file_id, location, dir_name)
            elif filename == "urls.txt":
                self._urls_file = file
                self._scrape_urls_file(file_id, location, filename, mime_type)

    def _scrape_resources_dir(self, dir_id, location, dir_name):
        create_dir_if_not_exists(location + dir_name)
        location = location + dir_name + "/"
        dir_content = self._get_dir_content(dir_id)
        scraped, total = 0, 0
        print(f"Downloading directory with the id = {dir_id} to location {location}...")
        for item in dir_content:
            file_id, filename, mime_type, shortcut_details = _get_file_props(item)
            file_path = location + filename
            if mime_type == "application/vnd.google-apps.folder":
                self._scrape_resources_dir(file_id, location, filename)
            elif (
                    mime_type != "application/vnd.google-apps.folder"
                    and file_path not in self._resources
            ):
                total = total + 1
                try:
                    data = self._parse_file_name(file_path)
                except ValueError as e:
                    log_exception(e, "LearningResource")
                    continue
                status = self._download_file(file_id, location, filename, mime_type)
                if status:
                    resource = self._try_save_resource(data)
                    scraped = scraped + 1
                    if resource is not None:
                        self._delete_file(file_id)
                        store_obj_in_es_index(resource)
                    print(
                        f"{file_id} {filename} {mime_type} ({scraped}/{total})"
                    )

    def _scrape_urls_file(self, file_id, location, filename, mime_type):
        unsaved_lines = []
        status = self._download_file(file_id, location, filename, mime_type)
        if not status:
            log("File with urls couldn't have been downloaded!")
        else:
            file_content = read_file(location + filename)
            for line in file_content:
                try:
                    data = self._parse_file_line(line)
                    resource = self._create_learning_resource(data)
                    if resource is not None:
                        store_obj_in_es_index(resource)
                    else:
                        unsaved_lines.append(line)
                except ValueError as e:
                    unsaved_lines.append(line)
                    log_exception(e, "LearningResource")
                    continue
            if len(unsaved_lines) > 0 and self._urls_file is not None:
                self._update_urls_file(unsaved_lines, location, filename, file_id)

    def _update_urls_file(self, resources, location, filename, file_id):
        create_dir_if_not_exists(location + "tmp/")
        new_file_name = location + "tmp/" + filename
        write_to_file(new_file_name, resources)
        try:
            media_body = MediaFileUpload(
                new_file_name, mimetype="text/plain", resumable=True
            )
            self.service.files().update(fileId=file_id, media_body=media_body).execute()
        except apiclient.errors.HttpError as e:
            log_exception(e, "Update urls file")

    def _create_learning_resource(self, data, filepath=None, parse_type="text_line"):
        resource = self._try_save_resource(data)
        if resource is not None:
            log(
                f"LearningResource with name = {data['name']} and value = {data['resource']} successfully created."
            )

        elif parse_type == "file":
            remove(filepath)
        return resource

    def _parse_file_line(self, line):
        params = line[:-1].split("--!!--")
        if len(params) < 4:
            raise ValueError(
                "Wrong resource parameters format. Some params are missing!"
            )
        category = self._categories.get(params[2])
        if category is None:
            raise ValueError(
                f"There is no resource category with such a name({params[2]})"
            )
        return {
            "name": params[0],
            "resource": params[1],
            "resource_category": category,
            "resource_type": ResourceType.str_to_enum(params[3]),
            "material_type": MaterialType.URL,
        }

    def _parse_file_name(self, filepath):
        params = filepath.split("/")
        if len(params) < 3:
            raise ValueError(
                "Wrong resource parameters format. Some params are missing!"
            )
        (
            resource_type,
            pattern,
            filename,
        ) = params[-3:]
        name = determine_resource_name_by_filename(filename, pattern)
        resource_type = resource_type.lower()
        if resource_type[-1] == "s":
            resource_type = resource_type[:-1]
        category = determine_category_name_by_filename(name, self._categories)
        if category is None:
            raise ValueError("There is no resource category with such a name")
        return {
            "name": name,
            "resource": filepath,
            "resource_category": category,
            "resource_type": ResourceType.str_to_enum(resource_type),
            "material_type": MaterialType.FILE,
        }

    def _delete_file(self, file_id):
        try:
            self._service.files().delete(fileId=file_id).execute()
            print(
                f"File with the id = {file_id} successfully removed from the Google Drive."
            )
        except googleapiclient.errors.HttpError as e:
            log_exception(e, "Google drive delete execution")

    def _try_save_resource(self, resource):
        resource_obj = None
        try:
            resource_obj = self._resource_dao.create(**resource)
        except (
                db.exc.InvalidRequestError,
                db.exc.IntegrityError,
                db.exc.ProgrammingError,
                db.exc.DataError,
        ) as e:
            log_exception(e, "Learning resource")
        finally:
            return resource_obj

    def _get_dir_content(self, dir_id):
        result = []
        page_token = None
        while True:
            files = (
                self._service.files()
                    .list(
                    q=f"'{dir_id}' in parents",
                    fields="nextPageToken, files(id, name, mimeType, shortcutDetails)",
                    pageToken=page_token,
                    pageSize=1000,
                )
                    .execute()
            )
            result.extend(files["files"])
            page_token = files.get("nextPageToken")
            if not page_token:
                break
        return result

    def _download_file(self, file_id, location, filename, mime_type):
        request, filename = self._create_download_request(file_id, filename, mime_type)
        fs = io.FileIO(location + filename, "wb")
        downloader = MediaIoBaseDownload(fs, request, 1024 * 1024 * 1024)
        return _download(downloader, fs, location + filename)

    def _create_download_request(self, file_id, filename, mime_type):
        if "vnd.google-apps" in mime_type:
            request = self._service.files().export_media(
                fileId=file_id, mimeType="application/pdf"
            )
            filename += ".pdf"
        else:
            request = self._service.files().get_media(fileId=file_id)
        return request, filename


ds = DriveScrapper()
ds.scrape("16w4J1PZSa_qm-lajv2hBOnEaztEa2vwN", "test/", "testio")
# ds._scrape_urls_file(
#     "1bGDKYPdtBVJz9uAjJ02JEX-NgA7f3_oN", "test/testio/", "urls.txt", "text/plain"
# )
