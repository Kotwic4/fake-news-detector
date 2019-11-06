import json

import psycopg2
from datetime import datetime
from random import shuffle
import os

PATH_TO_DATA_DIRECTORY = '/Users/grzegorz/Downloads/fakenewsnet_dataset/politifact'
FAKE_ARTICLE_DIRECTORY = PATH_TO_DATA_DIRECTORY + '/fake'
REAL_ARTICLE_DIRECTORY = PATH_TO_DATA_DIRECTORY + '/real'

conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=password")
cur = conn.cursor()


def insert_article(is_fake, is_training, title, article_text, url, article_source, keywords, description, authors,
                   published_at):
    sql = """INSERT INTO article(is_fake, is_training, title, article_text, url,
        article_source, keywords, description, authors, published_at)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING article_id;"""
    cur.execute(sql, (is_fake, is_training, title, article_text, url, article_source,
                      keywords, description, authors, published_at))
    conn.commit()
    return cur.fetchone()[0]


def insert_user(twitter_user_id, user_name, screen_name, location, description, followers_count, friends_count,
                created_at):
    sql = """INSERT INTO users(twitter_user_id, user_name, screen_name, location, description,
            followers_count, friends_count, created_at)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s) RETURNING user_id;"""
    cur.execute(sql, (str(twitter_user_id), user_name, screen_name, location, description,
                      followers_count, friends_count, created_at))
    conn.commit()
    return cur.fetchone()[0]


def search_for_user(user_name):
    sql = """SELECT user_id FROM users where user_name = %s"""
    cur.execute(sql, (user_name,))
    conn.commit()
    return cur.fetchall()


def insert_tweet(article_id, user_id, tweet_text, created_at, retweet_count, favourite_count, contributors,
                 in_reply_to_user_id):
    sql = """INSERT INTO tweet(article_id, user_id, tweet_text, created_at, retweet_count,
        favourite_count, contributors, in_reply_to_user_id)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s) RETURNING tweet_id;"""
    cur.execute(sql, (article_id, user_id, tweet_text, created_at, retweet_count,
                      favourite_count, contributors, str(in_reply_to_user_id)))
    conn.commit()
    return cur.fetchone()[0]


def parse_date_from_seconds(seconds):
    try:
        return datetime.utcfromtimestamp(seconds)
    except:
        return None


def parse_date(date):
    try:
        return datetime.strptime(date, '%a %b %d %H:%M:%S %z %Y')
    except Exception as e:
        return None


def extract_description(data):
    try:
        return data['meta_data']['description']
    except:
        return None


def extract_data(articles, root, is_fake, is_training):
    for dir in articles:
        try:
            with open(root + "/" + dir + "/news content.json", "r") as json_file:
                data = json.load(json_file)
                article_id = insert_article(is_fake, is_training,
                                            data['title'],
                                            data['text'],
                                            data['url'],
                                            data['source'],
                                            ", ".join(data['keywords']),
                                            extract_description(data),
                                            ", ".join(data['authors']),
                                            parse_date_from_seconds(data['publish_date']))

            for r, d, tweet_files in os.walk(root + "/" + dir + "/" + "tweets"):
                for tweet_file in tweet_files:
                    with open(r + "/" + tweet_file) as json_file:
                        data = json.load(json_file)
                        result = search_for_user(data['user']['name'])

                        if len(result) == 0:
                            user_id = insert_user(data['user']['id'],
                                                  data['user']['name'],
                                                  data['user']['screen_name'],
                                                  data['user']['location'],
                                                  data['user']['description'],
                                                  data['user']['followers_count'],
                                                  data['user']['friends_count'],
                                                  parse_date(data['user']['created_at']))
                        else:
                            user_id = result[0][0]

                        insert_tweet(article_id,
                                     user_id,
                                     data['text'],
                                     parse_date(data['created_at']),
                                     data['retweet_count'],
                                     data['favorite_count'],
                                     data['contributors'],
                                     data['in_reply_to_user_id'])


        except Exception as e:
            continue


def extact_data_by_directory(dir_path, is_fake):
    for root, dirs, files in os.walk(dir_path):
        shuffle(dirs)
        training_articles = dirs[:int(len(dirs) * 0.8)]
        testing_articles = dirs[int(len(dirs) * 0.8) + 1:]

        extract_data(training_articles, root, is_fake, True)
        extract_data(testing_articles, root, is_fake, False)

        cur.close()
        conn.close()
        break


if __name__ == '__main__':
    extact_data_by_directory(FAKE_ARTICLE_DIRECTORY, True)
    extact_data_by_directory(REAL_ARTICLE_DIRECTORY, False)
