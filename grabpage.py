import urllib.request
import re
import pprint
import psycopg2

pp = pprint.PrettyPrinter(indent=4)



#def insertSongName(songname):
#    try:
#        conn = psycopg2.connect("dbname='MusicGenreMigration' user='postgres' host='postgres.d' password='minkovski'")
#    except:
#        print "I am unable to connect to the database"
#    cur = conn.cursor()
#    cur.execute("""INSERT INTO DicSong(SongName) VALUES (songname)""") 

def insertBandName(bandname):
#    try:
    conn = psycopg2.connect("dbname='MusicGenreMigration' user='postgres' host='postgres.d' password='minkovski'")
#    except
#print "I am unable to connect to the database"
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO dicband(bandname) VALUES ('%s')" % (bandname,))
    except:
        print("INSERT INTO dicband(bandname) VALUES ('%s')" % (bandname,))
    conn.commit()
    cur.execute("SELECT bandid FROM dicband WHERE bandname = '%s'" % (bandname,))
    row = cur.fetchall()
    return row[0][0]
    
    


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
#------new
  massive = []
  dictionary = {}
  line = re.findall('<a href="/music/([^/]+)/_/([^/]+)"\s+class="recent-tracks-image media-pull-left media-link-hook">.*? datetime="([\d\-:TZ]+)"', page, re.S)
  pp.pprint(line)
  for item in line:
      dictionary['song']= item[0]
      dictionary['author'] = item[1]
      dictionary['time'] = item[2]
     # insertSongName(item[0])        #insert in db-dict
      insertBandName(item[1])        #insert in db-dict
      massive.append(dictionary)
  
  return nextpage, [], massive

  

      
# <a href="/user/kakabomba/tracks?page=3" class="btn btn--icon-only btn--small btn--white iconright iconright--right" rel="next" title="Next page">Next</a>
  
#<a href="/music/Downlink/_/Triphekta"     class="recent-tracks-image media-pull-left media-link-hook"> 

def buildUrl(page):
  return "http://www.last.fm/user/kakabomba/tracks?page=2"

grabPage(buildUrl(2))


#postges.d/postgres/minkovski
#-de pysaty nazvu db
#- jak dodaty foreignkey
