# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import pymongo
import sqlite3


class sqlitePipeline:
    collection_name = "best_movies"

    # @classmethod
    # def from_crawler(cls, crawler):
    #     logging.warning(crawler.settings.get("MONGO_URI"))

    def open_spider(self, spider):
        self.connection = sqlite3.connection("imdb.db")
        self.c = self.connection.cursor()
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS best_movies (
                title TEXT,
                year INTEGER,
                rating REAL,
        ''')
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO best_movies (title, year, rating)
            VALUES (?, ?, ?)
        ''', item.get('title'), item[year], item[rating])
        return item


class ImdbPipeline:
    collection_name = "best_movies"

    # @classmethod
    # def from_crawler(cls, crawler):
    #     logging.warning(crawler.settings.get("MONGO_URI"))

    def open_spider(self, spider):
        logging.warning("SPIDER OPEN FROM PIPELINE")
        # self.file = open('imdb.csv', 'w')
        # self.file.write('name,year,rating,genre,director,cast,plot\n')
        self.client = pymongo.MongoClient("")
        self.db = self.client["imdb"]

    def close_spider(self, spider):
        logging.warning("SPIDER CLSOED FROM PIPELINE")
        # self.file.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item
