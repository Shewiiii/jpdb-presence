from pypresence import Presence
import time
from dotenv import load_dotenv
import os
import time
from jpdb import jpdbSession


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

while True:
    jpdb.refresh()
    due = jpdb.get_due()
    known = jpdb.get_known_words()

    if due:
        RPC.update(
            large_image='logo',
            details=f'{due} Due cards remaining',
            state=f'{known} Known words',
            large_text='\\(￣︶￣*\\))',
            start=start_epoch
        )
    else:
        RPC.update(
            large_image='logo',
            details=f'Learning...',
            state=f'{known} Known words',
            large_text='\\(￣︶￣*\\))',
            start=start_epoch
        )

    time.sleep(10)
