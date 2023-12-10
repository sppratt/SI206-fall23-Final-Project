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

def population_gather_data(cur, conn):
    create_population_table(cur, conn)
    cur.execute("SELECT city_name FROM cities ORDER BY city_id")
    data_list = cur.fetchall()
    new_list = []
    start = get_population_size(cur,conn)
    for i in range(start, start + 25):
        name = data_list[i][0]
        api_url = 'https://api.api-ninjas.com/v1/city?name={}'.format(name)
        response = requests.get(api_url, headers={'X-Api-Key': '33HglWdrhQ8+6vp3ggXWvQ==jLQS9WyZ4Fhyiq3L'})
        if response.status_code == requests.codes.ok:
            inner_list = []
            data = json.loads(response.text)
            for val in data[0].values():
                inner_list.append(val)
            new_list.append(inner_list)

        else:
            print("Error:", response.status_code, response.text)
    add_population_data(cur, conn, new_list)

def create_population_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS population (city_id INTEGER PRIMARY KEY, latitude FLOAT, longitude FLOAT, country_id INTEGER, population NUMERIC, is_capital BOOLEAN)")
    conn.commit()

def add_population_data(cur, conn, some_list):
    for i in range(25):
        city = some_list[i]
        city_name = city[0]
        if city_name == "Porto Alegre":
            city_name = "Porto"
        cur.execute("SELECT city_id FROM cities WHERE city_name=?", (city_name,))
        city_id = cur.fetchone()[0]
        latitude = city[1]
        longitude = city[2]
        cur.execute("SELECT country_id FROM quality WHERE city_id=?", (city_id,))
        country_id = cur.fetchone()[0]
        population = city[4]
        is_capital = city[5]
        cur.execute("INSERT OR IGNORE INTO population VALUES (?,?,?,?,?,?)", (city_id, latitude, longitude, country_id, population, is_capital))
    conn.commit()

def get_population_size(cur, conn):
    cur.execute("SELECT COUNT(*) FROM population")
    count = cur.fetchone()[0]
    return count

def main():
    cur, conn = setUpDatabase('cities.db')
    population_gather_data(cur, conn)

if __name__ == "__main__":
    main()