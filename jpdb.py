from bs4 import BeautifulSoup, NavigableString
import requests
from dotenv import load_dotenv
import os
import re

load_dotenv()
SID = os.getenv('SID')
learn_page = 'https://jpdb.io/learn'

'''
    tr examples:
    'LearningYou\xa0know'
    [<tr><th></th><th></th><th>Learning</th><th>You know</th></tr>,
    <tr><td>Words (direct)</td><td>30977</td><td>689</td><td>5880 (18%)</td></tr>,
    <tr><td>Words (indirect)</td><td>54</td><td>0</td><td>1 (1%)</td></tr>]

    [<tr><th></th><th></th><th>Learning</th><th>You know</th></tr>,
    <tr><td>Words (direct)</td><td>30977</td><td>138</td><td>5880 (18%)</td></tr>,
    <tr><td>Kanji (direct)</td><td>2836</td><td>3</td><td>0 (0%)</td></tr>,
    <tr><td>Words (indirect)</td><td>54</td><td>0</td><td>1 (1%)</td></tr>,
    <tr><td>Kanji (indirect)</td><td>248</td><td>0</td><td>0 (0%)</td></tr>]
'''


class jpdbSession:
    def __init__(self, sid: str) -> None:
        self.sid: str = sid
        self.learn_page: str = learn_page
        self.raw: BeautifulSoup = BeautifulSoup()
        self.refresh()
        self.logged: bool = not 'Login' in self.raw.text

    def refresh(self) -> None:
        raw = requests.get(
            url=self.learn_page,
            cookies={'sid': self.sid}
        )
        raw.encoding = 'UTF-8'
        self.raw = BeautifulSoup(
            raw.text,
            features='html.parser'
        )

    def get_known_words(self, redundant: bool = False) -> int:
        if redundant:
            table = self.raw.find('table', {'class': 'cross-table'})
            tr_list = table.find_all('tr')
            return int(re.findall(r'\d+', str(tr_list[1]))[2])
        else:
            return int(re.findall(r'\d+', self.raw.find('p').text)[0])

    def get_due(self) -> int | None:
        span = self.raw.find('span', {'style': 'color: red;'})
        if not span:
            return None
        return int(span.text)


if __name__ == '__main__':
    jpdb = jpdbSession(SID)
    print(jpdb.get_known_words())
    print(jpdb.get_due())
