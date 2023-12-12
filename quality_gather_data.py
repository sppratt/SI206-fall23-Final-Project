# Names: Sami Pratt, Natalie Anderson, Mia Trotter
# Student IDs: 97430564, 14233024, 02196024
# Emails: sppratt@umich.edu, nateand@umich.edu, miatrot@umich.edu

# Final Project

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

def quality_gather_data(url, cur, conn):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        data_list = []

        table = soup.find('table', {'id': 't2'})

        rows = table.find_all('tr')
        id = 0
        for row in range(1,len(rows)):
            row = rows[row]
            
            cols = row.find_all('td')
            match = re.findall( r"(.*),\s(.*)", cols[1].text)
            city = match[0][0]
            country = match[0][1]
            if country == "United States":
                match = re.findall("(.*),\s(.*)", city)
                city = match[0][0]
            if '(' in city:
                match = re.findall(r'^([^(:]+)', city)
                city = match[0].strip()
            quality = float(cols[2].text)
            safety = float(cols[4].text)
            cost = float(cols[6].text)
            traffic = float(cols[8].text)
            data_list.append([id,city,country,quality,safety,cost,traffic])
            id+=1
            if id == 100:
                break

        create_cities_table(cur, conn)
        add_cities(cur, conn, data_list)
        create_quality_table(cur, conn)
        create_countries_table(cur, conn)
        add_countries(cur, conn, data_list)
        add_quality_data(cur, conn, data_list)

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

def create_cities_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS cities (city_id INTEGER PRIMARY KEY, city_name TEXT)")
    conn.commit()

def add_cities(cur, conn, some_list):
    start = get_cities_size(cur,conn)
    for i in range(start, start + 25):
        city_name = some_list[i][1]
        cur.execute("INSERT OR IGNORE INTO cities VALUES (?,?)", (i, city_name))
    conn.commit()

def get_cities_size(cur, conn):
    cur.execute("SELECT COUNT(*) FROM cities")
    count = cur.fetchone()[0]
    return count

def create_countries_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS countries (country_id INTEGER PRIMARY KEY, country_name TEXT)")
    conn.commit()

def add_countries(cur, conn, quality_list):
    country_id = get_countries_size(cur,conn)
    start = get_quality_size(cur, conn)
    for i in range(start,start + 25):
        country_name = quality_list[i][2]

        cur.execute("SELECT country_id FROM countries WHERE country_name=?", (country_name,))
        existing_country_id = cur.fetchone()

        if existing_country_id is None:
            cur.execute("INSERT OR IGNORE INTO countries VALUES (?, ?)", (country_id, country_name))
            country_id += 1
    conn.commit()

def get_countries_size(cur, conn):
    cur.execute("SELECT COUNT(*) FROM countries")
    count = cur.fetchone()[0]
    return count
    
def get_quality_size(cur, conn):
    cur.execute("SELECT COUNT(*) FROM quality")
    count = cur.fetchone()[0]
    return count

def create_quality_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS quality (city_id INTEGER PRIMARY KEY, country_id INTEGER, quality FLOAT, safety FLOAT, cost FLOAT, traffic FLOAT)")
    conn.commit()

def add_quality_data(cur, conn, some_list):
    start = get_quality_size(cur, conn)
    for i in range(start,start + 25):
        city = some_list[i]
        city_name = city[1]
        cur.execute("SELECT city_id FROM cities WHERE city_name=?", (city_name,))
        city_id = cur.fetchone()[0]
        country = city[2]
        cur.execute("SELECT country_id FROM countries WHERE country_name=?", (country,))
        country_id = cur.fetchone()[0]
        quality = city[3]
        safety = city[4]
        cost = city[5]
        traffic = city[6]
        cur.execute("INSERT OR IGNORE INTO quality VALUES (?,?,?,?,?,?)", (city_id, country_id, quality, safety, cost, traffic))
    conn.commit()

def main():
    cur, conn = setUpDatabase('cities.db')
    url = 'https://www.numbeo.com/quality-of-life/rankings.jsp'
    quality_gather_data(url, cur, conn)

if __name__ == "__main__":
    main()