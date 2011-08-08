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

import eventlet
from eventlet import queue
from eventlet.green import urllib2
from response import Response

import traceback
import logging

logger = logging.getLogger(__name__)

class CCrawler:
    def __init__(self, spider):
        self.spider = GetAttr(spider)
        self.workers = GetAttr(self.spider, 'workers', 10)
        self.timeout = GetAttr(self.spider, 'timeout', 120)
        self.start_urls = GetAttr(self.spider, 'start_urls', [])
        self.creq = queue.Queue()
        self.cres = queue.Queue()
        self.pool = eventlet.GreenPool(self.workers)
        self.task = [self.pool.spawn_n(self.fetcher) for i in self.start_urls]
        self.task_count = 0
        self.dispatcher()

    def dispatcher(self):
        try:
            for url in self.start_urls:
                self.creq.put(url)
        except Exception:
            logger.error("dispatcher Error!\n%s" % traceback.format_exc())
        finally:
            logger.info("Task Count: %s" % self.creq.qsize())

    def fetcher(self):
        url, body, status, headers, response = self.creq.get(), None, 200, None, None
        with eventlet.Timeout(self.timeout, False):
            try:
                request = urllib2.Request(url)
                response = urllib2.urlopen(request)
            except eventlet.Timeout:
                logger.error('TimeOut: %s' % url)
            except urllib2.HTTPError, e:
                status = e.code
                logger.error('URLError: %s(%s)' % (url, status))
            finally:
                body = response.read()
                response = Response(url, status, headers, body, request)
                self.cres.put(response)
                logger.info('fetching: %s' % url)
                self.task_count += 1

    def pipeliner(self):
        pass

    def start(self):
        logger.info("CCrawler start...")
        self.pool.waitall()
        self.resmap()
        logger.info("CCrawler closed.")

    def stop(self):
        pass

    def resmap(self):
        rslist = []
        while not self.cres.empty():
            rslist.append(self.cres.get())
        parse = GetAttr(self.spider, 'parse', object)
        pool = eventlet.GreenPool(self.workers)
        for rs in rslist:
            pool.spawn_n(parse, rs)
        pool.waitall()


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