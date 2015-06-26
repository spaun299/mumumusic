import urllib.request
import re
import pprint
import datetime
from sqlalchemy import MetaData,create_engine,insert
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
pp = pprint.PrettyPrinter(indent=4)
DEBUG = True
metadata=MetaData()
engine = create_engine('postgresql://postgres:minkovski@postgres.d/MusicGenreMigration')     # connection to SQLALCHEMY db
metadata.reflect(engine, only=['dicband','dicsong','userlist','listening','dicgenre','bandgenremx']) #connect to tables
Base = automap_base(metadata=metadata) # make auto-generation existing tables and classes
Base.prepare()
connection=engine.connect()
# Connect classes to tables
Band=Base.classes.dicband
Song=Base.classes.dicsong
User=Base.classes.userlist
Listening=Base.classes.listening
Genre=Base.classes.dicgenre
BandAndGen=Base.classes.bandgenremx
#create session handler
sql_session = Session(engine)

def Debug(s):
    # pp.pprint(s)
    pass

def Error(s):
    pp.pprint(s)
    pass

def Info(s):
    pp.pprint(s)
    pass


def insertSongName(songname, bandid):
    # Add Song into dicsong table and than Select id
    try:
        sql_session.add(Song(songname=songname,bandid=bandid))
        sql_session.commit()
    except:
        sql_session.rollback()
    for song in sql_session.query(Song):
        if songname==song.songname and bandid==song.bandid:
            Info(song.songname)
            return song.songid



def insertBandName(bandname):
    # Add Band into dicband table and than Select id
    try:
        sql_session.add(Band(bandname=bandname))
        sql_session.commit()
    except:
        sql_session.rollback()
    # print("INSERT INTO dicband(bandname) VALUES ('%s')" % (bandname,))
    #conn.commit()
    for band in sql_session.query(Band):
        if bandname==band.bandname:
            return band.bandid


# --------------------------------------------------------------------18th May-------
def buildBandUrl(bandname):
    return ("http://www.last.fm/music/%s" % (bandname))


def grabBandPage(url, bandid):
    # Debug(url)
    try:
        f = urllib.request.urlopen(url)
        page = f.read().decode('utf-8')
        #googletag.pubads().setTargeting("tag", "punk,punkrock,british,70s,rock,classicrock,classicpunk,alternative,sexpistols,britishpunk");
        line = re.findall('googletag\.pubads\(\)\.setTargeting\("tag", "([^"]+)"\);', page)  #find all tag-words
        if not len(line):
            return
        tags = line[0].split(',')  #я не зрозуміла. перепояснити!!!
        for item in tags:
            genreid = insertGenreName(item)
            insertGenreBandMx(bandid, genreid)
    except:
        Error("can't grab band page %s for bandid=%s" % (url , bandid))


def insertGenreName(genrename):
    # Add Genre into dicgenre table and than Select id
    try:
        sql_session.add(Genre(genrename=genrename))
        sql_session.commit()

    except:
        sql_session.rollback()
    for genre in sql_session.query(Genre):
        if genrename==genre.genrename:
            return genre.genreid


def insertGenreBandMx(bandid, genreid):
    try:
        sql_session.add(BandAndGen(bandid=bandid,genreid=genreid))
        sql_session.commit()
    except:
        sql_session.rollback()
        #------------------------------------------------------------20th May


def insertListening(userid, songid, listeningdate):
    try:
        sql_session.add(Listening(userid=userid,songid=songid,listeningdate=listeningdate))
        sql_session.commit()
    except:
        sql_session.rollback()


def insertUser(url, username):
    f = urllib.request.urlopen(url)
    page = f.read().decode('utf-8')
    searchresult = re.search('<small>since ([\d]{1,2}[\s]+[a-zA-Z]+ [\d]{4,4})</small></span><p class="userActivity">', page)
    regdate = datetime.datetime.strptime(searchresult.group(1), "%d %b %Y")
    # Add User into userlist table and than Select id
    try:
        sql_session.add(User(username=username,regdate=regdate))
        sql_session.commit()
    except:
        sql_session.rollback()

    for user in sql_session.query(User):
        if username==user.username:
            return user.userid

    #-------------------------------------------------------21th May

def buildProfilePage(username):
    return ("http://www.last.fm/user/%s" % (username))
    #-------------------------------------------------------------
def grabPage(url, userid):
    f = urllib.request.urlopen(url)
    page = f.read().decode('utf-8')
    # print(page)
    # page = ''
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
        bandid = insertBandName(item[0])  #insert in db-dict
        grabBandPage(buildBandUrl(item[0]), bandid)
        songid = insertSongName(item[1], bandid)  #insert in db-dict
        insertListening(userid, songid, item[2])
    return nextpage

def buildHistoryUrl(username, page):
    return ("http://www.last.fm/user/%s/tracks?page=%s" % (username, page))

def grabUserPages(username):
    userid = insertUser(buildProfilePage(username),username)  # NEW!!!
    Info('Grabbing Pages for User %s' % username)
    nextpage = 1
    while nextpage != False:
        Info('Grabbing Page %s for User' % nextpage)
        nextpage = grabPage(buildHistoryUrl(username, nextpage), userid)

# <a href="/user/kakabomba/tracks?page=3" class="btn btn--icon-only btn--small btn--white iconright iconright--right" rel="next" title="Next page">Next</a>

#<a href="/music/Downlink/_/Triphekta"     class="recent-tracks-image media-pull-left media-link-hook"> 



grabUserPages('mine')  #THE FIRST STEP



#postges.d/postgres/minkovski
#-de pysaty nazvu db
#- jak dodaty foreignkey
