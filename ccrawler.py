#!/usr/bin/python
#-*-coding:utf-8-*-

# Main App.
#
# $Author$
# $Id$
#
# Lib: eventlet, lxml
#
# GNU Free Documentation License 1.3

from __future__ import with_statement

import common
import eventlet
from eventlet import queue
from eventlet.green import urllib2
from response import Response

import logging, traceback
logger = common.logger(name=__name__, filename='ccrawler.log', level=logging.DEBUG)

class CCrawler:
    def __init__(self, spider):
        self.spider = GetAttr(spider)
        self.workers = GetAttr(self.spider, 'workers', 10)
        self.timeout = GetAttr(self.spider, 'timeout', 120)
        self.start_urls = GetAttr(self.spider, 'start_urls', [])
        self.creq = queue.Queue()
        self.cres = queue.Queue()
        self.pool = eventlet.GreenPool(self.workers)
        self.task = [self.pool.spawn_n(self.fetch_coroutine) for i in range(self.workers)]
        self.task_done = 0
        self.dispatcher()

    def dispatcher(self):
        try:
            for url in self.start_urls:
                self.creq.put(url)
        except Exception:
            logger.error("dispatcher Error!\n%s\n" % traceback.format_exc())

    def fetch_coroutine(self):
        while not self.creq.empty():
            self.fetcher()

    def fetcher(self):
        url, body, status, headers, response, = self.creq.get(), None, 200, None, None
        request = urllib2.Request(url)
        t = eventlet.Timeout(self.timeout, False)
        try:
            response = urllib2.urlopen(request)
            body = response.read()
        except urllib2.HTTPError, e:
            status = e.code
        except urllib2.URLError, e:
            logger.error('URLError: %s%s' % (url, e.args[0]))
        except eventlet.Timeout, e:
            logger.error('TimeOut: %s(%s)' % (url, e))
        except:
            logger.error('URLError: Could not resolve url "%s"' % url)
        finally:
            t.cancel()
            response = Response(url, status, headers, body, request)
            self.cres.put(response)
            logger.info('Fetched: %s' % url)
            self.task_done += 1

    def pipeliner(self):
        pass

    def start(self):
        logger.info("CCrawler start...")

        self.pool.waitall()

        '''
        pool = eventlet.GreenPool(self.workers)
        for i in range(self.workers):
            pool.spawn_n(self.parsepool)
        pool.waitall()
        '''

        logger.info("CCrawler closed.\n")

    def stop(self):
        pass

    def parsepool(self):
        parse = GetAttr(self.spider, 'parse', self.parse)
        while not self.cres.empty():
            rslist.append(self.cres.get())
        pool = eventlet.GreenPool()
        for rs in rslist:
            pool.spawn_n(parse, rs)

    def parse(self, response):
        '''when spider's parse is empty, then use this replace with do nothing'''
        pass


def GetAttr(object, name=None, default=None):
    try:
        if object is None:
            return default
        elif not type(object).__name__=='instance':
            raise Exception

        if name==None:
            return object
        else:
            if not hasattr(object, str(name)):
                return default
            else:
                return getattr(object, name)
    except Exception:
        logger.error('Spider not exist!')