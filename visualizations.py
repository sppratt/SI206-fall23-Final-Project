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
from plotly.subplots import make_subplots
import plotly.graph_objects as go

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

        

def vis2(cur, conn):
    cur.execute("SELECT population.city_id, population.population, quality.quality, quality.safety, quality.traffic, quality.cost FROM population JOIN quality ON quality.city_id = population.city_id")
    results = cur.fetchall()
    df = pd.DataFrame(results, columns=['City_id', 'Population', 'Quality of Life', 'Safety', 'Traffic', 'Cost'])
    
    fig = make_subplots(rows=2, cols=2,
                    subplot_titles=['Quality of Life', 'Safety', 'Traffic', 'Cost'],
                    shared_xaxes=True, shared_yaxes=False,
                    horizontal_spacing=0.1, vertical_spacing=0.2)

    # Add scatter plots with trend lines to subplots
    fig.add_trace(go.Scatter(x=df['Population'], y=df['Quality of Life'], mode='markers', name='Quality of Life'),
                row=1, col=1)

    fig.add_trace(go.Scatter(x=df['Population'], y=df['Quality of Life'].rolling(window=5).mean(), mode='lines', name='Trendline'),
                row=1, col=1)

    fig.add_trace(go.Scatter(x=df['Population'], y=df['Safety'], mode='markers', name='Safety'),
                row=1, col=2)

    fig.add_trace(go.Scatter(x=df['Population'], y=df['Safety'].rolling(window=5).mean(), mode='lines', name='Trendline'),
                row=1, col=2)

    fig.add_trace(go.Scatter(x=df['Population'], y=df['Traffic'], mode='markers', name='Traffic'),
                row=2, col=1)

    fig.add_trace(go.Scatter(x=df['Population'], y=df['Traffic'].rolling(window=5).mean(), mode='lines', name='Trendline'),
                row=2, col=1)

    fig.add_trace(go.Scatter(x=df['Population'], y=df['Cost'], mode='markers', name='Cost'),
                row=2, col=2)

    fig.add_trace(go.Scatter(x=df['Population'], y=df['Cost'].rolling(window=5).mean(), mode='lines', name='Trendline'),
                row=2, col=2)

    # Update layout for better presentation
    fig.update_layout(title_text='Population vs. Quality of Life Factors')

    # Show the plot
    fig.show()


def vis3(cur, conn):
    results = calc2(cur, conn) 
    df = pd.DataFrame(results, columns=['country', 'avg_temp_f'])

    fig = px.bar(df, x='avg_temp_f', y='country', orientation='h',
             title='Average Temperature (°F) by Country',
             labels={'avg_temp_f': 'Average Temperature (°F)', 'country': 'Country'},
             template='plotly_white')

    fig.show()

def visualizations(cur, conn):
    vis1(cur, conn)
    vis2(cur, conn)
    vis3(cur, conn)
    

def main():
    cur, conn = setUpDatabase("cities.db")
    calculations(cur, conn)
    visualizations(cur,conn)

if __name__ == "__main__":
    main()

