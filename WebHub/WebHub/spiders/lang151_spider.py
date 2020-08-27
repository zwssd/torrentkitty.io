#coding:utf-8
import requests
import logging
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from WebHub.items import Lang151Item
from WebHub.pipelines import SqliteDBPipeline
from WebHub.pornhub_type import PH_TYPES
from WebHub.download_m3u8 import download_m3u8
from scrapy.http import Request
import re
import json
import random
import base64
import sys
import os
import datetime
import urllib.parse

class Spider(CrawlSpider):
    name = 'lang151_spider'
    host = 'https://torrentkitty.io/'
    start_urls = list(set(PH_TYPES))
    pipelines = SqliteDBPipeline()

    file_name = 1

    test_model = False
    if test_model:
        logging.getLogger("requests").setLevel(logging.WARNING)  # 将requests的日志级别设成logging.WARNING
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
            datefmt='%a, %d %b %Y %H:%M:%S',
            filename='cataline.log',
            filemode='w')
    else:
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

    # test = True
    def start_requests(self):
        if self.test_model:
            file_dir = "/home/david/download_m3u8/"
            temp_dir = "/home/david/download_m3u8/" + "haha"
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            dm = download_m3u8()
            dm.start_download("http://www.ting74.com/tingshu/6945", temp_dir, file_dir, "aaaa")
        else:
            for ph_type in self.start_urls:
                #print("insert db start......")
                #self.pipelines.insert_link("LIST", self.host + ph_type)
                #print("insert db end......")
                yield Request(url=self.host + ph_type, callback=self.parse_magnet_address)

    def parse_magnet_address(self, response):
        #logging.debug('response:------>' + response.text)
        #sys.exit(0)
        selector = Selector(response)
        #logging.debug('request url:------>' + response.url)
        #logging.info(selector)
        lis = selector.xpath('//table[@id="archiveResult"]//tr')
        for li in lis:
            logging.debug('li :------>' + li.extract())
            viewkey = re.findall('href="magnet(.*?)"', li.extract())
            logging.debug('viewkey :------>' + viewkey[0])
            #self.pipelines.insert_link("ITEM", self.host + viewkey[0])
            #yield Request(url=self.host + viewkey[0],callback=self.parse_play_address)
        '''url_next = selector.xpath('//a[@class="wrpage wr_pagefirst" and text()="下一页"]/@href').extract()
        #logging.debug('len(url_next) :------>' + str(len(url_next)))
        #logging.debug('url_next :------>' + url_next[0])
        if url_next:
            # if self.test:
            #logging.debug(' next page:=====>>>>>' + self.host + url_next[0])
            self.pipelines.insert_link("NEXT LIST", self.host + url_next[0])
            yield Request(url=self.host + url_next[0], callback=self.parse_ph_key)'''

    def parse_play_address(self, response):
        selector = Selector(response)
        play_address = selector.xpath('//iframe/@src').extract()
        logging.debug('play_address :------>' + play_address[0])
        if play_address:
            # if self.test:
            logging.debug(' play address:=====>>>>>>>>>>' + self.host + play_address[0])
            yield Request(url=self.host + play_address[0], callback=self.parse_m4a_url)
            #logging.debug(' play address2222222222:=====>>>>>>>>>>' + self.host + play_address[0])

    def parse_m4a_url(self, response):
        phItem = Lang151Item()
        selector = Selector(response)
        #logging.debug('m4a_url=====>>>>>>>>>>>>>>>>>>>>>'+selector.extract())
        _ph_info = re.findall('http://audio(.*?)\'', selector.extract())
        url = 'http://audio' + _ph_info[0]
        if url.find('.m4a') == -1:
            url = url+'.m4a'
        logging.debug('播放地址信息的JSON:=====>>>>>'+url)

        file_dir = "/home/david/download_m4a/m4a/"
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        dm = download_m3u8()
        dm.start_download(url, file_dir, format(self.file_name)+'.m4a')
        self.file_name += 1

        yield phItem
