# Names: Sami Pratt, Natalie Anderson, Mia Trotter
# Student IDs: 97430564, 14233024, 02196024
# Emails: sppratt@umich.edu, nateand@umich.edu, miatrot@umich.edu
# List any AI tool (e.g. ChatGPT, GitHub Copilot): 

# Final Project

# API #2: write at least one function in this file to gather data from the 
# APIs/website (using Beautiful Soup) and store it in a database
#city_id, city, state, country, quality_of_life_index, safety_index, cost_index, traffic_commute
import requests
from bs4 import BeautifulSoup
import re

def quality_gather_data(url):
    #make request to URL
    response = requests.get(url)
    #check if request was successful
    if response.status_code == 200:
        #parse HTML content of page
        soup = BeautifulSoup(response.content, 'html.parser')
        #begin extracting information


        data_list = []
        # for i in range(100):
        
        table = soup.find_all('table', class_="stripe row-border order-column compact dataTable no-footer")
        print(table)
        body = table.find('tbody')
        rows = body.find_all('tr')
        id = 0
        for row in rows:
            cols = row.find_all('td')
            match = re.findall( r"(.*),\s(.*)", cols[1].text)
            city = match[0][0]
            country = match[0][1]
            if country == "United States":
                match = re.findall("(.*),\s(.*)", city)
                city = match[0][0]
            
            quality = int(cols[2].text)
            safety = int(cols[4].text)
            cost = int(cols[6].text)
            traffic = int(cols[8].text)
            data_list.append([id,city,country,quality,safety,cost,traffic])
            id+=1
            if id == 100:
                break

        print(len(data_list))
        print(data_list)
        


    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")


#test run
url = 'https://www.numbeo.com/quality-of-life/rankings.jsp'
quality_gather_data(url)
