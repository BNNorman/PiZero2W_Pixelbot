
# taken from https://github.com/lucien2k/wipy-urllib/blob/master/urllib.py
always_safe = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'
               'abcdefghijklmnopqrstuvwxyz'
               '0123456789' '_.-')

def quote(s):
    res = []
    replacements = {}
    for c in s:
        if c in always_safe:
            res.append(c)
            continue
        res.append('%%%x' % ord(c))
    return ''.join(res)

def unquote(s):
    """Kindly rewritten by Damien from Micropython"""
    """No longer uses caching because of memory limitations"""
    """xrange replaced with range BNN 23/3/24 """
    res = s.split('%')
    for i in range(1, len(res)):
        item = res[i]
        try:
            res[i] = chr(int(item[:2], 16)) + item[2:]
        except ValueError:
            res[i] = '%' + item
    return "".join(res)

def parse(s):
    items=s.split("\n")
    # first entry should be like GET /upload?program=%23%20MQTT... HTTP...
    parts=items[0].split(" ") # to remove the trailing HTTP and GET
    get=parts[1]    
    prog=get.split("=",1)
    return unquote(prog[1])


if __name__=="__main__":
    
    print(parse("GET /upload?program=%23%20MQTT%20test%20script%0Aimport% HTTP"))
    