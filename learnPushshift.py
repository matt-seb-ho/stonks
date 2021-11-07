import pandas as pd
import datetime
import requests
import json
import csv
import datetime

"""
# datetime
now = datetime.datetime.now()
print('datetime(auto): ', now)
print('unix time/epoch value: ', now.timestamp())

# http requests
url = 'https://api.github.com'
response1 = requests.get(url)
print('response: ', response1) 
"""

# pushshift request
def add_url_param(url, name, val):
	if not val:
		url += ('&' + name + '=' + val)
	return url

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

def get_posts(after=None, before=None, search=None, sub=None, size=None):
	# return None
	url = build_url(after, before, search, sub, size)
	# print('url: ', url)
	r = requests.get(url)
	data = json.loads(r.text)
	return data['data']

# print(buildURL(after = datetime.datetime.now().timestamp(), sub = 'dogecoin'))
# print(getPosts(after = '1d', sub = 'dogecoin'))

# prevHour = getPosts(after='1d', sub='nostupidquestions')
# print('len: ', len(prevHour))
# print('item0: ', prevHour[0])
# 
# ct = datetime.datetime.now()
# after_t = ct - datetime.timedelta(days=1)
# ts = str(after_t.timestamp()).split('.')[0]
# 
# print('timestamp:', ts)
# prevHour2 = getPosts(after=ts, sub='nostupidquestions')
# print('len: ', len(prevHour2))
# print('item0: ', prevHour2[0])

# print('they are equal?', prevHour == prevHour2)

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

def is_why_q(post):
	# return (post['title'][0:3].lower() == 'why')
	return ('why' in post['title'].lower())

def get_why_qs(sub, num_posts):
	posts = []
	get_x_posts(num_posts, posts, sub=sub)
	print('total posts:', len(posts))
	return [post['title'] for post in posts if is_why_q(post)]

# why_qs = get_why_qs('askreddit', 500)
# print(len(why_qs))
# if len(why_qs) > 10:
# 	print(why_qs[:10])


# def build_url(after=None, before=None, search=None, sub=None, size=None):
print(build_url(after='1d', sub='wallstreetbets'))
