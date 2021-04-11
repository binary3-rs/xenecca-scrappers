from os import getenv

COMMON_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/81.0.4044.138 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/png,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9 '
}

LEARN_VIRAL = {
    'name': 'learn_viral',
    'url': 'https://udemycoupon.learnviral.com/coupon-category/free100-discount/page/',
    'headers': {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/81.0.4044.138 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/png,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
    },
    'patterns': ['div', {"class": 'content-box'}],
    'need_original_content': False
}

REAL_DISCOUNT = {
    'name': 'real_discount',
    'url': 'https://www.real.discount/new/page/',
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/81.0.4044.138 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9 '
    },
    'pattern': ['div', {'style': 'margin-top:-274px;z-index:9;position: absolute; left: 0; margin-left: 15px; color: '
                                 '#fff; background: rgba(0,0,0,0.5); padding: 2px 4px; font-weight: 700;'}],
    'need_original_content': True
}

UDEMY_FREEBIES = {
    'name': 'udemy_freebies',
    'url': 'https://www.udemyfreebies.com/free-udemy-courses/',
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/81.0.4044.138 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9 '
    },
    'pattern_1st_level': ('div', {'class': 'theme-block'}),
    'pattern_2nd_level': ('div', {'class': 'theme-block'}),
    'url_scrapper': 'common',
    'details_scrapper': None,
    'need_original_content': False
}

UDEMY_COUPONS_ME = {
    'name': 'udemy_coupons_me',
    'url': 'https://udemycoupons.me/page/',
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/81.0.4044.138 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9 '
    },
    'pattern': ['div', {'class': 'td_module_1 td_module_wrap td-animation-stack'}],
    'need_original_content': False
}

DISCUDEMY = {
    'name': 'discudemy',
    'url': 'https://www.discudemy.com/all/',
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/81.0.4044.138 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9 '
    },
    'pattern': ['section', {'class': 'card'}],
    'need_original_content': False
}

TRICKS_INFO = {
    'name': 'tricks_info',
    'url': 'https://tricksinfo.net/page/',
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/81.0.4044.138 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9 '
    },
    'pattern': ['a', {'class': 'post-thumb'}],
    'need_original_content': False
}

FREE_WEBCART = {
    'name': 'free_webcart',
    'url': 'https://www.freewebcart.com/udemy/',
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/81.0.4044.138 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9 '
    },
    'pattern': ['h2', {'class': 'title'}],
    'need_original_content': False
}

JOJO_COUPONS = {
    'name': 'jojo_coupons',
    'url': 'https://jojocoupons.com/category/udemy/page/',
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/81.0.4044.138 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9 '
    },
    'pattern': ['h2', {'class': 'font130 mt0 mb10 mobfont110 lineheight20'}],
    'need_original_content': False
}

FREE_WEBCART_PATTERN = {'element': 'div',
                        'attrs': {'class': 'stm_lms_courses__single--title'}}  # stm_lms_courses__single__inner'}}

ONLINE_TUTORIALS = {
    'name': 'online_tutorials',
    'url': 'https://udemycoupon.onlinetutorials.org/page/',
    'headers': COMMON_HEADERS,
    'pattern_1st_level': ('h3', {'class': 'entry-title'}),
    'pattern_2nd_level': ('h3', {'class': 'entry-title'}),
    'url_scrapper': 'common',
    'details_scrapper': None,
    'need_original_content': False
}

SMARTY_BRO = {
    'name': 'smarty_bro',
    'url': 'https://smartybro.com/page/',
    'headers': COMMON_HEADERS,
    'pattern_1st_level': ['h2', {'class': 'grid-tit'}],
    'pattern_2nd_level': ('h3', {'class': 'entry-title'}),
    'url_scrapper': None,
    'details_scrapper': None,
    'need_original_content': False
}

# COURSEMANIA = 'https://api.coursemania.xyz/api/get_courses'  # api
# HELPCOV = 'https://asia-east2-myhelpcovid19.cloudfunctions.net/app/courses?pagesize=50&source=udemy'  # api
# JOJOCP = 'https://jojocoupons.com/category/udemy/page/'
# ONLINETUT = 'https://udemycoupon.onlinetutorials.org/page/'
# CHECKOUT = 'https://www.udemy.com/payment/checkout-submit/'
# FREE_ENROLL = 'https://www.udemy.com/api-2.0/users/me/subscribed-courses/?fields%5Buser%5D=title%2Cimage_100x100' \
#               '&fields%5Bcourse%5D=title%2Cheadline%2Curl%2Ccompletion_ratio%2Cnum_published_lectures' \
#               '%2Cimage_480x270%2Cimage_240x135%2Cfavorite_time%2Carchive_time%2Cis_banned%2Cis_taking_disabled' \
#               '%2Cfeatures%2Cvisible_instructors%2Clast_accessed_time%2Csort_order%2Cis_user_subscribed' \
#               '%2Cis_wishlisted '
# #SMARTY_BRO = 'https://smartybro.com/category/web-development/page/'

NUM_OF_CONSEC_EMPTY_PAGES_THRESHOLD = 3

# URLs
BASIC_COURSE_DETAILS_URL = {"prefix": "https://www.udemy.com/api-2.0/courses/",
                            "suffix": "/?fields[course]=primary_category,"
                                      "primary_subcategory,avg_rating_recent,visible_instructors, locale,"
                                      "estimated_content_length,"
                                      "num_subscribers "}

# deal_badge, discount_expiration, gift_this_course, price_text, purchase, redeem_coupon, cacheable_deal_badge, cacheable_discount_expiration, cacheable_price_text, cacheable_buy_button, buy_button, buy_for_team, cacheable_purchase_text, cacheable_add_to_cart, money_back_guarantee, instructor_links, top_companies_notice_context, curated_for_ufb_notice, sidebar_container, purchase_tabs_context, subscribe_team_modal_context
COURSE_INCENTIVES_AND_PRICE = {"prefix": "https://www.udemy.com/api-2.0/course-landing-components/",
                               "suffix": "/me/?components=deal_badge,discount_expiration,gift_this_course,price_text,purchase,redeem_coupon,cacheable_deal_badge,cacheable_discount_expiration,cacheable_price_text,cacheable_buy_button,buy_button,buy_for_team,cacheable_purchase_text,cacheable_add_to_cart,money_back_guarantee,instructor_links,top_companies_notice_context,curated_for_ufb_notice,sidebar_container"}

SMARTY_BRO_BASE_URL = 'https://smartybro.com/page/'

LANDING_COMPONENTS = {"prefix": "https://www.udemy.com/api-2.0/course-landing-components/",
                      "suffix": "/me/?components=curriculum,price_text,reviews,incentives,instructor_bio,"
                                "discount_expiration,slider_menu"}

COURSE_DATA = {"prefix": "https://www.udemy.com/api-2.0/courses/",
               "suffix": "?fields[course]=primary_category,primary_subcategory,context_info,locale"}

# elastic search data

ES_PORT = getenv('ES_PORT', 9200)
ES_COURSES_INDEX = getenv('ES_COURSES_INDEX', 'xenecca-course')
COURSES_ES_ENDPOINT = f'http://localhost:{ES_PORT}/{ES_COURSES_INDEX}/_doc/'


# length constants
CURRICULUM_ITEM_DESCRIPTION_LEN = 500
COURSE_DESCRIPTION_LEN = 6000
COURSE_GOALS_LEN = 1000
COURSE_REQUIREMENTS_LEN=1000