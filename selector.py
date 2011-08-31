
# selector (xpath and regex).
#
# $Author$
# $Id$
#
# GNU Free Documentation License 1.3

from lxml import etree
from response import Response
from common import extract_regex, body_as_utf8
from python import unicode_to_str
from list import HtmlSelectorList

class HtmlSelector:
    __slots__ = ['html', 'text', 'expr', 'namespaces', '_root', '_xpathev']
    _parser = etree.HTMLParser
    _tostring_method = 'html'

    def __init__(self, response=None, text=None, root=None, expr=None, namespaces=None):
        if text:
            self.response = Response(url='about:blank', \
                body=unicode_to_str(text, 'utf-8'), encoding='utf-8')
        else:
            self.response = response
        self._root = root
        self._xpathev = None
        self.namespaces = namespaces
        self.expr = expr

    @property
    def root(self):
        if self._root is None:
            parser = self._parser(encoding=self.response.encoding, recover=True)
            self._root = etree.fromstring(self.utf8body, parser=parser)
        return self._root

    @property
    def xpathev(self):
        if self._xpathev is None:
            self._xpathev = etree.XPathEvaluator(self.root, namespaces=self.namespaces)
        return self._xpathev

    def select(self, xpath):
        try:
            result = self.xpathev(xpath)
        except etree.XPathError:
            raise ValueError("Invalid XPath: %s" % xpath)

        if hasattr(result, '__iter__'):
            result = [self.__class__(root=x, expr=xpath, namespaces=self.namespaces) \
                for x in result]
        else:
            result = [self.__class__(root=result, expr=xpath, namespaces=self.namespaces)]
        return HtmlSelectorList(result)

    def re(self, regex):
        result = extract_regex(regex, self.utf8body)
        if not self._root:
            result = [self.__class__(text=x, root=self.utf8body) \
                for x in result]
        return result
    '''
    def Link(self):
        return self._root
        parser = self._parser(encoding=self.htmlencoding, recover=True)
        root = etree.fromstring(self.html['text'], parser=parser)
        xpatheval = etree.XPathEvaluator(root)
        try:
            result = xpatheval('a/@href')
            return etree.tostring(root, method='html', encoding=unicode)
        except etree.XPathError:
            pass
    '''
    def extract(self):
        try:
            return etree.tostring(self.root, method=self._tostring_method, \
                encoding=unicode)
        except (AttributeError, TypeError):
            return unicode(self.root)