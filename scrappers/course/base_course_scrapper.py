from scrappers.base_scrapper import get_page_content


class BaseCourseScrapper:
    HOST_BASE_URL = None

    @classmethod
    def find_basic_courses_details(cls, args):
        courses = {}
        for arg in args:
            url = f"{cls.HOST_BASE_URL}{arg}/"
            page_content = get_page_content(url)
            courses.update(cls.find_host_urls_in_page_content(page_content))
        return courses

    # TODO: check if this could be thrown away - just find_course_details instead
    @classmethod
    def find_all_course_details(cls, url):
        return cls._find_course_details(url)

    @classmethod
    def _find_course_details(cls, url):
        pass

    @classmethod
    def _find_course_headline(cls, content):
        pass

    @classmethod
    def _find_course_udemy_url(cls, content):
        pass

    @classmethod
    def _find_course_category_and_subcategory(cls, content):
        pass

    @classmethod
    def _find_course_description(cls, content):
        pass

    @classmethod
    def _find_course_objectives(cls, content):
        pass

    @classmethod
    def _find_course_poster(cls, content):
        pass

    @classmethod
    def _find_course_language(cls, content):
        pass
