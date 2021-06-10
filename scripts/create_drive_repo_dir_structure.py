from scrappers.learning_resources.drive_scrapper import DriveScrapper

ds = DriveScrapper()

BASE_PATH = "resources/"
file_metadata = {
    "name": None,
    "parents": ["1dqtqcHMYsbEAiZ6_Zb1vJSNsSihZMc_S"],
    "mimeType": "application/vnd.google-apps.folder",
}
if __name__ == "__main__":
    for dir_name in (
        "cheatsheets",
        "books",
        "scripts",
        "images",
        #"projects"
        #"blogs_articles",
        #"tutorials",
        #"websites",
        #"podcasts",
        #"collections",
    ):
        file_metadata["name"] = dir_name
        file_metadata["parents"] = ["1dqtqcHMYsbEAiZ6_Zb1vJSNsSihZMc_S"]
        created_dir = ds.service.files().create(body=file_metadata, fields="id").execute()
        file_metadata["parents"] = [created_dir.get('id')]
        for dir_pattern in ("_", "-", "AAA", "OK"):
            file_metadata["name"] = dir_pattern
            ds.service.files().create(body=file_metadata, fields="id").execute()
