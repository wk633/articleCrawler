# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb

class JobbolecrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', '', 'article_spider', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

        insert_sql = """
                        insert into article (title, create_date, url, url_object_id, praise_nums, 
                        fav_nums, tag_list, content) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item['title'], item['create_date'], item['url'], item['url_object_id'],item['praise_nums'], item['fav_nums'], item['tag_list'], item['content']))
        self.conn.commit()