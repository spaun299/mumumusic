from db_connect import *
from print_info import *
import datetime
import urllib.request
import re
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