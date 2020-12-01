def fetch_data(cur,obj, table, key, value):
	attrs = [k for k,v in vars(obj) if v==None]
	cur.execute("SELECT %s FROM %s WHERE %s=%s", (' '.join(attrs), table, key, value))
	data = zip(attrs, cur.fetchone())
	for k,v in data:
		setattr(obj, k, v)

class User:
	def __init__(self, cur, user_id):
		self.id = user_id
		self.cur = cur
		self.username = None
		self.favourites = None
		self.followers = None
		self.following = None
		self.mentions = None
		self.tweets = None
		self.created = None
		self.updated = None

	def uid(self):
		return self.id

	def user_name(self):
		if self.username == None:
			fetch_data(self.cur, self, "users", "id", self.id)
		return self.user_name


class Tweet:
	def __init__(self, cur, tid, user_id=None, post=None, favourites=None, replies=None, retweets=None, mentions=None, tags=None, created=None, updated=None):
		self.cur = cur
		self.id = tid
		self.user_id = user_id
		self.userobj = False if user_id==None else User(cur, user_id)
		self.post = post
		self.favourites = favourites
		self.replies = replies
		self.retweets = retweets
		self.tags = tags
		self.mentions = mentions
		self.created = created
		self.updated = updated

	def tweet_id(self):
		return self.tid

	def user(self):
		if self.userobj==False:
			fetch_data(self.cur, self, "tweets", "id", self.id)
		return self.userobj

	def tweet_post(self):
		if self.post==None:
			fetch_data(self.cur, self, "tweets", "id", self.id)
		return self.post