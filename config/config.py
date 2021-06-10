from os import getenv

from dotenv import load_dotenv
load_dotenv()
# elastic search data

ES_PORT = getenv("ES_PORT", 9200)
ES_COURSES_INDEX = getenv("ES_COURSES_INDEX", "xenecca-course")
COURSES_ES_ENDPOINT = f"http://localhost:{ES_PORT}/{ES_COURSES_INDEX}/_doc/"

ES_RESOURCES_INDEX = getenv("ES_RESOURSES_INDEX", "xenecca-learning-resource")
LEARNING_RESOURCES_ES_ENDPOINT = f"http://localhost:{ES_PORT}/{ES_RESOURCES_INDEX}/_doc/"

GOOGLE_DISK_DIR_ID = getenv("GOOGLE_DISK_DIR_ID")

MEDIA_DIR_PATH = getenv("MEDIA_DIR_PATH", "/var/www/xenecca.com/public_html/media/")
RESOURCES_LOCATION = getenv("RESOURCES_LOCATION","~/xenecca/learning-resources/")

