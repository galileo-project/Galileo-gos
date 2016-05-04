_ENCODE = ["utf-8", "gbk"]

def decode(byte):
    for e in _ENCODE:
        try:
            string = byte.decode(e)
            return string
        except UnicodeDecodeError:
            pass
    raise Exception()

def is_str(string):
    try:
        return isinstance(string, (unicode, str))
    except:
        return isinstance(string, str)