from json import loads
from scrappers.base_scrapper import BaseScrapper
from utils.utils_functions import create_target_url, convert_duration_from_str_to_int


class UdemyScrapper(BaseScrapper):
    def __init__(self):
        super().__init__()

    def find_course_details(self, udemy_id):
        landing_data = self._fetch_udemy_data(udemy_id, "landing")
        course_data = self._fetch_udemy_data(udemy_id, "course")
        # variables needed here
        price_details = {}
        incentives = {}
        instructors = []
        headline_data = {}
        curriculum = []
        discount_expiration = {}
        ratings = {}
        # if not landing_data or not course_data:
        #     return {}
        if 'price_text' in landing_data:
            price_details = self.find_course_price_details(landing_data['price_text'].get('data'))
        if 'incentives' in landing_data:
            incentives = self.find_course_incentives(landing_data['incentives'])
        if 'instructor_bio' in landing_data:
            instructors = self.find_course_instructors(landing_data['instructor_bio'].get('data'))
        if "slider_menu" in landing_data:
            headline_data = self.find_course_headline_data(landing_data['slider_menu'].get('data'))
        if "curriculum" in landing_data:
            curriculum = self.find_course_curriculum(landing_data['curriculum'].get('data'))
        if "discount_expiration" in landing_data:
            discount_expiration = self.find_course_discount_expiration(landing_data['discount_expiration'].get('data'))
        if "reviews" in landing_data:
            ratings = self.find_course_ratings(landing_data['reviews'].get('display_app_args'))
        basic_info = self.find_course_basic_info(course_data)
        return {
            "headline_data": {**headline_data, **discount_expiration},
            "basic_data": basic_info,
            "instructors": instructors,
            "incentives": incentives,
            "price_details": price_details,
            "curriculum": curriculum,
            "ratings": ratings
        }

    # price details
    def find_course_price_details(self, data):
        if data is None:
            return {}
        pricing_result = data.get("pricing_result")
        if pricing_result:
            list_price = pricing_result.get("list_price")
            if list_price:
                return {"discount_code": pricing_result.get("code"),
                        "price": pricing_result.get("price", {}).get("amount", 0),
                        "old_price": list_price.get("amount", 0),
                        "currency": pricing_result.get("price", {}).get("currency_symbol", '$'),
                        #"price_as_string": list_price.get("price_string"),
                        "discount_percent": pricing_result.get("discount_percent_for_display", 0)
                        }
        return {}

    def find_course_incentives(self, data):
        if data is None:
            return {}
        fields = ("video_content_length", "has_assignments", "devices_access", "has_certificate",
                  "has_lifetime_access", "num_articles", "num_additional_resources", "num_practice_tests",
                  "num_coding_exercises")
        return {key: data.get(key) for key in fields}

    def find_course_instructors(self, data):
        if data is None:
            return []
        instructors_data = data.get("instructors_info")
        instructors = []
        for instructor in instructors_data:
            instructor_details = {"full_name": instructor.get("display_name"),
                                  "job_title": instructor.get("job_title"),
                                  "udemy_id": instructor.get("id"),
                                  "description": instructor.get("description") if len(instructor.get("description"))
                                  else None,
                                  "num_of_courses": instructor.get("total_num_taught_courses", 0),
                                  "num_of_students": instructor.get("total_num_students", 0),
                                  "avg_rating": round(instructor.get("avg_rating_recent", 0.0), 2),
                                  "original_image_url": instructor.get("image_75x75"),
                                  "image_path": None
                                  }
            instructors.append(instructor_details)
        return instructors

    def find_course_headline_data(self, data):
        if data is None:
            return {}
        return {
            "title": data.get("title"),
            "avg_rating": data.get("rating", 0.0),
            "badge": data.get("badge_family"),  # new, top_rated
            "num_reviews": data.get("num_reviews", 0),
            "num_students": data.get("num_students", 0)
        }

    def find_course_basic_info(self, data):
        if data is None:
            return {}
        primary_category = data.get("primary_category", {}).get("title") # TODO: maybe to add title cleaned
        primary_subcategory = data.get("primary_subcategory", {}).get("title")
        language = data.get("locale", {}).get("simple_english_title")
        topic = data.get("context_info", {}).get("label", {})
        if topic is not None:
            topic = topic.get("display_name")
        return {"category": primary_category, "subcategory": primary_subcategory, "language": language, "topic": topic}

    def find_course_curriculum(self, data):
        if data is None:
            return []
        sections = data.get("displayed_sections", [])
        lectures = []
        counter = 1
        for section in sections:
            items = section.get("items", [])
            lectures.append({
                "title": section.get("title"),
                "item_type": "section",
                "description": None,
                "index": counter,
                "section_index": 0,
                "udemy_lesson_id": None,
                "content_length": convert_duration_from_str_to_int(section.get("content_length_text")),
            })

            for item in items:
                lectures.append({
                    "title": item.get("title"),
                    "item_type": item.get("item_type"),
                    "description": item.get("description"),
                    "index": item.get("object_index", 0),
                    "section_index": counter,
                    "udemy_lesson_id": item.get("id", 0),
                    "content_length": convert_duration_from_str_to_int(item.get("content_summary")),
                })
            counter += 1
        return lectures

    def find_course_discount_expiration(self, data):
        if data is None:
            return {}
        return {"discount_period": data.get("discount_deadline_text")}

    def find_course_ratings(self, data):
        if data is None:
            return {}
        ratings = data.get("ratingDistribution", {})
        return {rating['rating']: rating['count'] for rating in ratings}

    def find_udemy_course_id_and_headline(self, content):
        """
        Finds id of the udemy course
        :param content: HTML content of the page we're scrapping
        :return: string id or None
        """
        results = super()._find_content_on_page(content, 'body')
        body_element = results[0] if len(results) else None
        udemy_id = body_element.attrs['data-clp-course-id'] if body_element else None
        headline_el = super()._find_content_on_page(content, 'div', 'udlite-text-md clp-lead__headline')
        headline = headline_el[0].text if len(headline_el) > 0 else ''
        return udemy_id, headline

    # API calls
    def _fetch_udemy_data(self, course_id, target):
        target_url = create_target_url(target, course_id)
        data = self._fetch_data_from_the_api(target_url)
        return {} if data is None else loads(data)


