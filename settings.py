import os
import json

TWITTER = os.getenv("TWITTER")

if TWITTER:
    TWITTER = json.loads(TWITTER)

TWEET_TEXT = os.getenv("TWEET_TEXT")

TRACK_ITEM = os.getenv("TRACK_ITEM")

try:
    from local_settings import *
except ImportError as e:
    pass
