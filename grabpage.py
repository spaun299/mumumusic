import urllib.request
import re
from print_info import Debug,Error,Info
import db_fill
from  buildpage import Build



def grabPage(url, userid):
    f = urllib.request.urlopen(url)
    page = f.read().decode('utf-8')
    searchresult = re.search('page=(\d+)[^>]*Next page', page)
    Debug(searchresult)  #go away
    if searchresult:
        nextpage = searchresult.group(1)
    else:
        nextpage = False
    line = re.findall(
            '<a href="/music/([^/]+)/_/([^/]+)"\s+class="recent-tracks-image media-pull-left media-link-hook">.*? datetime="([\d\-:TZ]+)"',
            page, re.S)
    Debug(line)
    for item in line:
        bandid = db_fill.insertBandName(item[0])  #insert in db-dict
       # grabBandPage(build.build_band_url(item[0]),bandid)
        grabBandPage(Build(bandname=item[0]).build(),bandid)
        songid = db_fill.insertSongName(item[1], bandid)  #insert in db-dict
        db_fill.insertListening(userid, songid, item[2])
    return nextpage


def grabUserPages(username):
    userid = db_fill.insertUser(Build(username=username).build(),username)  # NEW!!!
    Info('Grabbing Pages for User %s' % username)
    nextpage = 1
    while nextpage != False:
        Info('Grabbing Page %s for User' % nextpage)
        nextpage = grabPage(Build(username=username, page=nextpage).build(), userid)



def grabBandPage(url, bandid):
    Debug(url)
    try:
        f = urllib.request.urlopen(url)
        page = f.read().decode('utf-8')
        #googletag.pubads().setTargeting("tag", "punk,punkrock,british,70s,rock,classicrock,classicpunk,alternative,sexpistols,britishpunk");
        line = re.findall('googletag\.pubads\(\)\.setTargeting\("tag", "([^"]+)"\);', page)  #find all tag-words
        if not len(line):
            return
        tags = line[0].split(',')  #я не зрозуміла. перепояснити!!!
        for item in tags:
            genreid = db_fill.insertGenreName(item)
            db_fill.insertGenreBandMx(bandid, genreid)
    except:
        Error("can't grab band page %s for bandid=%s" % (url , bandid))

