import requests
import json
import sys
import random
from time import sleep

self_id = int(sys.argv[1])
cluster_id = int(sys.argv[2])
num_clusters = int(sys.argv[3])
num_followers = int(sys.argv[4])
server = sys.argv[5]

username = "client_{}_{}".format(cluster_id, self_id)

# Defining the query url
url = 'http://{}/api'.format(server)

# Signup
q = {"Mutation":{"create_profile":({"username":"{}".format(username), "password":"pass"}, "token")}}
x = requests.post(url, json = q)
# Loading Cookie
cookie = json.loads(x.text)['data']
print("{} Logged In".format(username))

# Tweeting Entry
q = {"Mutation":{"create_tweet":({"tweet_content":"Hi! I am {}".format(username), "tags":[], "mentions_list":[]}, ('tweet_post',{'user':'user_name'}))}}
x = requests.post(url, json = q, cookies=cookie)
data = json.loads(x.text)['data']
print("{} Tweeted: {}".format(username, data['tweet_post']))

sleep(2)
for i in range(num_followers):
	if i==self_id:
		continue
	q = {"Mutation":{"follow":({"username":"client_{}_{}".format(cluster_id, i)}, 'status')}}
	x = requests.post(url, json = q, cookies=cookie)
	if 'True' in x.text:
		print("{} Followed client_{}_{}".format(username, cluster_id, i))

# Get Feed
q = {"Query":{"twitter_feed":({}, (['tweets', ('tweet_post',{'user':'user_name'})],))}}
x = requests.post(url, json = q, cookies=cookie)
data = json.loads(x.text)['data']['tweets']
for t in data:
	print("{} Received Feed: {} tweets - {}".format(username, t['user']['user_name'], t['tweet_post']))