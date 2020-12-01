import requests
import json
import sys
import random

username = sys.argv[1]
cluster_id = sys.argv[2]
num_clusters = int(sys.argv[3])
num_followers = int(sys.argv[4])
server = sys.argv[5]

# Defining the query url
url = 'http://{}/api'.format(server)

# Signup
q = {"Mutation":{"create_profile":({"username":"{}".format(username), "password":"pass"}, "token")}}
x = requests.post(url, json = q)
# Loading Cookie
cookie = json.load(x.text)['data']
print("{} Logged In".format(username))

# Tweeting Entry
q = {"Mutation":{"create_tweet":({"tweet_content":"Hi! I am {}".format(username), "tags":[], "mentions_list":[]}, ('tweet_post',{'user':'user_name'}))}}
x = requests.post(url, json = q)
data = json.loads(x.text)['data']
print("{} Tweeted: {}".format(username, data['tweet_post']))

for i in range(num_followers):
	q = {"Mutation":{"create_tweet":({"tweet_content":"Hi! I am {}".format(username), "tags":[], "mentions_list":[]}, ('tweet_post',{'user':'user_name'}))}}