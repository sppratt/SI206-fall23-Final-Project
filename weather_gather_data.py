# Names: Sami Pratt, Natalie Anderson, Mia Trotter
# Student IDs: 97430564, 14233024, 02196024 
# Emails: sppratt@umich.edu, nateand@umich.edu, miatrot@umich.edu

import requests
import json
from bs4 import BeautifulSoup
import re
import os
import matplotlib.pyplot as plt
import sqlite3

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def weather_gather_data(cur, conn):
    create_weather_table(cur, conn)
     
    cur.execute("SELECT latitude, longitude FROM population ORDER BY city_id")
    data_list = cur.fetchall()
    url = "https://weatherapi-com.p.rapidapi.com/current.json"
    weather_list = []
    print(data_list)
    start = get_weather_size(cur,conn)
    print(start)
    for i in range(start, start + 25):
        city = data_list[i]
        lat = city[0]
        long = city[1]
        querystring = {"q":f"{lat},{long}"}
        headers = {
            "X-RapidAPI-Key": "150d0e020bmshe7e191a3e33bedap11d3d3jsn94fe99a7f050",
			"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
		}
        response = requests.get(url, headers=headers, params=querystring)

        data = response.json()
        inner_list = []
        city = data["location"]["name"]
        temp_f = data["current"]["temp_f"]
        feelslike_f = data["current"]["feelslike_f"]
        wind_mph = data["current"]["wind_mph"]
        inner_list = [city, temp_f, feelslike_f, wind_mph]
        weather_list.append(inner_list)

    add_weather_data(cur, conn, weather_list)

    print(weather_list)

def create_weather_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS weather (city_id INTEGER PRIMARY KEY, temp_f FLOAT, feelslike_f FLOAT, wind_mph FLOAT)")
    conn.commit()

def add_weather_data(cur, conn, some_list):
    for i in range(25):
        city = some_list[i]
        city_id = get_weather_size(cur, conn)
        
        temp_f = city[1]
        feelslike_f = city[2]
        wind_mph = city[3]
        cur.execute("INSERT OR IGNORE INTO weather VALUES (?,?,?,?)", (city_id, temp_f, feelslike_f, wind_mph))
    conn.commit()

def get_weather_size(cur, conn):
    cur.execute("SELECT COUNT(*) FROM weather")
    count = cur.fetchone()[0]
    return count

def main():
    cur, conn = setUpDatabase('cities.db')
    weather_gather_data(cur, conn)

if __name__ == "__main__":
    main()