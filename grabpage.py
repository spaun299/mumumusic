import urllib.request
import re
import pprint

pp = pprint.PrettyPrinter(indent=4)

def grabPage(url):
  f = urllib.request.urlopen(url)
  page = f.read().decode('utf-8')

# print(page)
# page = ''
  searchresult = re.search('page=(\d+)[^>]*Next page', page)
  pp.pprint(searchresult)                                                             #go away
  if searchresult:
    nextpage = searchresult.group(1)
  else:
    nextpage = False
# <a href="/user/kakabomba/tracks?page=3" class="btn btn--icon-only btn--small btn--white iconright iconright--right" rel="next" title="Next page">Next</a>
  return nextpage, []

def buildUrl(page):
  return "http://www.last.fm/user/kakabomba/tracks?page=2"

grabPage(buildUrl(2))
