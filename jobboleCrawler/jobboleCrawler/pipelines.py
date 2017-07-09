# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from MySQLdb.cursors import DictCursor
from twisted.enterprise import adbapi

class JobbolecrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

# image download
class ArticleImagesPipeline(ImagesPipeline):
    # override original get_media_requests
    def get_media_requests(self, item, info):
        front_img_url = item.get('front_img_url')
        if front_img_url:
            return Request(front_img_url)

    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value['path']
            item["front_img_path"] = image_file_path
        return item

# save to mysql
class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', '', 'article_spider', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

        insert_sql = """
                        insert into article (title, create_date, url, url_object_id, praise_nums, 
                        fav_nums, tag_list, content, front_image_url, front_image_path) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item['title'], item['create_date'], item['url'], item['url_object_id'],item['praise_nums'], item['fav_nums'], item['tag_list'], item['content'], item['front_img_url'], item['front_img_path']))
        self.conn.commit()

# save to mysql
class MysqlAsyncPipeline(object):
    @classmethod
    def from_crawler(cls, cralwer):
        settings = cralwer.settings
        dbParams = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbParams)
        return cls(dbpool)

    def __init__(self, dbPool):
        self.dbPool = dbPool

    def process_item(self, item, spider):
        insertion = self.dbPool.runInteraction(self.insertRow, item)
        insertion.addErrback = self.error_handler

    def insertRow(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)
        # commit automatically

    def error_handler(self, e):
        print(e)