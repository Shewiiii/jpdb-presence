from bs4 import BeautifulSoup
from bs4.element import Tag
import requests
import re
import logging


def bs(url: str, sid: str) -> BeautifulSoup:
    # Function to make the code a bit lighter
    logging.info(f'Request: {url}')
    return BeautifulSoup(
        requests.get(
            url=url,
            cookies={'sid': sid},
        ).text,
        features='html.parser'
    )


class jpdbSession:
    def __init__(self, sid: str) -> None:
        self.sid: str = sid
        self.refresh()
        self.logged: bool = not 'Login' in self.raw.text
        self.new_cards_limit: int | None = self.get_new_cards_limit()

    def refresh(self) -> None:
        self.raw = bs('https://jpdb.io/learn', self.sid)

    def get_stats(self) -> dict:
        raw = bs('https://jpdb.io/stats', self.sid)
        chart: Tag = raw.find_all('script')[4]
        nums = [eval(i) for i in re.findall(r'\d+', chart.text)]
        failed = nums[12:20]
        passed = nums[25:33]
        new = nums[38:46]
        return {
            'failed': failed,
            'passed': passed,
            'new': new
        }

    def get_new_cards_limit(self) -> int | None:
        raw = bs('https://jpdb.io/settings', self.sid)
        max = raw.find(
            'input',
            {'id': 'max-new-cards-per-day'}
        )
        if not max:
            return None
        return int(max['value'])

    def get_known_words(self, redundant: bool = False) -> int:
        if redundant:
            return int(re.findall(r'\d+', str(self.raw.find_all('tr')[1]))[2])
        else:
            return int(re.findall(r'\d+', self.raw.find('p').text)[0])

    def get_due(self) -> int | None:
        span = self.raw.find('span', {'style': 'color: red;'})
        if not span:
            return None
        return int(span.text)
