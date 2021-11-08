import datetime
import json
import my_ps_wrapper as ps

# print('first 3 items:', data[0:3])
fname = 'halloween_wsb.json'
WRITE_FILE = 1
if WRITE_FILE:
    halloween = datetime.date(2021, 10, 31)
    data = ps.get_posts_from_day(halloween, 'wallstreetbets')
    print('size:', len(data))
    json_f = json.dumps(data, indent=2)
    f = open(fname, 'w')
    f.write(json_f)
    f.close()
    print('Successfully written to ' + fname)

# # generate irrelevant keys
# f = open(fname)
# posts = json.load(f)
# f.close()
# print('Successfully read from', fname)
# 
# print('[', end='')
# for key in posts[0]:
#     if key not in ps.relevantKeys:
#         print('\'', key, '\', ', sep='',  end='')
# print(']')
