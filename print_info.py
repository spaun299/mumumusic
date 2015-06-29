import pprint
pp = pprint.PrettyPrinter(indent=4)
def debug(s):
    # pp.pprint(s)
    pass

def error(s):
    pp.pprint(s)
    pass

def info(s):
    pp.pprint(s)
    pass
