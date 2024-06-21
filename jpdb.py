from bs4 import BeautifulSoup
import requests
import re


class jpdbSession:
    def __init__(self, sid: str) -> None:
        self.sid: str = sid
        self.refresh()
        self.logged: bool = not 'Login' in self.raw.text

    def refresh(self) -> None:
        raw = requests.get(
            url='https://jpdb.io/learn',
            cookies={'sid': self.sid}
        )
        self.raw = BeautifulSoup(
            raw.text,
            features='html.parser'
        )

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
