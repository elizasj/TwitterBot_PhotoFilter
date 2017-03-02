from settings import api


def repost_to_twitter(final_filename, screen_name):
    TWEET_TEXT = "@{} voici ta Part Postale par @partcompanyband".format(screen_name)
    filtered_img = open(final_filename, 'rb')
    data = filtered_img.read()
    repost = api.request('statuses/update_with_media',
                         {'status': TWEET_TEXT},
                         {'media[]': data})
    print("SUCCESS" if repost.status_code == 200 else "FAILURE")
