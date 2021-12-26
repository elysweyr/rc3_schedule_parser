from typing import Optional

import datetime

import dateutil
import pytz
from bs4 import BeautifulSoup
from requests_html import AsyncHTMLSession

from rc3 import RC3Talk

RC3_TALK_MODAL_CSS_SELECTOR = ".modal-dialog"
HTML_PARSER_MODE = "html.parser"


class RC3TalkParser():
    TIME_ZONE = dateutil.tz.gettz('Europe / Berlin')

    def __init__(self, url: str):
        self.url = url
        self.soup = None
        self.__talk_metadata = {}

    def __parse_title(self) -> str:
        return self.soup.find("h3", class_="modal-title").text

    def __scrub_german_locales(self, date) -> str:
        return date.replace("Januar", "January").replace("Februar", "February").replace("März", "March").replace("Mai", "May").replace("Juni", "June").replace("Juli", "July").replace("Oktober", "October").replace("Dezember", "December")

    def __parse_description(self) -> str:
        return self.soup.find("p").text

    def __parse_start_date(self) -> datetime:
        scrubbed_date = self.__talk_metadata["start"].replace(".", "").replace(",", "")
        scrubbed_date = self.__scrub_german_locales(scrubbed_date)

        try:
            start_date = datetime.datetime.strptime(scrubbed_date, '%b %d %Y %I %p')
        except:
            try:
                start_date = datetime.datetime.strptime(scrubbed_date, '%b %d %Y %-I:%M %p')
            except:
                start_date = datetime.datetime.strptime(scrubbed_date, '%d %B %Y %H:%M')

        start_date = pytz.utc.localize(start_date)
        start_date = start_date.replace(tzinfo=self.TIME_ZONE)
        return start_date

    def __parse_end_date(self) -> datetime:
        duration_str = self.__talk_metadata["duration"]

        time = datetime.datetime.strptime(duration_str, "%H:%M:%S")
        time_delta = datetime.timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)

        return self.__parse_start_date() + time_delta

    def __parse_room(self) -> str:
        return self.__talk_metadata["room"]

    def __parse_language(self) -> str:
        return self.__talk_metadata["language"]

    def __parse_speakers(self) -> str:
        return self.__talk_metadata["speakers"]

    def __parse_join_url(self) -> str:
        return self.soup.find("a").text

    def __parse_track(self) -> str:
        return self.__talk_metadata["track"]

    def __get_rc3_talk(self, soup: BeautifulSoup) -> str:
        self.init_talk_metadata()

        title = self.__parse_title()
        description = self.__parse_description()
        start_date = self.__parse_start_date()
        end_date = self.__parse_end_date()
        room = self.__parse_room()
        track = self.__parse_track()
        language = self.__parse_language()
        speakers = self.__parse_speakers()
        join_url = self.__parse_join_url()

        return RC3Talk(title, description, start_date, end_date, room, track, language, speakers, join_url, self.url)

    def __no_event_modal_found(self, modals_dom_elements) -> bool:
        return len(modals_dom_elements) == 0

    async def parse_rc3_schedule_url(self, url: str) -> Optional[RC3Talk]:
        await self.__init_parser()

        if not self.__init_succeeded:
            return None

        return self.__get_rc3_talk(self.soup)

    def init_talk_metadata(self):
        table_values = self.soup.find_all(["dt", "dd"])

        metadata_dict = {}

        for i in range(0, len(table_values) - 1, 2):
            metadata_dict[table_values[i].text.lower()[:-1]] = table_values[i + 1].text

        self.__talk_metadata = metadata_dict

    async def __init_parser(self):
        session = AsyncHTMLSession()
        page = await session.get(self.url, headers={
            "Accept-Language": "en",
            "Content-Language": "en"
        })
        await page.html.arender()

        modals_dom_elements = page.html.find(RC3_TALK_MODAL_CSS_SELECTOR)

        if self.__no_event_modal_found(modals_dom_elements):
            self.__init_succeeded = False
            return

        modal_dom = modals_dom_elements[0]
        self.soup = BeautifulSoup(modal_dom.html, HTML_PARSER_MODE)
        self.__init_succeeded = True
