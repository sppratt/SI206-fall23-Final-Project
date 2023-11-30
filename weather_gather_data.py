# Names: Sami Pratt, Natalie Anderson, Mia Trotter
# Student IDs: 97430564, 14233024, 02196024
# Emails: sppratt@umich.edu, nateand@umich.edu, miatrot@umich.edu
# List any AI tool (e.g. ChatGPT, GitHub Copilot): 

# Final Project

# API #1: write at least one function in this file to gather data from the 
# APIs/website (using Beautiful Soup) and store it in a database

import requests

url = "https://us-weather-by-city.p.rapidapi.com/getweather"

# for loop 
# city = ""
# state = ""
querystring = {"city":"San Francisco","state":"CA"}

headers = {
	"X-RapidAPI-Key": "SIGN-UP-FOR-KEY",
	"X-RapidAPI-Host": "us-weather-by-city.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())