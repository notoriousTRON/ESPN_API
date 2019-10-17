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

def add_matchup_row(matchup_rost_key,year,week,matchup_id,roster_id,points):
    db = open_connection.open_connection()
    cursor = db.cursor()
    insert_query = """INSERT INTO matchups_tbl(matchup_rost_key,year,week,matchup_id,roster_id,points) 
                        VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(insert_query, (matchup_rost_key,year,week,matchup_id,roster_id,points))
    db.commit()
    cursor.close()
    db.close()
    return

league_id = references.league_id()
year = 2019
#url = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/"+str(year)+"/segments/0/leagues/"+str(league_id)
url = "http://fantasy.espn.com/apis/v3/games/ffl/seasons/"+str(year)+"/segments/0/leagues/"+str(league_id)+"?&view=&view=mMatchupScore"

k = open_connection.k()
swid = open_connection.swid()
cookies = {"swid": swid,"espn_s2": k}

r = requests.get(url,cookies=cookies )
d = r.json()

#'''
drop_table("matchups_tbl")
matchup_create = """
CREATE TABLE matchups_tbl
    (
    matchup_rost_key character(255),
    year character(4),
    week character(2),
    matchup_id character(2),
    roster_id character(2),
    points character(255),
    
    primary key(matchup_rost_key)
    )
    """
db = open_connection.open_connection()
cursor = db.cursor()
cursor.execute(matchup_create)
db.commit()
cursor.close()
db.close()
#'''
matchup_id = 1
week_check = 1
for i in range(0,len(d['schedule'])):
    week = d['schedule'][i]['matchupPeriodId']
    
    if week == week_check:
        away_roster_id = d['schedule'][i]['away']['teamId']
        away_points = d['schedule'][i]['away']['totalPoints']
        if len(str(week))<2:
            wk = '0'+str(week)
        else:
            wk = str(week)
        if len(str(matchup_id))<2:
            m_id = '0'+str(matchup_id)
        else:
            m_id = str(matchup_id)
        if len(str(away_roster_id))<2:
            r_id = '0'+str(away_roster_id)
        else:
            r_id = str(away_roster_id)
        matchup_rost_key_away = str(year)+wk+m_id+r_id

        add_matchup_row(matchup_rost_key_away,year,week,matchup_id,away_roster_id,away_points)

        home_roster_id = d['schedule'][i]['home']['teamId']
        home_points = d['schedule'][i]['home']['totalPoints']

        if len(str(home_roster_id))<2:
            r_id = '0'+str(home_roster_id)
        else:
            r_id = str(home_roster_id)
        matchup_rost_key_home = str(year)+wk+m_id+r_id

        add_matchup_row(matchup_rost_key_home,year,week,matchup_id,home_roster_id,home_points)
        matchup_id += 1
    
    else:
        matchup_id = 1
        week_check = d['schedule'][i]['matchupPeriodId']
        away_roster_id = d['schedule'][i]['away']['teamId']
        away_points = d['schedule'][i]['away']['totalPoints']
        if len(str(week))<2:
            wk = '0'+str(week)
        else:
            wk = str(week)
        if len(str(matchup_id))<2:
            m_id = '0'+str(matchup_id)
        else:
            m_id = str(matchup_id)
        if len(str(away_roster_id))<2:
            r_id = '0'+str(away_roster_id)
        else:
            r_id = str(away_roster_id)
        matchup_rost_key_away = str(year)+wk+m_id+r_id

        add_matchup_row(matchup_rost_key_away,year,week,matchup_id,away_roster_id,away_points)

        home_roster_id = d['schedule'][i]['home']['teamId']
        home_points = d['schedule'][i]['home']['totalPoints']

        if len(str(home_roster_id))<2:
            r_id = '0'+str(home_roster_id)
        else:
            r_id = str(home_roster_id)
        matchup_rost_key_home = str(year)+wk+m_id+r_id

        add_matchup_row(matchup_rost_key_home,year,week,matchup_id,home_roster_id,home_points)
        matchup_id += 1
