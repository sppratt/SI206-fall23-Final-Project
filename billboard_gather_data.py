# Names: Sami Pratt, Natalie Anderson, Mia Trotter
# Student IDs: 97430564, 14233024, 02196024
# Emails: sppratt@umich.edu, nateand@umich.edu, miatrot@umich.edu
# List any AI tool (e.g. ChatGPT, GitHub Copilot): 

# Final Project

# API #1: write at least one function in this file to gather data from the 
# APIs/website (using Beautiful Soup) and store it in a database

import requests

url = "https://billboard-api2.p.rapidapi.com/artist-100"

querystring = {"date":"2019-05-11","range":"1-10"}

headers = {
	"X-RapidAPI-Key": "SIGN-UP-FOR-KEY",
	"X-RapidAPI-Host": "billboard-api2.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())