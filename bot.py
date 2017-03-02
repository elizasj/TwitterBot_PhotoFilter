#!/usr/bin/env python
# coding: utf-8
from treatment import image_treatment
from daemonize import Daemonize
from TwitterAPI import TwitterAPI
import logging
import urllib.request
import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
fh = logging.FileHandler("labelgum.log", "w")
formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]
pid = "labelgum.pid"

api = TwitterAPI(settings.TWITTER.get("consumer_key"),
                 settings.TWITTER.get("consumer_secret"),
                 settings.TWITTER.get("access_token_key"),
                 settings.TWITTER.get("access_token_secret"))


def repost_to_twitter(file_to_send, screen_name):
    TWEET_TEXT = "@{0} {1}".format(screen_name, settings.TWEET_TEXT)
    filtered_img = open(file_to_send, 'rb')
    data = filtered_img.read()
    repost = api.request('statuses/update_with_media',
                         {'status': TWEET_TEXT},
                         {'media[]': data})
    return repost


# def labelgum_bot():
tweets = api.request('statuses/filter', {'track': settings.TRACK_ITEM})
logger.debug("Listening on Twitter API - Tracking {0}".format(settings.TRACK_ITEM))
for tweet in tweets:
    if tweet.get("extended_entities"):
        imgs_on_twitter = tweet['extended_entities']['media']
        if len(imgs_on_twitter) >= 1:
                first_img = imgs_on_twitter[0]
                url = "{}:large".format(imgs_on_twitter[0]["media_url"])
                filename = "{}.jpg".format(imgs_on_twitter[0]["id_str"])
                screen_name = tweet["user"]["screen_name"]
                img_to_edit = urllib.request.urlretrieve(url, filename)

                try:
                    final_filename = image_treatment(filename)
                except ValueError:
                    logger.debug("Picture is too small")
                except Exception as e:
                    logger.debug(e)
                else:
                    repost_to_twitter(final_filename, screen_name)
                    logger.debug("Tweet sent to {0}".format(screen_name))

# daemon = Daemonize(app="labelgum_bot", pid=pid, action=labelgum_bot, keep_fds=keep_fds)
# daemon.start()
