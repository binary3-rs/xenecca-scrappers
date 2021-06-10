

COMMON_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/81.0.4044.138 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/png,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9 ",
}

# URLs
BASIC_COURSE_DETAILS_URL = {
    "prefix": "https://www.udemy.com/api-2.0/courses/",
    "suffix": "/?fields[course]=primary_category,"
              "primary_subcategory,avg_rating_recent,visible_instructors, locale,"
              "estimated_content_length,"
              "num_subscribers ",
}

COURSE_INCENTIVES_AND_PRICE = {
    "prefix": "https://www.udemy.com/api-2.0/course-landing-components/",
    "suffix": "/me/?components=deal_badge,discount_expiration,gift_this_course,price_text,purchase,redeem_coupon,"
              "cacheable_deal_badge,cacheable_discount_expiration,cacheable_price_text,cacheable_buy_button,"
              "buy_button,buy_for_team,cacheable_purchase_text,cacheable_add_to_cart,money_back_guarantee,"
              "instructor_links,top_companies_notice_context,curated_for_ufb_notice,sidebar_container",
}

SMARTY_BRO_BASE_URL = "https://smartybro.com/page/"
FREEWEB_CART_BASE_URL = "https://www.freewebcart.com/course/"

LANDING_COMPONENTS = {
    "prefix": "https://www.udemy.com/api-2.0/course-landing-components/",
    "suffix": "/me/?components=curriculum,price_text,reviews,incentives,instructor_bio,"
              "discount_expiration,slider_menu",
}

COURSE_DATA = {
    "prefix": "https://www.udemy.com/api-2.0/courses/",
    "suffix": "?fields[course]=primary_category,primary_subcategory,context_info,locale",
}

# length constants
COURSE_DESCRIPTION_LEN = 6000
COURSE_OBJECTIVES_LEN = 1200
COURSE_REQUIREMENTS_LEN = 1200
COURSE_HEADLINE_LEN = 252

# misc
NUM_OF_CONSEC_DAYS = 2
NUM_OF_CONSEC_EMPTY_PAGES_THRESHOLD = 3

#
CATEGORIES_JSON_PATH = "resources/categories.json"

# naming pattenrs of directories in GD repository
DASH_PATTERN = "-"
UNDERSCORE_PATTERN = "_"
CAPITAL_LETTERS_PATTERN = "AAA"
PREFIX_PATTERN = []
SUFFIX_PATTERN = []

# auth scope for GD API
SCOPES = ["https://www.googleapis.com/auth/drive"]
CREDENTIALS_PICKLE_FILEPATH = "token.pickle"

# resources data
RESOURCES_DIR_NAME = "files"

