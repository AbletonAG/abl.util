"""
misc functions
"""

def unicodify(text, codecs=('utf-8', 'latin-1', 'cp1252'), errors='ignore'):
    """
    cast any kind of string into a unicode string, even if the encoding is not known.
    If none of the codecs work, use 'unicode' with the errors attribute.
    """
    assert isinstance(text, basestring)
    if isinstance(text, unicode):
        return text
    for codec in codecs:
        try:
            return text.decode(codec)
        except UnicodeDecodeError:
            pass
    return unicode(text, errors=errors)


