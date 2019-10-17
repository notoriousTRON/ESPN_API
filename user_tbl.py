import os
os.chdir('P:\Projects\ESPN_API\modules')
import requests
import pandas as pd
import psycopg2 as ps
import open_connection
import references


def drop_table(tbl_name):
    db = open_connection.open_connection()
    cursor = db.cursor()
    drop = "DROP TABLE IF EXISTS "+tbl_name
    cursor.execute(drop)
    db.commit()
    cursor.close()
    db.close()
    return

def refresh_user_data(user_year_id, year, display_name, user_id, first, last, name):
    db = open_connection.open_connection()
    cursor = db.cursor()
    insert_query = """INSERT INTO users_tbl(user_year_id, year, display_name, user_id, first, last, name) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(insert_query, (user_year_id, year, display_name, user_id, first, last, name))
    db.commit()
    cursor.close()
    db.close()
    return

def refresh_team_data(user_year_id, user_id, abbrev, team_id, team_name):
    db = open_connection.open_connection()
    cursor = db.cursor()
    insert_query = """INSERT INTO team_tbl(user_year_id, user_id, abbrev, team_id, team_name) 
                        VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(insert_query, (user_year_id, user_id, abbrev, team_id, team_name))
    db.commit()
    cursor.close()
    db.close()
    return

league_id = references.league_id()
year = 2019
#url = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/"+str(year)+"/segments/0/leagues/"+str(league_id)
url = "http://fantasy.espn.com/apis/v3/games/ffl/seasons/"+str(year)+"/segments/0/leagues/"+str(league_id)+"?&view=mTeam"

k = open_connection.k()
swid = open_connection.swid()
cookies = {"swid": swid,"espn_s2": k}

r = requests.get(url,cookies=cookies )
d = r.json()

'''
drop_table("users_tbl")
user_create = """
CREATE TABLE users_tbl
    (
    user_year_id character(255),
    year character(255),
    display_name character(255),
    user_id character(255),
    first character(255),
    last character(255),
    name character(255),
    
    primary key(user_year_id)
    )
    """
drop_table("team_tbl")
team_create = """
CREATE TABLE team_tbl
    (
    user_year_id character(255),
    user_id character(255),
    abbrev character(4),
    team_id character(2),
    team_name character(255),

    primary key(user_year_id)
    )
    """
db = open_connection.open_connection()
cursor = db.cursor()
cursor.execute(user_create)
cursor.execute(team_create)
db.commit()
cursor.close()
db.close()
'''

for i in range(0,len(d['teams'])):
    abbrev = d['teams'][i]['abbrev']
    team_id = d['teams'][i]['id']
    location = d['teams'][i]['location']
    nickname = d['teams'][i]['nickname']
    user_id = d['teams'][i]['owners'][0].strip('{}')
    team_name = str(location)+' '+str(nickname)
    user_year_id = str(year)+str(user_id)
    
    refresh_team_data(user_year_id, user_id, abbrev, team_id, team_name)

for i in range(0,len(d['members'])):
    first = d['members'][i]['firstName']
    last = d['members'][i]['lastName']
    name = first+' '+last
    display_name = d['members'][i]['displayName']
    user_id = d['members'][i]['id'].strip('{}')
    user_year_id = str(year)+str(user_id)
    
    refresh_user_data(user_year_id, year, display_name, user_id, first, last, name)