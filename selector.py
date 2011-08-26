
# selector (xpath and regex).
#
# $Author$
# $Id$
#
# GNU Free Documentation License 1.3

from lxml import etree
from common import encoding, extract_regex
from list import HtmlSelectorList

class HtmlSelector:
    __slots__ = ['html', 'text', 'expr', 'namespaces', '_root', '_xpathev']
    _parser = etree.HTMLParser
    _tostring_method = 'html'

    def __init__(self, html=None, text=None, root=None, expr=None, namespaces=None, encoding=None):
        if html:
            print encoding(html)
            self.html = encoding(html)
        elif text:
            self.html = encoding(text)
        else:
            self.html = encoding('None')
        if not encoding:
            self.encoding = self.html['encoding']
        self._root = root
        self._xpathev = None
        self.namespaces = namespaces
        self.expr = expr

    @property
    def root(self):
        if self._root is None:
            parser = self._parser(encoding=self.encoding, recover=True)
            self._root = etree.fromstring(self.html['text'], parser=parser)
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
            result = [self.__class__(root=x, expr=xpath, namespaces=self.namespaces, encoding=self.encoding) \
                for x in result]
        else:
            result = [self.__class__(root=result, expr=xpath, namespaces=self.namespaces, encoding=self.encoding)]
        return HtmlSelectorList(result)

    def re(self, regex):
        result = extract_regex(regex, self.html['text'].encode(self.encoding))
        if not self._root:
            result = [self.__class__(html=x, root=self.html, encoding=self.encoding) \
                for x in result]
        return result

    def extract(self):
        try:
            return etree.tostring(self.root, method=self._tostring_method, \
                encoding=unicode)
        except (AttributeError, TypeError):
            return unicode(self.root)