class Builder:
    def __init__(self):
        self.__full_name = None
        self.__job_title = None
        self.__original_image_url = None
        self.__image_path = None
        # self.instructor = Instructor()

    def full_name(self, full_name):
        self.__full_name = full_name
        return self

    def job_title(self, job_title):
        self.__job_title = job_title
        return self

    def original_image_url(self, original_image_url):
        self.__original_image_url = original_image_url
        return self

    def image_path(self, image_path):
        self.__image_path = image_path
        return self

    def build(self):
        return Instructor(self.__full_name, self.__job_title, self.__original_image_url, self.__image_path)


class Instructor:
    builder = Builder()

    def __init__(self, full_name=None, job_title=None, original_image_url=None, image_path=None):
        self.__full_name = full_name
        self.__job_title = job_title
        self.__original_image_url = original_image_url
        self.__image_path = image_path

    @staticmethod
    def create(**kwargs):
        instructor = Instructor.builder.full_name(kwargs.get('display_name')).job_title(kwargs.get('job_title'))\
            .original_image_url(kwargs.get('image_50x50')).image_path(None).build()
        return instructor

    @property
    def full_name(self):
        return self.__full_name

    @full_name.setter
    def full_name(self, full_name):
        self.__full_name = full_name

    @property
    def job_title(self):
        return self.__job_title

    @job_title.setter
    def job_title(self, job_title):
        self.__job_title = job_title

    @property
    def original_image_url(self):
        return self.__original_image_url

    @original_image_url.setter
    def original_image_url(self, original_image_url):
        self.__original_image_url = original_image_url

    @property
    def image_path(self):
        return self.__image_path

    @image_path.setter
    def image_path(self, image_path):
        self.__image_path = image_path

    def __str__(self):
        return f"[full_name = {self.full_name}, job_title = {self.job_title}, image_url = {self.original_image_url}," \
               f" image_path = {self.image_path}]"
