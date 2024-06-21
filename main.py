from pypresence import Presence
import time
from dotenv import load_dotenv
import os
import time
from jpdb import jpdbSession
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


# Load variables
load_dotenv()
SID = os.getenv('SID')
CLIENT_ID = os.getenv('CLIENT_ID')
start_epoch = int(time.time())

# Load jpdb session
jpdb = jpdbSession(SID)
assert jpdb.logged, 'SID not valid !'

# Load pypresence
RPC = Presence(CLIENT_ID)
RPC.connect()


def update(details: str, state: str) -> None:
    # Function to make the code a bit lighter
    RPC.update(
        large_image='logo',
        large_text='\\(￣︶￣*\\))',
        start=start_epoch,
        state=state,
        details=details
    )


logging.info('Rich presence is active !')

while True:
    jpdb.refresh()
    due = jpdb.get_due()
    known = jpdb.get_known_words()
    logging.info(f'Known words: {known}, Due cards: {due}')

    if due:
        update(
            f'Reviewing | {due} Cards remaining',
            f'{known} Known words',
        )
    else:
        stats: dict = jpdb.get_stats()
        new_today = stats['new'][-1]
        remaining_new = jpdb.new_cards_limit - new_today
        logging.info(msg=f'New cards remaining: {remaining_new}')
        if remaining_new > 0:
            update(
                f'Learning | {remaining_new} New cards remaining',
                f'{known} Known words'
            )
        else:
            update(
                f'Learning new words !',
                f'{known} Known words'
            )

    time.sleep(10)
