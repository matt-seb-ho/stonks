import requests
import time
import datetime
import json
import csv
import entry_keys

# # datetime
# now = datetime.datetime.now()
# print('datetime(auto): ', now)
# print('unix time/epoch value: ', now.timestamp())
# 
# # http requests
# url = 'https://api.github.com'
# response1 = requests.get(url)
# print('response: ', response1) 

# build pushshift request
def build_url(after=None, before=None, search=None, sub=None, size=None):
    url = 'https://api.pushshift.io/reddit/search/submission/?sort_type=created_utc'
    params = {
        'after':after, 
        'before':before, 
        'search':search, 
        'subreddit':sub,
        'size':size
    }
    for name in params:
        if params[name] is not None:
            url += '&'
            url += (name + '=' + str(params[name]))
    return url

dummy = {}
def clean_post(post):
    for bad_key in entry_keys.irrelevant_keys:
        post.pop(bad_key, None)

def get_posts(after=None, before=None, search=None, sub=None, size=None):
    # return None
    url = build_url(after, before, search, sub, size)
    # print('url: ', url)
    r = requests.get(url)
    data = json.loads(r.text)

    print('hello')
    for post in data['data']:
        clean_post(post)

    return data['data']


SIZE_LIMIT = 100
def get_x_posts(x, data, search=None, sub=None, before=None):
    if x <= SIZE_LIMIT:
        data.extend(get_posts(search=search, sub=sub, size=x))
    else:
        next_batch = get_posts(search=search, sub=sub, size=SIZE_LIMIT)
        # print('current batch size:', len(next_batch))
        next_earliest = next_batch[0]['created_utc']
        data.extend(next_batch)
        get_x_posts(x - SIZE_LIMIT, data, search=search, sub=sub, before=next_earliest)


# def build_url(after=None, before=None, search=None, sub=None, size=None):
print(build_url(after='1d', sub='wallstreetbets'))

def date_timestamp(day):
    stamp = time.mktime(day.timetuple())
    return int(stamp)

def date_timestampe_triple(day, month, year):
    precise = time.mktime(datetime.date(year, month, day).timetuple())
    return int(stamp)

# day is a datetime object pointing to start of day
def get_posts_from_day(day, sub):
    after = date_timestamp(day)
    before = date_timestamp(day + datetime.timedelta(days=1))
    return get_posts(after=after, before=before, sub=sub, size=SIZE_LIMIT)

# # unix timestamps can be used in the before and after params
# prevHour = getPosts(after='1d', sub='nostupidquestions')
# print('len with \'1d\':', len(prevHour))
# print('item0: ', prevHour[0])
# 
# ct = datetime.datetime.now()
# after_t = ct - datetime.timedelta(days=1)
# # remove extra precision
# ts = str(after_t.timestamp()).split('.')[0]
# 
# print('timestamp:', ts)
# prevHour2 = getPosts(after=ts, sub='nostupidquestions')
# print('len with timestamp: ', len(prevHour2))
# print('item0: ', prevHour2[0])
# print('equivalent?', prevHour == prevHour2)
