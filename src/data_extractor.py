import json

import psycopg2
import psycopg2.extras
from datetime import datetime
from random import shuffle
import os

PATH_TO_DATA_DIRECTORY = './fakenewsnet_dataset/politifact'
FAKE_ARTICLE_DIRECTORY = PATH_TO_DATA_DIRECTORY + '/fake'
REAL_ARTICLE_DIRECTORY = PATH_TO_DATA_DIRECTORY + '/real'

CONN = psycopg2.connect("host=eksploracjadanych.cfp1phbzfxbf.us-east-1.rds.amazonaws.com dbname=eddb user=postgres password=password")
CUR = CONN.cursor()
USERS = []
USERS_NAME_TO_USER_ID = {}

def insert_article(is_fake, is_training, title, article_text, url, article_source, keywords, description, authors,
                   published_at):
    sql = """INSERT INTO article(is_fake, is_training, title, article_text, url,
        article_source, keywords, description, authors, published_at)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING article_id;"""
    CUR.execute(sql, (is_fake, is_training, title, article_text, url, article_source,
                      keywords, description, authors, published_at))
    CONN.commit()
    return CUR.fetchone()[0]


def insert_user(users_to_insert):
    sql = """INSERT INTO users(twitter_user_id, user_name, screen_name, location, description,
            followers_count, friends_count, created_at)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"""
    psycopg2.extras.execute_batch(CUR, sql, users_to_insert, page_size=1000)
    CONN.commit()


def search_for_user():
    sql = """SELECT user_id, user_name from users"""
    CUR.execute(sql)
    CONN.commit()
    return CUR.fetchall()


def insert_tweet(tweets_to_insert):
    sql = """INSERT INTO tweet(article_id, user_id, tweet_text, created_at, retweet_count,
        favourite_count, contributors, in_reply_to_user_id)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s); """
    psycopg2.extras.execute_batch(CUR, sql, tweets_to_insert, page_size=1000)
    CONN.commit()


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
    global CONN, CUR
    for dir in articles:
        print("Actual dir: " + dir)
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

            users_to_insert = []

            for r, d, tweet_files in os.walk(root + "/" + dir + "/" + "tweets"):
                for tweet_file in tweet_files:
                    with open(r + "/" + tweet_file) as json_file:
                        data = json.load(json_file)

                        if not data['user']['name'] in USERS:
                            users_to_insert.append((data['user']['id'],
                                                  data['user']['name'],
                                                  data['user']['screen_name'],
                                                  data['user']['location'],
                                                  data['user']['description'],
                                                  data['user']['followers_count'],
                                                  data['user']['friends_count'],
                                                  parse_date(data['user']['created_at'])))
                            USERS.append(data['user']['name'])
                insert_user(users_to_insert)
                result = search_for_user()
                for user in users_to_insert:
                    USERS_NAME_TO_USER_ID[user[1]] = [item[0] for item in result if item[1] == user[1]][0]
            tweets_to_insert = []

            for r, d, tweet_files in os.walk(root + "/" + dir + "/" + "tweets"):
                for tweet_file in tweet_files:
                    with open(r + "\\" + tweet_file) as json_file:
                        data = json.load(json_file)
                        user_id = USERS_NAME_TO_USER_ID[data['user']['name']]
                        tweets_to_insert.append((article_id,
                                                 user_id,
                                                 data['text'],
                                                 parse_date(data['created_at']),
                                                 data['retweet_count'],
                                                 data['favorite_count'],
                                                 data['contributors'],
                                                 data['in_reply_to_user_id']))
                insert_tweet(tweets_to_insert)
        except psycopg2.ProgrammingError as e:
            print("ProgrammingError while processing dir: " + dir + " " + str(e))
            CONN.rollback()
        except psycopg2.InterfaceError as e:
            print("InterfaceError while processing dir: " + dir + " " + str(e))
            CONN = psycopg2.connect(
                "host=eksploracjadanych.cfp1phbzfxbf.us-east-1.rds.amazonaws.com dbname=eddb user=postgres password=password")
            CUR = CONN.cursor()
        except Exception as e:
            print("Exception while processing dir: " + dir + " " + str(e))
            continue


def extact_data_by_directory(dir_path, is_fake):
    for root, dirs, files in os.walk(dir_path):
        shuffle(dirs)
        training_articles = dirs[:int(len(dirs) * 0.8)]
        testing_articles = dirs[int(len(dirs) * 0.8) + 1:]

        extract_data(training_articles, root, is_fake, True)
        extract_data(testing_articles, root, is_fake, False)

        CUR.close()
        CONN.close()
        break


if __name__ == '__main__':
    extact_data_by_directory(FAKE_ARTICLE_DIRECTORY, True)
    extact_data_by_directory(REAL_ARTICLE_DIRECTORY, False)
