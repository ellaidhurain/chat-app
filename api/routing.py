from django.urls import re_path
from . import consumers

# app routing like app urls
# websocket specific url patterns

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+/$)',consumers.chatRoomConsumer) 
]

# re_path regular expression path. Regular expressions provide a flexible way to match
# (and sometimes modify) text strings based on patterns.
# regular expression is a pattern of all mixed upper case lowercase with numbers and special characters
# (?P<room_name>\w+) capture group expression is used to capture the room
# w is match word character any word with any length
# & is ends the search url and throws error