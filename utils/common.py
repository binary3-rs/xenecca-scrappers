from datetime import datetime, timezone
from logging import debug, error, info, warning
from os import path, sep
from json import load
from requests import get

from constants.config import COURSES_MEDIA_DIR_PATH
from constants.constants import COURSE_DATA, LANDING_COMPONENTS
from database.sqlalchemy_extension import db

LOCAL_FILE_PATH = path.dirname(path.realpath("__file__"))


def download_image(url, type="poster"):
    if url is None:
        raise ValueError("The url is not valid.")
    if type not in ("poster", "instructor"):
        raise ValueError("The image target type is not valid.")
    filename = url.split("/")[-1].split("?")[0]
    filepath = path.join(
        LOCAL_FILE_PATH, COURSES_MEDIA_DIR_PATH + type + "s" + sep + filename
    )
    return _download_image(url, filepath)


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
def log(text, type="info"):
    log = info
    if type == "debug":
        log = debug
    elif type == "warn":
        log = warning
    elif type == "error":
        log = error
    log({text})


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
        raise e
        log_with_timestamp(f"ERROR: An unpredicted error occurred: {e}!", "error")


def load_data_into_dict(dao, key="name"):
    all_records = dao.find_all()
    return {getattr(item, key): item for item in all_records}


def put_if_not_null(collection, key, value):
    if key is not None:
        collection[key] = value


def load_from_json(json_path):
    with open(json_path) as json_file:
        return load(json_file)

