class User:
	def __init__(self, cur, user_id):
		self.user_id = user_id
		self.cur = cur
		self.user_name = None

	def uid(self):
		return self.user_id

	def username(self):
		if self.user_name == None:
			self.cur.execute("SELECT username FROM users WHERE user_id=%s", (self.user_id,))
			self.user_name = self.cur.fetchone()[0]
		return self.user_name


class Tweet:
	def __init__(self, cur, tid, user_id, post, favourites=None, replies=None, retweets=None, mentions=None, tags=None, created=None, updated=None):
		self.tid = tid
		self.cur = cur
		self.userobj = User(cur, user_id)
		self.post_txt = post
		self.favourites = favourites
		self.replies = replies
		self.retweets = retweets
		self.mentions = mentions
		self.created = created
		self.updated = updated

	def tweet_id(self):
		return self.tid

	def user(self):
		return self.userobj

	def post(self):
		return self.post_txt