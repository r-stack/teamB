# -*- coding: utf-8 -*-


import tweepy
import commands


from django.conf import settings

from celery.utils.log import get_task_logger
from celery.app.base import Celery
app = Celery()
app.loader.config_from_object(settings)

logger = get_task_logger(__name__)

from models import Recipe,Tweet,TwitterUser


CONSUMER_KEY = "Z6qUPji16henxLge2seayOO2J"
CONSUMER_SECRET = "VWPa9bjqws0yegJQrDYroYbRIOMbM80vGGk27lkTRlczwjOHiK"
ACCESS_TOKEN = "750936091679686656-K5WlyPc31sTB7bvanGYNwwa8wI86BFy"
ACCESS_TOKEN_SECRET = "RPVumaFYo9tWdYZ9R3KE1ybT9DJuJPDMEwwAr5TjN8dnJ"


@app.task(name="twitter.get_mentions")
def get_mentions():
    logger.info("hoge")
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    keywords = u'@BotTeamb'
    for tw in tweepy.Cursor(api.search, q=keywords).items(1):
        tweet = tw
    if tweet:
       print tweet.text
#      print tweet.user.id
#      print tweet.id
    
    tweetlog = Tweet.objects.filter(tweet_id=tweet.id)
    if len(tweetlog) > 0:
        return
    word = word_extract(tweet.text)
    cands = []
    for key in word:
        cands = Recipe.objects.filter(title__contains=key)[:1]
        if len(cands) > 0:
            break
    if len(cands) > 0:
        send_tweet(cands[0], tweet, api)
        
    return

def word_extract(text):
    command = "curl -G http://jlp.yahooapis.jp/KeyphraseService/V1/extract -d 'appid=dj0zaiZpPWVwdFY3dWZWbHc3USZzPWNvbnN1bWVyc2VjcmV0Jng9Njk-&sentence=" + text[10:].encode('utf-8') + "&output=json'"

    ret = commands.getoutput(command).decode('unicode_escape')

    output = []
    start_p = 0
    while ret[start_p:].find('"') >= 0:
        start_p = start_p + ret[start_p:].find('"') + 1
        end_p = start_p + ret[start_p:].find('"')
        output.append(ret[start_p:end_p])
        start_p = end_p +1

    return output 

def send_tweet(recipe, tweet, api):
    tweet_id = tweet.id 
    screen_name = tweet.user.screen_name.encode("UTF-8")
    reply_text = "@" + screen_name + " " + recipe.title + u"はいかがですか？\n" + recipe.recipe_url
    print reply_text
    try:
        api.update_status(status=reply_text, inreply_to_status_id=tweet_id)
    except:
        print 'TweepError'
    #user = TwitterUser.objects.get_or_create(account_id=tweet.user.id)
    Tweet.objects.get_or_create(tweet_id=tweet_id)

    return


if __name__ == "__main__":
    out = get_mentions()
    for i in out:
        print i
