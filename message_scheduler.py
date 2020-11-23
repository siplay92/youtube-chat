import sched, time

from base import *
from youtuber import *


class MessageScheduler(object):
    LIVE_CHAT_PART_ID = 'id'
    LIVE_CHAT_PART_SNIPPET = 'snippet'
    LIVE_CHAT_PART_AUTHOR_DETAILS = 'authorDetails'

    scheduler = None

    def get_new_message(self, sc, youtube: Youtube, live_chat_id: str, next_page_token: str = None):
        # do request to chat
        response = youtube.youtube_live_chat.list(live_chat_id, self.LIVE_CHAT_PART_SNIPPET, 10, next_page_token)

        next_page_token = response.get('nextPageToken')  # TODO is changing?

        polling_interval_millis = response.get('pollingIntervalMillis')  # TODO ++

        print(json_pretty(response.get('items')))

        self.scheduler.enter(polling_interval_millis / 1000, 1, self.get_new_message, (sc, youtube, live_chat_id, next_page_token))

    def schedule(self, youtube: Youtube, live_chat_id: str):
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.scheduler.enter(0, 1, self.get_new_message, (self.scheduler, youtube, live_chat_id))
        self.scheduler.run()
