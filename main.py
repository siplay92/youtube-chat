# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import tkinter
from message_scheduler import *

TRANSLATION_ID = 'PzawWO5TtGo'

BROADSCAST_STATUS_ACTIVE = 'active'
BROADSCAST_STATUS_ALL = 'all'
BROADSCAST_STATUS_COMPLETED = 'completed'
BROADSCAST_STATUS_UPCOMING = 'upcoming'

LIVE_CHAT_PART_ID = 'id'
LIVE_CHAT_PART_SNIPPET = 'snippet'
LIVE_CHAT_PART_AUTHOR_DETAILS = 'authorDetails'

youtube = Youtube()

# response = youtube.live_broadcasts.list_by_id(TRANSLATION_ID)
# print(json_pretty(response))

response = youtube.live_broadcasts.list_by_broadcast_status(BROADSCAST_STATUS_ACTIVE)
# print(json_pretty(response))

live_chats = youtube.extract_live_chat_id(response)
# print(live_chats)

if len(live_chats) == 0:
    raise Exception('No chat found')

live_chat_id = live_chats[0].get('live_chat_id')

messageScheduler = MessageScheduler()
messageScheduler.schedule(youtube, live_chat_id)

# response = youtube.youtube_live_chat.list(live_chat_id, LIVE_CHAT_PART_SNIPPET, 100)
# print(json_pretty(response))

# response = youtube.youtube_live_chat.list(live_chat_id, LIVE_CHAT_PART_AUTHOR_DETAILS, 100)
# print(json_pretty(response))


"""
root = tkinter.Tk()
root.mainloop()
root.winfo_screenwidth = 500
"""
