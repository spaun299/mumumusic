from sqlalchemy import MetaData,create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
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




#postges.d/postgres/minkovski