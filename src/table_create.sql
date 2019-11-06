CREATE TABLE article(
   article_id serial PRIMARY KEY,
   is_fake BOOLEAN,
   is_training BOOLEAN,
   title text,
   article_text text,
   url text,
   article_source text,
   keywords text,
   description text,
   authors text,
   published_at timestamp
);


create table users(
	user_id serial primary key,
	twitter_user_id text,
	user_name text,
	screen_name text,
	location text,
	description text,
	followers_count integer,
	friends_count integer,
	created_at timestamp
);


create table tweet(
	tweet_id serial primary key,
	article_id integer references article(article_id),
	user_id integer references users(user_id),
	tweet_text text,
	created_at timestamp,
	retweet_count integer,
	favourite_count integer,
	contributors text,
	in_reply_to_user_id text

);
