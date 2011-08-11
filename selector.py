#!/usr/bin/python
#-*-coding:utf-8-*-

# selector (xpath and regex).
#
# $Author$
# $Id$
#
# GNU Free Documentation License 1.3

from lxml import etree
from common import encoding, extract_regex
from list import SelectorList



class HtmlSelector(object):
    def __init__(self, text):
        if not hasattr(text, '__iter__'):
            self.text = encoding(text)
            self.text = self.parse(self.text)
        else:
            self.text = text

    def select(self, xpath):
        try:
            result = self.text.xpath(xpath)
        except etree.XPathError:
            raise ValueError("Invalid XPath: %s" % xpath)

        if hasattr(result, '__iter__'):
            result = [self.__class__(x) \
                for x in result]
        else:
            result = [self.__class__(result)]
        return SelectorList(result)

    def re(self, regex):
        return extract_regex(regex, self.text)

    def extract(self):
        try:
            return etree.tostring(self.root, method=self._tostring_method, \
                encoding=unicode)
        except (AttributeError, TypeError):
            #return unicode(self.root)
            pass

    def parse(self, text):
        parser = etree.HTMLParser(remove_blank_text=True, remove_comments=True)
        return etree.HTML(text, parser)


content = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>

<body>
<form>
	<div id='leftmenu'>
		<h3>标题一</h3>
		<ul>
            <li>// 列表一</li>
            <li>// 列表二</li>
        </ul>
        <h3>标题二</h3>
		<ul>
            <li>// 列表三</li>
            <li>// 列表四</li>
        </ul>
	</div>
	<ul>
		<li><a href="/news/23" title="实时新闻概况">南昌百人跳江事件背后</a></li>
		<li><a href="/news/453" title="xpath">XPath应用示例</a></li>
	</ul>
</form>
</body>
</html>
'''

hxs = HtmlSelector(content)
itemlist = hxs.select('//li')

for item in itemlist:
    title = item.select('a/text()').extract()
    print title
    #print title
    #print item