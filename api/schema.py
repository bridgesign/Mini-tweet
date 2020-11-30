from .objects import User
from https import token


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

		if username=='uu' and password=='pass':

			return token.create_token({'uid':'as'}, 3600)
		else:
			return Error("Credential Error")

	def access(self, ctx):
		if 'username' in ctx:
			return User(ctx['uid'])
		else:
			return Error("Not Logged In")


class Mutation:
	def __init__(self, obj=None):
		self.obj = obj

	def create_profile(self, username:str, password:str):
		'''
		First time users
		'''
		conn, cur = self.obj['conn'], self.obj['cur']
		try:
			cur.execute("INSERT INTO users (username, passw) VALUES (%s, %s);", (username, password))
		except:
			conn.rollback()
			return Error("Username not unique")

		conn.commit()
		cur.execute(f"SELECT id FROM users WHERE username={username};")
		user_id = cur.fetchone()[0]
		return token.create_token({'uid':user_id}, 3600)

	def tweet_tags_count(self):
		'''
		Function for count of tweets grouped with tags 
		'''
		conn, cur = self.obj['conn'], self.obj['cur']
		try:
			cur.execute("SELECT id FROM users WHERE username=%s;", username)

			cur.execute(f"INSERT INTO tags (name, tweets) VALUES ({tags});")
		
		except:
			conn.rollback()
			return Error("Error in creating tweet")
		conn.commit()


	def create_tweet(self, ctx, tweet_content:str, tags:str, mentions:str):
		'''
		Tweet Entry
		'''
		conn, cur = self.obj['conn'], self.obj['cur']

		user_id = ctx['uid']
		try:
			cur.execute(f"INSERT INTO tweets (user_id, post, mentions, tags) VALUES ({user_id}, {tweet_content}, {mentions}, {tags});")
		except:
			conn.rollback()
			return Error("Error in creating tweet")
		conn.commit()	 

class Subscription:
	def __init__(self, obj=None):
		self.obj = obj
