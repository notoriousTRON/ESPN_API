import os
os.chdir('P:\Projects\ESPN_API\modules')
import crds
import psycopg2 as ps

usr = crds.get_usr()
pwd = crds.get_pwd()

def open_connection():
    db = ps.connect(database="smokehouse", user=usr, password=pwd, host="127.0.0.1",port="5432")
    return db
	
def k():
	k= crds.get_k()
	return k

def swid():
	swid = crds.get_swid()
	return swid