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
        #self.pool = eventlet.GreenPool()
        #self.task = [self.pool.spawn_n(self.fetcher) for i in range(self.workers)]
        self.task_count = 0
        self.dispatcher()

    def start(self):
        #self.pool.waitall()
        while not self.creq.empty():
            t = eventlet.spawn(self.fetcher)
            t.wait()
        '''
        for i in range(self.workers):
            t = eventlet.spawn(self.fetcher)
            t.wait()
        '''

    def dispatcher(self):
        try:
            for url in self.start_urls:
                self.creq.put(url)
        except Exception:
            logger.error("dispatcher Error!\n%s" % traceback.format_exc())
        finally:
            logger.debug("task count: %s" % self.creq.qsize())

    def fetcher(self):
        url, result = self.creq.get(), None
        with eventlet.Timeout(self.timeout, False):
            try:
                result = urllib2.urlopen(url).read()
                if result is not None:
                    self.cres.put(result)
            except eventlet.Timeout:
                print 'TimeOut: %s' % url
                return url, result
            except:
                print 'URLError: %s' % url
            else:
                logger.debug("done: %s" % url)
            finally:
                self.task_count += 1
                return url, result

    def pipeliner(self):
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