import urllib.request
import re
import pprint
import psycopg2

pp = pprint.PrettyPrinter(indent=4)
DEBUG = False

conn = psycopg2.connect("dbname='MusicGenreMigration' user='postgres' host='postgres.d' password='minkovski'") #connection to db
cur = conn.cursor()

def Debug(s):
    #pp.pprint(s)
    pass
    
def insertSongName(songname, bandid):
    try:
        cur.execute("INSERT INTO dicsong(songname, bandid) VALUES ('%s', '%s')" % (songname, bandid, ))
        conn.commit()
    except:
        conn.rollback()
    cur.execute("SELECT songid FROM dicsong WHERE songname = '%s' AND bandid = '%s'" % (songname,bandid))
    songid = cur.fetchall()
    return songid[0][0]

def insertBandName(bandname):
    try:
        cur.execute("INSERT INTO dicband(bandname) VALUES ('%s')" % (bandname,))
        conn.commit()
    except:
        conn.rollback()
    #print("INSERT INTO dicband(bandname) VALUES ('%s')" % (bandname,))
    #conn.commit()
    cur.execute("SELECT bandid FROM dicband WHERE bandname = '%s'" % (bandname,))
    bandid = cur.fetchall()
    return bandid[0][0]
#--------------------------------------------------------------------18 May-------
def buildBandUrl(bandname):
    return ("http://www.last.fm/music/%s" % (bandname))

def grabBandPage(url, bandid):
  f = urllib.request.urlopen(url)
  page = f.read().decode('utf-8')
  line = re.findall('googletag.pubads().setTargeting("tag", "([^"]+)");', page) #find all tag-words
  tags = line[0][1].split(',')  #я не зрозуміла. перепояснити!!!
  for item in tags:
      genreid = insertGenreName(item)
      insertGenreBandMx(bandid, genreid)

def insertGenreName(genrename):
     try:
        cur.execute("INSERT INTO dicgenre(genrename) VALUES ('%s')" % (genrename,))
        conn.commit()
    except:
        conn.rollback()
        cur.execute("SELECT genreid FROM dicgenre WHERE genrename = '%s'" % (genrename,))
    genreid = cur.fetchall()
    return genreid[0][0]

def insertGenreBandMx(bandid, genreid):
    try:
        cur.execute("INSERT INTO bandgenremx(bandid, genreid) VALUES ('%s', '%s')" % (bandid, genreid, ))
        conn.commit()
    except:
        conn.rollback()
  #------------------------------------------------------------
def grabPage(url):
  f = urllib.request.urlopen(url)
  page = f.read().decode('utf-8')
# print(page)
# page = ''
  searchresult = re.search('page=(\d+)[^>]*Next page', page)
  Debug(searchresult)                                                             #go away
  if searchresult:
    nextpage = searchresult.group(1)
  else:
    nextpage = False
  massive = []
  dictionary = {}
  line = re.findall('<a href="/music/([^/]+)/_/([^/]+)"\s+class="recent-tracks-image media-pull-left media-link-hook">.*? datetime="([\d\-:TZ]+)"', page, re.S)
  Debug(line)
  for item in line:
      bandid = insertBandName(item[1])        #insert in db-dict
      grabBandPage(buildBandUrl(item[1]), bandid)
      songid = insertSongName(item[0], bandid)        #insert in db-dict

  
  return nextpage

def buildHistoryUrl(username, page):
  return ("http://www.last.fm/user/%s/tracks?page=%s" % (username, page))

def grabUserPages(username):
    print('Grabbing Pages for User %s' % username)
    nextpage = 1
    while nextpage != False:
        print('Grabbing Page %s for User' % nextpage)
        nextpage = grabPage(buildHistoryUrl(username, nextpage))

# <a href="/user/kakabomba/tracks?page=3" class="btn btn--icon-only btn--small btn--white iconright iconright--right" rel="next" title="Next page">Next</a>
  
#<a href="/music/Downlink/_/Triphekta"     class="recent-tracks-image media-pull-left media-link-hook"> 



grabUserPages('kakabomba')  #THE FIRST STEP

conn.commit() #end db-connection  

#postges.d/postgres/minkovski
#-de pysaty nazvu db
#- jak dodaty foreignkey
