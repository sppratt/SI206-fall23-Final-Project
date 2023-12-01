# Names: Sami Pratt, Natalie Anderson, Mia Trotter
# Student IDs: 97430564, 14233024, 02196024
# Emails: sppratt@umich.edu, nateand@umich.edu, miatrot@umich.edu
# List any AI tool (e.g. ChatGPT, GitHub Copilot): 

# Final Project

# API #3: write at least one function in this file to gather data from the 
# APIs/website (using Beautiful Soup) and store it in a database


import requests

name = 'San Francisco'
api_url = 'https://api.api-ninjas.com/v1/city?name={}'.format(name)
response = requests.get(api_url, headers={'X-Api-Key': 'M5VM2aS8wMwsYdOCutO3dQ==76LK9aFKvZksa0IC'})
if response.status_code == requests.codes.ok:
    print(response.text)
else:
    print("Error:", response.status_code, response.text)