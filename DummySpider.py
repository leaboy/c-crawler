# -*- coding: utf-8 -*-

from ccrawler import CCrawler

import logging

logging.basicConfig(level=logging.DEBUG)

class DummySpider:
    start_urls = ['http://www.163.com', 'http://www.qq.com', 'http://www.sina.com.cn', 'http://www.sohu.com', 'http://www.yahoo.com', 'http://www.baidu.com', 'http://www.google.com', 'http://www.microsoft.com']
    workers = 100
    timeout = 20

    def parse(self, result):
        pass

    def pipeline(self, results):
        for r in results:
            print "Downloaded : %s(%s)" % r


class a:
    pass


spider = DummySpider()
crawler = CCrawler(spider)
crawler.start()

'''
spider2 = a()
crawler2 = CCrawler('')
crawler2.start()
'''
