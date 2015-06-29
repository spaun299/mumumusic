import urllib.request
import re
from print_info import debug,error,info
import db_fill
from  buildpage import Build



def grab_page(url, userid):
    f = urllib.request.urlopen(url)
    page = f.read().decode('utf-8')
    searchresult = re.search('page=(\d+)[^>]*Next page', page)
    debug(searchresult)  #go away
    if searchresult:
        nextpage = searchresult.group(1)
    else:
        nextpage = False
    line = re.findall(
            '<a href="/music/([^/]+)/_/([^/]+)"\s+class="recent-tracks-image media-pull-left media-link-hook">.*? datetime="([\d\-:TZ]+)"',
            page, re.S)
    debug(line)
    for item in line:
        bandid = db_fill.insert_band_name(item[0])  #insert in db-dict
       # grabBandPage(build.build_band_url(item[0]),bandid)
        grab_band_page(Build(bandname=item[0]).build(),bandid)
        songid = db_fill.insert_song_name(item[1], bandid)  #insert in db-dict
        db_fill.insert_listening(userid, songid, item[2])
    return nextpage


def grab_user_pages(username):
    userid = db_fill.insert_user(Build(username=username).build(),username)  # NEW!!!
    info('Grabbing Pages for User %s' % username)
    nextpage = 1
    while nextpage != False:
        info('Grabbing Page %s for User' % nextpage)
        nextpage = grab_page(Build(username=username, page=nextpage).build(), userid)



def grab_band_page(url, bandid):
    debug(url)
    try:
        f = urllib.request.urlopen(url)
        page = f.read().decode('utf-8')
        #googletag.pubads().setTargeting("tag", "punk,punkrock,british,70s,rock,classicrock,classicpunk,alternative,sexpistols,britishpunk");
        line = re.findall('googletag\.pubads\(\)\.setTargeting\("tag", "([^"]+)"\);', page)  #find all tag-words
        if not len(line):
            return
        tags = line[0].split(',')  #я не зрозуміла. перепояснити!!!
        for item in tags:
            genreid = db_fill.insert_genre_name(item)
            db_fill.insert_genre_band_mx(bandid, genreid)
    except:
        error("can't grab band page %s for bandid=%s" % (url , bandid))

