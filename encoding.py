import codecs

from settings import ENCODING_ALIASES_BASE, ENCODING_ALIASES

_ENCODING_ALIASES = dict(ENCODING_ALIASES_BASE)
_ENCODING_ALIASES.update(ENCODING_ALIASES)

def encoding_exists(encoding, _aliases=_ENCODING_ALIASES):
    """Returns ``True`` if encoding is valid, otherwise returns ``False``"""
    try:
        codecs.lookup(resolve_encoding(encoding, _aliases))
    except LookupError:
        return False
    return True

def resolve_encoding(alias, _aliases=_ENCODING_ALIASES):
    """Return the encoding the given alias maps to, or the alias as passed if
    no mapping is found.
    """
    return _aliases.get(alias.lower(), alias)
