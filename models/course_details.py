
class CourseDetails:
    def __init__(self):
        self.title = None
        self.categories = []
        self.udemy_url = None
        self.poster_path = None
        self.authors = []
        self.languages = []
        self.old_price = 0
        self.new_price = 0
        self.discount_percent = 0
        self.time_coupon_still_active = None
        self.headlne = None
        self.goals = None
        self.included_info = {}
        self.num_of_enrolled_students = 0
        self.num_of_reviews = 0
        self.avg_score = 0.0
        self.description = None
        self.faq = {}
        self.curriculum = {}
        self.reviews = {}

    def build(self, **kwargs):
        for key, value in kwargs:
            if hasattr(self, key):
                setattr(self, key, value)
