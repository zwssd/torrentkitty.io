# -*- coding: utf-8 -*-

# Scrapy settings for pornhub project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'WebHub'

SPIDER_MODULES = ['WebHub.spiders']
NEWSPIDER_MODULE = 'WebHub.spiders'

DOWNLOAD_DELAY = 0  # 间隔时间
# LOG_LEVEL = 'INFO'  # 日志级别
#### Scrapy downloader(下载器) 处理的最大的并发请求数量。 默认: 16
CONCURRENT_REQUESTS = 1
# CONCURRENT_ITEMS = 1
# CONCURRENT_REQUESTS_PER_IP = 1
#REDIRECT_ENABLED = False
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'pornhub (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

DOWNLOADER_MIDDLEWARES = {
    "WebHub.middlewares.UserAgentMiddleware": 401,
    "WebHub.middlewares.CookiesMiddleware": 402,
}
# ITEM_PIPELINES = {
#     "PornHub.pipelines.PornhubMongoDBPipeline": 403,
# }

FEED_URI=u'/home/david/lang151.csv'
FEED_FORMAT='CSV'

DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'