'''
components
slider menu
'''

'''
Recommendation
https://www.udemy.com/api-2.0/discovery-units/?context=landing-page&from=0&page_size=6&item_count=18&course_id=3826872&source_page=course_landing_page&locale=en_US&currency=usd&navigation_locale=en_US&skip_price=true
'''

'''
Price
https://www.udemy.com/api-2.0/course-landing-components/3826872/me/?components=price_text,deal_badge,discount_expiration,redeem_coupon,gift_this_course,base_purchase_section,purchase_tabs_context,subscribe_team_modal_context
'''
'''
https://www.udemy.com/api-2.0/course-landing-components/3826872/me/?components=practice_test_bundle,recommendation,instructor_bio,incentives,featured_qa,caching_intent
'''

'''
https://www.udemy.com/api-2.0/courses/3826872/reviews/?courseId=3826872&page=1&is_text_review=1&ordering=course_review_score__rank,-created&fields[course_review]=@default,response,content_html,created_formatted_with_time_since&fields[user]=@min,image_50x50,initials&fields[course_review_response]=@min,user,content_html,created_formatted_with_time_since
'''
'''
https://www.udemy.com/api-2.0/discovery-units/?context=landing-page&from=0&page_size=6&item_count=18&course_id=3826872&source_page=course_landing_page&locale=en_US&currency=usd&navigation_locale=en_US&skip_price=true
'''
'''
https://www.udemy.com/api-2.0/courses/3826872/reviews/?courseId=3826872&page=1&is_text_review=1&ordering=course_review_score__rank,-created&fields[course_review]=@default,response,content_html,created_formatted_with_time_since&fields[user]=@min,image_50x50,initials&fields[course_review_response]=@min,user,content_html,created_formatted_with_time_since
'''
'''
https://www.udemy.com/api-2.0/course-landing-components/3826872/me/?components=slider_menu
'''

'''
https://www.udemy.com/api-2.0/course-landing-components/3826872/me/?components=curriculum,price_text,reviews,incentives,instructor_bio,discount_expiration,slider_menu
'''
'''
I ne mora
https://www.udemy.com/api-2.0/courses/3826872/reviews/?courseId=3826872&page=1&is_text_review=1&ordering=course_review_score__rank,-created&fields[course_review]=@default,response,content_html,created_formatted_with_time_since&fields[user]=@min,image_50x50,initials&fields[course_review_response]=@min,user,content_html,created_formatted_with_time_since
'''

'''
https://www.udemy.com/api-2.0/courses/3826872/?fields[course]=context_info,primary_category,primary_subcategory,avg_rating_recent,visible_instructors,locale,estimated_content_length,num_subscribers,courseId=3826872&page=1&is_text_review=1&ordering=course_review_score__rank,-created&fields[course_review]=@default,response,content_html,created_formatted_with_time_since&fields[user]=@min,image_50x50,initials&fields[course_review_response]=@min,user,content_html,created_formatted_with_time_since
'''
