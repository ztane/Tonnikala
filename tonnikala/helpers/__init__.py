def escape(string):
    return string.replace('&', '&amp;')  \
                 .replace('<', '&lt;')   \
                 .replace('>', '&gt;')   \
                 .replace('"', '&#34;') \
                 .replace("'", '&#39;')


def internalcode(f):
    """Marks the function as internally used"""
    internal_code.add(f.__code__)
    return f


try:
    unicode
except:
    unicode = str


class StringWithLocation(unicode):
    def __new__(cls, value, lineno, offset):
        val = unicode.__new__(cls, value)
        val.position = lineno, offset
        return val

    def __getslice__(self, start, end):
        return self.__getitem__(slice(start, end))

    def __getitem__(self, i):
        s = unicode(self)
        if isinstance(i, slice):
            start = i.indices(len(self))[0]
            position = calculate_position(s, start, self.position)
            return StringWithLocation(s[i], position[0], position[1])

        return s[i]


def calculate_position(source, offset, start=None):
    if start is None:
        start = (1, 0)

    fragment = source[:offset]
    lines = fragment.count('\n')
    coloffset = offset - fragment.rfind('\n') if lines else offset

    if lines:
        pos = start[0] + lines, coloffset
    else:
        pos = start[0], start[1] + coloffset
    
    return pos

internal_code = set()


