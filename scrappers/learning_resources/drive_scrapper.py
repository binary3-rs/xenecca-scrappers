import io
from os import remove
from sys import stdout

import googleapiclient
import httplib2
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from database.sqlalchemy_extension import db
from utils.common import log_exception
from utils.credentials import obtain_credentials, refresh_token_if_expired
from utils.file import *

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
GOOGLE_DRIVE_CREDENTIALS_PATH = "scrappers/learning_resources/creds.json"
CREDENTIALS_PICKLE_FILEPATH = "token.pickle"


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


class DriveScrapper:
    def __init__(self):
        self._credentials = self._get_credentials()
        self._service = self._get_service()
        self._resources = set()
        self._resource_dao = None

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

    def download_dir(self, dir_id, location, dir_name):
        create_dir(location + dir_name)
        location = location + dir_name + "/"
        dir_content = self._get_dir_content(dir_id)
        total = len(dir_content)
        print(
            f"Downloading directory `{dir_name}` with the id = {dir_id} to location {location}..."
        )
        for index, item in enumerate(dir_content):
            file_id, filename, mime_type, shortcut_details = _get_file_props(item)
            filepath = location + filename
            if not filepath_exists(filepath) and filepath not in self._resources:
                status, filetype = self._download_resource(item, location)
                if status:
                    print(f"{file_id} {filename} {mime_type} ({index + 1}/{total})")
                    if filetype == "file":
                        self._try_save_resource(filepath)
        return True

    def _download_resource(self, resource, location):
        file_id, filename, mime_type, shortcut_details = _get_file_props(resource)
        if mime_type == "application/vnd.google-apps.folder":
            status = self.download_dir(file_id, location, filename)
            return status, "directory"
        else:
            status = self._download_file(file_id, location, filename, mime_type)
            return status, "file"

    def _try_save_resource(self, filepath):
        try:
            self._save_resource_to_db(filepath)
        except (
            db.exc.InvalidRequestError,
            db.exc.IntegrityError,
            db.exc.ProgrammingError,
            db.exc.DataError,
        ) as e:
            log_exception(e, "Learning resource")
            remove(filepath)

    def _save_resource_to_db(self, filepath):
        pass

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
ds.download_dir("16w4J1PZSa_qm-lajv2hBOnEaztEa2vwN", "test", "testio")
