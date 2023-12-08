# Names: Sami Pratt, Natalie Anderson, Mia Trotter
# Student IDs: 97430564, 14233024, 02196024 
# Emails: sppratt@umich.edu, nateand@umich.edu, miatrot@umich.edu
# List any AI tool (e.g. ChatGPT, GitHub Copilot): 

# Final Project

# select data from the database and perform calculations and visualize the results

#plot locations on map (lat vs long)
#plot temp vs quality of life (cross weather and quality databases)
#temp vs rank (city id)
#population vs. quality of life, safety, traffic, cost

# quality of life index per capita by dividing the quality of life by population (join quality and population)
# can do that with all of the indexes in quality table

import requests
import json
from bs4 import BeautifulSoup
import re
import os
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
import plotly.express as px

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def calc1(cur, conn):

    cur.execute("SELECT cities.city_name, quality.quality / population.population FROM quality JOIN population ON quality.city_id = population.city_id JOIN cities ON cities.city_id = quality.city_id")
    results = cur.fetchall()
    return results

def calc2(cur, conn):
    cur.execute("SELECT countries.country_name, AVG(weather.temp_f) FROM weather JOIN population ON weather.city_id = population.city_id JOIN countries ON population.country_id = countries.country_id GROUP BY population.country_id")
    results = cur.fetchall()
    return results

def calc3(cur, conn):
    cur.execute("SELECT AVG(safety) FROM quality")
    avg_safety = cur.fetchall()[0][0]
    cur.execute("SELECT quality.safety FROM quality JOIN population ON quality.city_id = population.city_id ORDER BY population.population DESC LIMIT 10")
    avg_safety10 = cur.fetchall()
    total = 0
    for city in avg_safety10:
        total += city[0]
    avg_safety10 = total/10
    return avg_safety, avg_safety10
    

def calculations(cur, conn):
    calc1(cur, conn)
    calc2(cur, conn)
    calc3(cur, conn)

    # list1 = calc #1
    # list2 = calc #2
    # list3 = calc #3...

    # write to text file
    pass

def vis1(cur, conn):
    cur.execute("SELECT cities.city_name, population.latitude, population.longitude FROM population JOIN cities ON cities.city_id = population.city_id;")
    results = cur.fetchall()

    df = pd.DataFrame(results, columns=['City', 'Latitude', 'Longitude'])

    fig = px.scatter_geo(df,
                     lat='Latitude',
                     lon='Longitude',
                     text='City',
                     hover_name='City',
                     size_max=50) 

    fig.show()

        

def vis2():
    # do something
    pass


def vis3():
    # do something
    pass

def visualizations(cur, conn):
    vis1(cur, conn)
    pass

def main():
    cur, conn = setUpDatabase("cities.db")
    calculations(cur, conn)
    visualizations(cur,conn)

if __name__ == "__main__":
    main()

