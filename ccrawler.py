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
        self.timeout = GetAttr(self.spider, 'timeout', 3)
        self.start_urls = GetAttr(self.spider, 'start_urls', [])
        self.creq = queue.Queue()
        self.cres = queue.Queue()
        self.task = queue.Queue()
        print self.spider, self.workers, self.timeout, self.start_urls, self.creq, self.cres, self.task

    def start(self):
        pass

    def dispatcher(self):
        try:
            for item in scheduler:
                self.qin.put(item)
        except Exception, e:
            logger.error("Scheduler Error!\n%s" % traceback.format_exc())
        finally:
            for i in range(self.job_count - 2):
                self.qin.put(StopIteration)
            self.job_count -= 1
            logger.debug("Scheduler done, job count: %s" % self.job_count)

    def fetcher(self, url):
        if hasattr(self.spider, 'parse'):
            parse = self.spider.parse
        else:
            parse = None

    def pipeliner(self):
        pass

def GetAttr(object, name=None, default=None):
    try:
        if object is None:
            return None
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