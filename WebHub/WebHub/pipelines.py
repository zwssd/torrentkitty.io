# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
#from WebHub.items import Lang151Item

class SqliteDBPipeline(object):
    def __init__(self):
        # 如果数据库不存在的话，将会自动创建一个 数据库
        self.conn = sqlite3.connect('../lang151.db')
        # 创建一个游标 curson
        self.cursor = self.conn.cursor()

        '''clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["PornHub"]
        self.PhRes = db["PhRes"]
        idx = IndexModel([('link_url', ASCENDING)], unique=True)
        self.PhRes.create_indexes([idx])
        # if your existing DB has duplicate records, refer to:
        # https://stackoverflow.com/questions/35707496/remove-duplicate-in-mongodb/35711737'''

    def insert_link(self, title, url):
        self.cursor.execute("INSERT INTO lang151 (title,url) VALUES ('" + title + "','" + url + "')")
        # 提交事物
        self.conn.commit()

        '''print 'MongoDBItem', item
        """ 判断类型 存入MongoDB """
        if isinstance(item, PornVideoItem):
            print 'PornVideoItem True'
            try:
                self.PhRes.update_one({'link_url': item['link_url']}, {'$set': dict(item)}, upsert=True)
            except Exception:
                pass'''
        return self.cursor.lastrowid
