
-- Silently drop everything in reverse (for development)
SET client_min_messages TO WARNING;
DROP SCHEMA "public" CASCADE;
DROP SCHEMA "random" CASCADE;
DROP SCHEMA "views" CASCADE;
SET client_min_messages TO NOTICE;
CREATE SCHEMA "public";
CREATE SCHEMA "random";
CREATE SCHEMA "views";
CREATE EXTENSION "uuid-ossp";

-------------------------------------------------------------------------------

CREATE TABLE favorites (
  user_id   uuid NOT NULL,
  tweet_id  uuid NOT NULL,
  PRIMARY KEY(user_id, tweet_id)
);

CREATE TABLE followers (
  user_id      uuid NOT NULL,
  follower_id  uuid NOT NULL, 
  created      timestamptz NOT NULL DEFAULT current_timestamp,
  PRIMARY KEY(user_id, follower_id)
);

CREATE TABLE mentions (
  user_id   uuid NOT NULL,
  tweet_id  uuid NOT NULL,  
  PRIMARY KEY(user_id, tweet_id)
);

CREATE TABLE replies (
  tweet_id  uuid NOT NULL,
  reply_id  uuid NOT NULL,
  PRIMARY KEY(tweet_id, reply_id)
);

CREATE TABLE retweets (
  tweet_id    uuid NOT NULL,
  retweet_id  uuid NOT NULL,
  PRIMARY KEY(tweet_id, retweet_id)
);

CREATE TABLE tags (
  id       uuid PRIMARY KEY NOT NULL DEFAULT uuid_generate_v4(),
  name     text NOT NULL UNIQUE,
  tweets   integer NOT NULL DEFAULT 0,
  created  timestamptz NOT NULL DEFAULT current_timestamp,
  updated  timestamptz NOT NULL DEFAULT current_timestamp
);

CREATE TABLE taggings (
  tag_id    uuid NOT NULL,
  tweet_id  uuid NOT NULL,
  PRIMARY KEY(tag_id, tweet_id)
);

CREATE TABLE tweets (
  id         uuid PRIMARY KEY NOT NULL DEFAULT uuid_generate_v4(),
  user_id    uuid NOT NULL,
  post       text NOT NULL,
  favorites  integer NOT NULL DEFAULT 0,
  replies    integer NOT NULL DEFAULT 0,
  retweets   integer NOT NULL DEFAULT 0,
  mentions   text[] NOT NULL DEFAULT '{}',
  tags       text[] NOT NULL DEFAULT '{}',
  created    timestamptz NOT NULL DEFAULT current_timestamp,
  updated    timestamptz NOT NULL DEFAULT current_timestamp
);

CREATE TABLE users (
  id         uuid PRIMARY KEY NOT NULL DEFAULT uuid_generate_v4(),
  username   text NOT NULL UNIQUE,
  passw      text NOT NULL,
  favorites  integer NOT NULL DEFAULT 0,
  followers  integer NOT NULL DEFAULT 0,
  following  integer NOT NULL DEFAULT 0,
  mentions   integer NOT NULL DEFAULT 0,
  tweets     integer NOT NULL DEFAULT 0,
  created    timestamptz NOT NULL DEFAULT current_timestamp,
  updated    timestamptz NOT NULL DEFAULT current_timestamp
);

CREATE VIEW views.retweets AS
  SELECT r.tweet_id, t.*
  FROM tweets AS t
  INNER JOIN retweets AS r
  ON t.id = r.retweet_id;
-- ############################################################################
-- # favorites
-- ############################################################################

ALTER TABLE favorites
  ADD CONSTRAINT user_fk FOREIGN KEY (user_id) REFERENCES users (id)
  MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE favorites
  ADD CONSTRAINT tweet_fk FOREIGN KEY (tweet_id) REFERENCES tweets (id)
  MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


-- ############################################################################
-- # followers
-- ############################################################################

ALTER TABLE followers
  ADD CONSTRAINT follower_fk FOREIGN KEY (follower_id) REFERENCES users (id)
  MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE followers
  ADD CONSTRAINT user_fk FOREIGN KEY (user_id) REFERENCES users (id)
  MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;

-- Don't allow users to follow themselves
ALTER TABLE followers
  ADD CONSTRAINT user_id CHECK (user_id != follower_id);


-- ############################################################################
-- # mentions
-- ############################################################################

ALTER TABLE mentions
  ADD CONSTRAINT user_fk FOREIGN KEY (user_id) REFERENCES users (id)
  MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE mentions
  ADD CONSTRAINT tweet_fk FOREIGN KEY (tweet_id) REFERENCES tweets (id)
  MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


-- ############################################################################
-- # replies
-- ############################################################################

ALTER TABLE replies
  ADD CONSTRAINT tweet_fk FOREIGN KEY (tweet_id) REFERENCES tweets (id)
  MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE replies
  ADD CONSTRAINT reply_fk FOREIGN KEY (reply_id) REFERENCES tweets (id)
  MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


-- ############################################################################
-- # reweets
-- ############################################################################

ALTER TABLE retweets
  ADD CONSTRAINT tweet_fk FOREIGN KEY (tweet_id) REFERENCES tweets (id)
  MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE retweets
  ADD CONSTRAINT retweet_fk FOREIGN KEY (retweet_id) REFERENCES tweets (id)
  MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


-- ############################################################################
-- # tags
-- ############################################################################

ALTER TABLE tags
  ADD CONSTRAINT tweets_count CHECK (tweets >= 0);

-- ############################################################################
-- # taggings
-- ############################################################################

ALTER TABLE taggings
  ADD CONSTRAINT tag_fk FOREIGN KEY (tag_id) REFERENCES tags (id)
  MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE taggings
  ADD CONSTRAINT tweet_fk FOREIGN KEY (tweet_id) REFERENCES tweets (id)
  MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


-- ############################################################################
-- # tweets
-- ############################################################################

ALTER TABLE tweets
  ADD CONSTRAINT user_fk FOREIGN KEY (user_id) REFERENCES users (id)
  MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE tweets ADD
  CONSTRAINT post_length CHECK (char_length(post) <= 140);

-- ############################################################################
-- # users
-- ############################################################################

ALTER TABLE users
  ADD CONSTRAINT mentions_count CHECK (mentions >= 0);

ALTER TABLE users
  ADD CONSTRAINT tweets_count CHECK (tweets >= 0);
-- ############################################################################
-- # tags
-- ############################################################################

CREATE UNIQUE INDEX ON tags (LOWER(name));

-- ############################################################################
-- # tweets
-- ############################################################################

CREATE INDEX ON tweets (user_id);