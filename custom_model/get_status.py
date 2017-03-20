import codecs
import sys
import requests
import json
import twitter
import config


def convert_status_to_pi_content_item(s):
    # My code here
    return {
        'userid': str(s.user.id),
        'id': str(s.id),
        'sourceid': 'python-twitter',
        'contenttype': 'text/plain',
        'language': s.lang,
        'content': s.text,
        'created': s.created_at_in_seconds,
        'reply': (s.in_reply_to_status_id == None),
        'forward': False
    }


handle = sys.argv[1]

twitter_api = twitter.Api(consumer_key=config.twitter_consumer_key,
                          consumer_secret=config.twitter_consumer_secret,
                          access_token_key=config.twitter_access_token,
                          access_token_secret=config.twitter_access_secret,
                          debugHTTP=True)

max_id = None
statuses = []
with codecs.open('statuses/statuses_' + handle + '_output.txt', mode='w', encoding='utf8') as outputfile:
    for x in range(0, 16):  # Pulls max number of tweets from an account
        if x == 0:
            statuses_portion = twitter_api.GetUserTimeline(screen_name=handle,
                                                       count=200,
                                                       include_rts=False)
            status_count = len(statuses_portion)
            max_id = statuses_portion[status_count - 1].id - 1  # get id of last tweet and bump below for next tweet set
        else:
            statuses_portion = twitter_api.GetUserTimeline(screen_name=handle,
                                                           count=200,
                                                           max_id=max_id,
                                                           include_rts=False)
            status_count = len(statuses_portion)
            if status_count == 0:
                break
            max_id = statuses_portion[max(0, status_count - 1)].id - 1  # get id of last tweet and bump below for next tweet set
        for status in statuses_portion:
            outputfile.write(status.text + '\nTWEETLINEBREAK\n')
