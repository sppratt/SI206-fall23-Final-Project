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
import pandas as pd
import numpy as np
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
    list1 = calc1(cur, conn)
    list2 = calc2(cur, conn)
    avg_safety, avg_safety10 = calc3(cur, conn)

    with open('calculation_results.txt', 'w') as f:
        f.write('Quality of Life Index per Capita\n\n')
        f.write("City: Quality of Life Index per Capita\n")
        for line in list1:
            f.write(f"{line[0]}: {line[1]}\n")

        f.write("\n-----------------------------\n\n")
        f.write("Average Temperature per Country\n\n")
        f.write("Country: Average Temperature ºF\n")
        for line in list2:
            f.write(f"{line[0]}: {line[1]}\n")
        f.write("\n-----------------------------\n\n")
        f.write("Average Safety Index of All Cities vs. Average Safety Index of Ten Most Populated Cities\n\n")
        f.write(f"All Cities: {avg_safety}\nTen Most Populated: {avg_safety10}")
    
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
    df = pd.DataFrame(results, columns=['City_id', 'Population', 'Quality of Life', 'Safety', 'Traffic Commute Time', 'Cost of Living'])

    fig = make_subplots(rows=2, cols=2,
                    subplot_titles=['Quality of Life', 'Safety', 'Traffic Commute Time', 'Cost of Living'],
                    shared_xaxes=False, shared_yaxes=False,
                    horizontal_spacing=0.1, vertical_spacing=0.2)

    fig.add_trace(go.Scatter(x=df['Population'], y=df['Quality of Life'], mode='markers', name='Quality of Life'),
                row=1, col=1)

    fig.add_trace(go.Scatter(x=df['Population'], y=np.polyval(np.polyfit(df['Population'], df['Quality of Life'], 1), df['Population']),
                mode='lines', name='Trendline'),
                row=1, col=1)

    fig.add_trace(go.Scatter(x=df['Population'], y=df['Safety'], mode='markers', name='Safety'),
                row=1, col=2)

    fig.add_trace(go.Scatter(x=df['Population'], y=np.polyval(np.polyfit(df['Population'], df['Safety'], 1), df['Population']),
                mode='lines', name='Trendline'),
                row=1, col=2)

    fig.add_trace(go.Scatter(x=df['Population'], y=df['Traffic Commute Time'], mode='markers', name='Traffic Commute Time'),
                row=2, col=1)

    fig.add_trace(go.Scatter(x=df['Population'], y=np.polyval(np.polyfit(df['Population'], df['Traffic Commute Time'], 1), df['Population']),
                mode='lines', name='Trendline'),
                row=2, col=1)

    fig.add_trace(go.Scatter(x=df['Population'], y=df['Cost of Living'], mode='markers', name='Cost of Living'),
                row=2, col=2)

    fig.add_trace(go.Scatter(x=df['Population'], y=np.polyval(np.polyfit(df['Population'], df['Cost of Living'], 1), df['Population']),
                mode='lines', name='Trendline'),
                row=2, col=2)

    fig.update_layout(
        title_text='Population vs. Quality of Life Factors',
    )

    fig.update_xaxes(title_text='Population', row=1, col=1)
    fig.update_yaxes(title_text='Quality of Life Index', row=1, col=1)

    fig.update_xaxes(title_text='Population', row=1, col=2)
    fig.update_yaxes(title_text='Safety Index', row=1, col=2)

    fig.update_xaxes(title_text='Population', row=2, col=1)
    fig.update_yaxes(title_text='Traffic Commute Time Index', row=2, col=1)

    fig.update_xaxes(title_text='Population', row=2, col=2)
    fig.update_yaxes(title_text='Cost of Living Index', row=2, col=2)

    fig.show()


def vis3(cur, conn):
    results = calc2(cur, conn) 
    df = pd.DataFrame(results, columns=['country', 'avg_temp_f'])

    fig = px.bar(df, x='avg_temp_f', y='country', orientation='h',
             title='Average Temperature (°F) by Country',
             labels={'avg_temp_f': 'Average Temperature (°F)', 'country': 'Country'},
             template='plotly_white')

    fig.show()

def vis2_0(cur, conn):
    cur.execute("SELECT population.city_id, population.population, quality.quality, quality.safety, quality.traffic, quality.cost FROM population JOIN quality ON quality.city_id = population.city_id WHERE quality.city_id != 34 AND quality.city_id != 99")
    results = cur.fetchall()
    df = pd.DataFrame(results, columns=['City_id', 'Population', 'Quality of Life', 'Safety', 'Traffic Commute Time', 'Cost of Living'])

    fig = make_subplots(rows=2, cols=2,
                    subplot_titles=['Quality of Life', 'Safety', 'Traffic Commute Time', 'Cost of Living'],
                    shared_xaxes=False, shared_yaxes=False,
                    horizontal_spacing=0.1, vertical_spacing=0.2)

    fig.add_trace(go.Scatter(x=df['Population'], y=df['Quality of Life'], mode='markers', name='Quality of Life'),
                row=1, col=1)

    fig.add_trace(go.Scatter(x=df['Population'], y=np.polyval(np.polyfit(df['Population'], df['Quality of Life'], 1), df['Population']),
                mode='lines', name='Trendline'),
                row=1, col=1)

    fig.add_trace(go.Scatter(x=df['Population'], y=df['Safety'], mode='markers', name='Safety'),
                row=1, col=2)

    fig.add_trace(go.Scatter(x=df['Population'], y=np.polyval(np.polyfit(df['Population'], df['Safety'], 1), df['Population']),
                mode='lines', name='Trendline'),
                row=1, col=2)

    fig.add_trace(go.Scatter(x=df['Population'], y=df['Traffic Commute Time'], mode='markers', name='Traffic Commute Time'),
                row=2, col=1)

    fig.add_trace(go.Scatter(x=df['Population'], y=np.polyval(np.polyfit(df['Population'], df['Traffic Commute Time'], 1), df['Population']),
                mode='lines', name='Trendline'),
                row=2, col=1)

    fig.add_trace(go.Scatter(x=df['Population'], y=df['Cost of Living'], mode='markers', name='Cost of Living'),
                row=2, col=2)

    fig.add_trace(go.Scatter(x=df['Population'], y=np.polyval(np.polyfit(df['Population'], df['Cost of Living'], 1), df['Population']),
                mode='lines', name='Trendline'),
                row=2, col=2)

    fig.update_layout(
        title_text='Population vs. Quality of Life Factors',
    )

    fig.update_xaxes(title_text='Population', row=1, col=1)
    fig.update_yaxes(title_text='Quality of Life Index', row=1, col=1)

    fig.update_xaxes(title_text='Population', row=1, col=2)
    fig.update_yaxes(title_text='Safety Index', row=1, col=2)

    fig.update_xaxes(title_text='Population', row=2, col=1)
    fig.update_yaxes(title_text='Traffic Commute Time Index', row=2, col=1)

    fig.update_xaxes(title_text='Population', row=2, col=2)
    fig.update_yaxes(title_text='Cost of Living Index', row=2, col=2)

    fig.show()

def visualizations(cur, conn):
    vis1(cur, conn)
    vis2(cur, conn)
    vis2_0(cur, conn)
    vis3(cur, conn)
    
def main():
    cur, conn = setUpDatabase("cities.db")
    calculations(cur, conn)
    visualizations(cur,conn)

if __name__ == "__main__":
    main()

