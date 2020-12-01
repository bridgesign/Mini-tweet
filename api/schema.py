from .objects import User, Tweet
from https import token

def get_SQLarray(simple_list):
	return '{'  +  ','.join(simple_list)  +  '}' 

class Error:
	def __init__(self, msg, code:int = 0):
		self.msg = msg
		self.code = code
	def repr(self):
		return {"Error":self.msg, "status":str(self.code)}

class Query:
	def __init__(self, obj=None):
		self.obj = obj

	def login(self, ctx, username:str, password:str):
		conn, cur = self.obj['conn'], self.obj['cur']
		cur.execute("SELECT id FROM users WHERE username=%s AND passw=%s", (username, password))
		
		user_id = cur.fetchone()[0]

		if user_id is not None:
			return token.create_token({'uid':user_id}, 3600*24*10)
		else:
			return Error("Invalid username or password.")

	def access_followers(self, ctx):
		'''
		IDs which the current user follows
		'''
		conn, cur = self.obj['conn'], self.obj['cur']
		user_id = ctx['uid']
		cur.execute("SELECT follower_id FROM followers WHERE user_id=%s", (user_id,))
		raw_list = cur.fetchall()

		followers_list = [User(cur, each_id[0]) for each_id in raw_list]
		return followers_list
	
	def access_tweets(self, ctx, user_id, count:int):
		'''
		Access 'count' no. of tweets when visiting profile

		'''
		conn, cur = self.obj['conn'], self.obj['cur']
		cur.execute("SELECT * FROM tweets WHERE user_id=%s", (user_id,))
		raw_list = cur.fetchall()

		return [Tweet(cur, *t) for t in raw_list[:count]]
	
	def twitter_feed(self, ctx, tweet_per_user=5):
		'''
		Personalized Twitter feed
		'''
		
		if 'uid' not in ctx:
			return Error("Not Logged In")

		conn, cur = self.obj['conn'], self.obj['cur']
		user_id = ctx['uid']
		followers_list = self.access_followers(ctx)

		tweets_data = []

		for follower in followers_list:
			tweets_data.extend(self.access_tweets(ctx, user_id=follower.uid(), count=tweet_per_user))

		return tweets_data
		
class Mutation:
	def __init__(self, obj=None):
		self.obj = obj

	def create_profile(self, ctx, username:str, password:str):
		'''
		First time users
		'''
		conn, cur = self.obj['conn'], self.obj['cur']
		try:
			cur.execute("INSERT INTO users (username, passw) VALUES (%s, %s) RETURNING id;", (username, password))
		except:
			conn.rollback()
			return Error("Username not unique")

		conn.commit()
		user_id = cur.fetchone()[0]
		return token.create_token({'uid':user_id}, 3600*24*10)

	def create_tweet(self, ctx, tweet_content:str, tags:list, mentions_list:list, FLAG_retweet=False):
		'''
		Tweet Entry
		'''
		conn, cur = self.obj['conn'], self.obj['cur']

		tags = get_SQLarray(tags)
		mentions_list = get_SQLarray(mentions_list)

		user_id = ctx['uid']

		try:
			cur.execute("INSERT INTO tweets (user_id, post, mentions, tags) VALUES (%s, %s, %s, %s) RETURNING id;", vars=(user_id, tweet_content, mentions_list, tags))			
		except:
			conn.rollback()
			return Error("Error in creating tweet")
		
		tweet = Tweet(cur, cur.fetchone()[0])
		conn.commit()	 

		if len(mentions)!=0:
			self.mentions(ctx, mentions_list, tweet.tweet_id(), conn, cur)

		return tweet

		def follow(self, ctx, other_uid):
			'''
			Twitter follow
			'''
			conn, cur = self.obj['conn'], self.obj['cur']
			user_id = ctx['uid']
			
			try:
				cur.execute("INSERT INTO followers (user_id, follower_id) VALUES (%s, %s);", (user_id, other_uid))
			except 
				conn.rollback()
				return Error("Error in following user")
		
			conn.commit()	 
			return token.create_token({'uid':user_id, 'recent_follower_id':other_uid}, 3600)
		
		def block(self, ctx, tobe_blocked_id):
			'''
			Twitter Blocking users
			'''
			conn, cur = self.obj['conn'], self.obj['cur']
			user_id = ctx['uid']

			try:
				cur.execute("DELETE FROM followers WHERE user_id=%s AND follower_id=%s", (user_id, tobe_blocked_id))
			except:
				conn.rollback()
				return Error("Error in blocking user")
			conn.commit()	 
			return token.create_token({'uid':user_id}, 3600)
		
		def mention(self, ctx, mentions_list, tweet_id, conn, cur):
			'''
			Mentions in tweet
			'''
			try:
				for each_id in mentions_list:
					cur.execute("INSERT INTO mentions (user_id, tweet_id) VALUES (%s, %s);", (each_id, tweet_id))
			except:
				conn.rollback()
				return Error("Error in blocking user")
			conn.commit()	 
			return True
		
		def retweet(self, ctx, tweet_id, retweet_content:str, tags:list, mentions_list:list):
			'''
			Retweets
				: A normal tweet + retweet data
			'''
			conn, cur = self.obj['conn'], self.obj['cur']
			user_id = ctx['uid']
			retweet_id = self.create_tweet(ctx, retweet_content:str, tags:list, mentions_list:list, FLAG_retweet=True)

			try:
				cur.execute("INSERT INTO retweets (tweet_id, retweet_id) VALUES (%s, %s);", (tweet_id, retweet_id))
			except:
				conn.rollback()
				return Error("Error in retweeting")				
			
			conn.commit()	 
			return token.create_token({'uid':user_id, 'recent_tweet_id':retweet_id}, 3600)


class Subscription:
	def __init__(self, obj=None):
		self.obj = obj
