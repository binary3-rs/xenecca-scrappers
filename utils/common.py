from datetime import datetime, timezone
from logging import debug, error, info, warning
from os import path, sep
from json import load
from requests import get
from re import split
from config.config import MEDIA_DIR_PATH
from config.constants import COURSE_DATA, LANDING_COMPONENTS

from database.sqlalchemy_extension import db


def download_image(url, image_type="course"):
    if url is None:
        raise ValueError("The url is not valid.")
    if image_type not in ("course", "instructor"):
        raise ValueError("The image target type is not valid.")
    filename = url.split("/")[-1].split("?")[0]
    filepath = path.join(
        MEDIA_DIR_PATH + image_type + "s" + sep + filename
    )
    _download_image(url, filepath)
    return filename


def _download_image(url, destination):
    log(f"Downloading image from the url = {url}...")
    data = get(url, allow_redirects=True)
    with open(destination, "wb") as image_handler:
        image_handler.write(data.content)
    return destination


def create_target_url(target, udemy_id):
    if not udemy_id:
        return None
    if target == "landing":
        return f"{LANDING_COMPONENTS['prefix']}{udemy_id}{LANDING_COMPONENTS['suffix']}"
    if target == "course":
        return f"{COURSE_DATA['prefix']}{udemy_id}{COURSE_DATA['suffix']}"
    return None


# logging utils
def log(text, log_type="info"):
    logger = info
    if log_type == "debug":
        logger = debug
    elif log_type == "warn":
        logger = warning
    elif log_type == "error":
        logger = error
    logger({text})


def log_with_timestamp(text, type="info"):
    log(f"[{datetime.now(timezone.utc)}]: {text}", type)


def load_data_as_map(data, key):
    return {getattr(obj, key): obj for obj in data}


# convert xx:yy:zz in seconds
def convert_duration_from_str_to_int(duration):
    if duration is None or len(duration) == 0:
        return 0
    if ":" not in duration:
        try:
            return int(duration)
        except ValueError:
            return 0
    hours, mins, seconds = 0, 0, 0
    duration_components = duration.split(":")
    seconds = int(duration_components[-1])
    if len(duration_components) == 2:
        mins = int(duration_components[0])
    if len(duration_components) == 3:
        hours, mins = int(duration_components[0]), int(duration_components[1])

    return hours * 3600 + mins * 60 + seconds


def try_save(fn, data, default_value=None, message_subject=""):
    result = default_value
    try:
        result = fn(data)
    except Exception as e:
        log_exception(e, message_subject)
    finally:
        return result


def log_exception(e, message_subject=None):
    if isinstance(e, db.exc.InvalidRequestError) or isinstance(
            e, db.exc.IntegrityError
    ):
        log_with_timestamp(
            f"ERROR: {message_subject} cannot be saved. Data integrity error: {e}.",
            "error",
        )
    elif isinstance(e, db.exc.ProgrammingError):
        log_with_timestamp(
            f"ERROR: {message_subject} cannot be created/updated. Reason: {e}!", "error"
        )
    elif isinstance(e, db.exc.DataError):
        log_with_timestamp(f"ERROR: Invalid data parameters: {e}", "error")
    else:
        log_with_timestamp(f"ERROR: An unpredicted error occurred: {e}!", "error")


def load_data_into_dict(dao, key="name"):
    all_records = dao.find_all()
    return {getattr(item, key): item for item in all_records}


def put_if_not_null(collection, key, value):
    if key is not None and value is not None:
        collection[key] = value


def load_from_json(json_path):
    with open(json_path) as json_file:
        return load(json_file)


def trim_to_len(data, trim_len):
    return f"{data[:trim_len - 3]}..." if (data is not None and len(data) > trim_len) else data


def udemy_url_to_slug(url):
    if url == "#":
        return None
    try:
        url = url.split('course/')[1]
        return f'{split("/?|/", url)[0]}'
    # TODO: check where null slug occurs
    except IndexError as e:
        log_with_timestamp(e)
        return None
