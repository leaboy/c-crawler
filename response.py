
# response object.
#
# $Author$
# $Id$
#
# GNU Free Documentation License 1.3

import codecs, settings
from common import deprecated_setter, UnicodeDammit, resolve_encoding

class Response:

    _DEFAULT_ENCODING = settings.DEFAULT_RESPONSE_ENCODING

    def __init__(self, url, status=200, headers=None, body='', request=None):
        self.headers = ''
        self.status = status
        self._set_body(body)
        self._set_url(url)
        self.request = request

    def _get_body(self):
        return self._body

    def _set_body(self, body):
        if isinstance(body, str):
            self._body = body
        elif isinstance(body, unicode):
            raise TypeError("Cannot assign a unicode body to a raw Response. " \
                "Use TextResponse, HtmlResponse, etc")
        elif body is None:
            self._body = ''
        else:
            raise TypeError("Response body must either str or unicode. Got: '%s'" \
                % type(body).__name__)

    body = property(_get_body, deprecated_setter(_set_body, 'body'))

    def _get_url(self):
        return self._url

    def _set_url(self, url):
        if isinstance(url, str):
            self._url = url
        else:
            raise TypeError('%s url must be str, got %s:' % (type(self).__name__, \
                type(url).__name__))

    url = property(_get_url, deprecated_setter(_set_url, 'url'))

    @property
    def encoding(self):
        return self._get_encoding(infer=True)

    def _get_encoding(self, infer=False):
        if infer:
            enc = self._body_inferred_encoding()
        else:
            enc = None
        if not enc:
            enc = self._DEFAULT_ENCODING
        return resolve_encoding(enc)

    def _body_inferred_encoding(self):
        enc = self._get_encoding()
        dammit = UnicodeDammit(self.body, [enc], isHTML=True)
        return dammit.originalEncoding