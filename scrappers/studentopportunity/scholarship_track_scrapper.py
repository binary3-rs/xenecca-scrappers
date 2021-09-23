import uuid
from collections import defaultdict

from config.constants import SCHOLARSHIP_TRACK_URL
from dao.studentopportunity.student_opportunity_dao import StudentOpportunityDao
from database.models.studentopportunity.student_opportunity import StudentOpportunity, OpportunityType
from scrappers.base_scrapper import get_page_content, find_content_on_page
from utils.common import log_with_timestamp

scholarship_type_map = {
    "scholarships": OpportunityType.SCHOLARSHIP,
    "fellowships": OpportunityType.FELLOWSHIP,
    "internships": OpportunityType.INTERNSHIP,
    "events": OpportunityType.EVENT
}


def _extract_opporutunites_from_items(scholarship_item_list):
    next_item = scholarship_item_list
    opporuntity_type = "internships"
    opportunities = defaultdict(dict)
    while next_item is not None:
        if next_item.name == 'h2':
            opporuntity_type = next_item.attrs.get('id')
            if opporuntity_type is None:
                break
        if next_item.name == 'a':
            class_name = next_item.attrs.get('class')
            if class_name is not None:
                break
            opportunity_name = next_item.contents[0].rstrip('\xa0')
            opporuntity_link = next_item.get('href')
            if opporuntity_link is None:
                continue
            log_with_timestamp(f"New student opportunity scrapped: {opportunity_name} - {opporuntity_link}")
            opportunities[opporuntity_type][opportunity_name] = opporuntity_link
        next_item = next_item.next_element
    return opportunities


class ScholarshipTrackScrapper:
    SOURCE_WEBSITE = "https://scholarshiptrack.org/"

    def __init__(self):
        self._student_opp_dao = StudentOpportunityDao()
        self._page_content = get_page_content(SCHOLARSHIP_TRACK_URL)
        self._opportunities_urls = self._load_all_opportunity_urls()

    def _load_all_opportunity_urls(self):
        return {opportunity.origin_url for opportunity in self._student_opp_dao.find_all()}

    def delete_old_scrape_results(self):
        self._student_opp_dao.delete_by_source(ScholarshipTrackScrapper.SOURCE_WEBSITE)

    def scrape(self):
        if self._page_content is None:
            log_with_timestamp("Couldn't fetch Scholarship Track page details!")
            return
        opportunities = self._scrape_opportunities()
        student_opportunities = self._map_to_opportunity_entities(opportunities)
        self._student_opp_dao.save_all(student_opportunities)

    def _scrape_opportunities(self):
        # list of the matching elements
        matching_elements = find_content_on_page(self._page_content, "h2", {"id": "scholarships"})
        return _extract_opporutunites_from_items(matching_elements[0]) if len(matching_elements) else {}

    def _map_to_opportunity_entities(self, opportunities):
        student_opportunities = []
        for opp_type, _opportunities in opportunities.items():
            for opp_name, opp_url in _opportunities.items():
                if opp_url not in self._opportunities_urls:
                    student_opportunities.append(StudentOpportunity(**{
                        "id": uuid.uuid4(),
                        "title": opp_name,
                        "opportunity_type": scholarship_type_map[opp_type],
                        "origin_url": opp_url,
                        "source_website": ScholarshipTrackScrapper.SOURCE_WEBSITE,
                    }))
        return student_opportunities
