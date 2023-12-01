# Names: Sami Pratt, Natalie Anderson, Mia Trotter
# Student IDs: 97430564, 14233024, 02196024
# Emails: sppratt@umich.edu, nateand@umich.edu, miatrot@umich.edu
# List any AI tool (e.g. ChatGPT, GitHub Copilot): 

# Final Project

# API #1: write at least one function in this file to gather data from the 
# APIs/website (using Beautiful Soup) and store it in a database

import requests

def get_data():

	url = "https://weatherapi-com.p.rapidapi.com/current.json"

	# for loop thru latitude and longtidue from population table
	querystring = {"q":"48.4283,-123.365"}

	headers = {
		"X-RapidAPI-Key": "150d0e020bmshe7e191a3e33bedap11d3d3jsn94fe99a7f050",
		"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
	}

	response = requests.get(url, headers=headers, params=querystring)

	print(response.json())

def main():
	get_data()

if __name__ == "__main__":
    main()