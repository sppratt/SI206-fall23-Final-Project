# Names: Sami Pratt, Natalie Anderson, Mia Trotter
# Student IDs: 97430564, 14233024, 02196024
# Emails: sppratt@umich.edu, nateand@umich.edu, miatrot@umich.edu
# List any AI tool (e.g. ChatGPT, GitHub Copilot): 

# Final Project

# API #1: write at least one function in this file to gather data from the 
# APIs/website (using Beautiful Soup) and store it in a database

import requests

pop_list = [['The Hague', 52.08, 4.27, 'NL', 1406000, True], ['Rotterdam', 51.92, 4.48, 'NL', 1005000, False], ['Luxembourg', 49.6106, 6.1328, 'LU', 122273, True], ['Vienna', 48.2083, 16.3731, 'AT', 1840573, True], ['Valencia', 10.1667, -68.0, 'VE', 1484430, False], ['Amsterdam', 52.35, 4.9166, 'NL', 1031000, True], ['Helsinki', 60.1756, 24.9342, 'FI', 642045, True], ['Madrid', 40.4189, -3.6919, 'ES', 3266126, True], ['Reykjavik', 64.1475, -21.935, 'IS', 128793, True], ['Copenhagen', 55.6786, 12.5635, 'DK', 1085000, True], ['Munich', 48.1372, 11.5755, 'DE', 1471508, False], ['Edinburgh', 55.953, -3.189, 'GB', 488050, False], ['Zurich', 47.3786, 8.54, 'CH', 434008, False], ['Porto Alegre', -30.0328, -51.23, 'BR', 1484941, False], ['Gothenburg', 57.6717, 11.981, 'SE', 600473, False], ['Oslo', 59.9111, 10.7528, 'NO', 693494, True], ['Muscat', 23.6139, 58.5922, 'OM', 1421409, True], ['Frankfurt', 50.1136, 8.6797, 'DE', 753056, False], ['Geneva', 46.2, 6.15, 'CH', 201818, False], ['Tallinn', 59.4372, 24.745, 'EE', 434562, True], ['Stuttgart', 48.7761, 9.1775, 'DE', 634830, False], ['Glasgow', 55.8609, -4.2514, 'GB', 985290, False], ['Hamburg', 53.55, 10.0, 'DE', 1841179, False], ['Cork', 51.9, -8.4731, 'IE', 208669, False], ['Abu Dhabi', 24.4781, 54.3686, 'AE', 1000000, True], ['Dubai', 25.2697, 55.3094, 'AE', 2502715, False], ['Tampa', 27.9942, -82.4451, 'US', 2908063, False], ['Orlando', 28.4772, -81.3369, 'US', 1822394, False], ['Raleigh', 35.8325, -78.6435, 'US', 1038738, False], ['San Antonio', 29.4658, -98.5253, 'US', 2049293, False], ['Charlotte', 35.208, -80.8304, 'US', 1512923, False], ['Austin', 30.3004, -97.7522, 'US', 1687311, False], ['Houston', 29.7863, -95.3889, 'US', 5464251, False], ['Ljubljana', 46.05, 14.5167, 'SI', 284355, True], ['Tokyo', 35.6897, 139.692, 'JP', 37977000, True], ['Columbus', 39.9862, -82.985, 'US', 1562009, False], ['Denver', 39.7621, -104.876, 'US', 2876625, False], ['Tucson', 32.1545, -110.878, 'US', 888486, False], ['Albuquerque', 35.1053, -106.646, 'US', 761195, False], ['Stockholm', 59.3294, 18.0686, 'SE', 972647, True], ['Vilnius', 54.6833, 25.2833, 'LT', 574147, True], ['Mississauga', 43.6, -79.65, 'CA', 721599, False], ['Boston', 42.3188, -71.0846, 'US', 4688346, False], ['Pittsburgh', 40.4396, -79.9762, 'US', 1703266, False], ['Dallas', 32.7936, -96.7662, 'US', 5743938, False], ['Kansas City', 39.1239, -94.5541, 'US', 1636715, False], ['Victoria', 48.4283, -123.365, 'CA', 335696, False], ['Portland', 45.5372, -122.65, 'US', 2074775, False], ['San Diego', 32.8312, -117.122, 'US', 3220118, False], ['San Jose', 37.3019, -121.849, 'US', 1798103, False], ['Brisbane', -27.4678, 153.028, 'AU', 2514184, False], ['Calgary', 51.05, -114.067, 'CA', 1239220, False], ['Halifax', 44.6475, -63.5906, 'CA', 403131, False], ['Seattle', 47.6211, -122.324, 'US', 3789215, False], ['Perth', -31.9522, 115.859, 'AU', 2059484, False], ['Salt Lake City', 40.7777, -111.931, 'US', 1098526, False], ['Atlanta', 33.7627, -84.4224, 'US', 5449398, False], ['Sacramento', 38.5667, -121.468, 'US', 1898019, False], ['Sydney', -33.865, 151.209, 'AU', 5312163, False], ['Wellington', -41.2889, 174.777, 'NZ', 418500, True], ['Melbourne', -37.8136, 144.963, 'AU', 5078193, False], ['Adelaide', -34.9289, 138.601, 'AU', 1345777, False], ['Minneapolis', 44.9635, -93.2678, 'US', 2977172, False], ['Vancouver', 49.25, -123.1, 'CA', 2264823, False], ['Canberra', -35.2931, 149.127, 'AU', 426704, True], ['Ottawa', 45.4247, -75.695, 'CA', 989567, False], ['Edmonton', 53.5344, -113.49, 'CA', 1062643, False], ['Auckland', -36.85, 174.783, 'NZ', 1467800, False], ['Washington', 38.9047, -77.0163, 'US', 5379184, True], ['Quebec City', 46.8139, -71.2081, 'CA', 705103, False], ['Berlin', 52.5167, 13.3833, 'DE', 3644826, True], ['Doha', 25.3, 51.5333, 'QA', 1312947, True], ['Montreal', 45.5089, -73.5617, 'CA', 3519595, False], ['Prague', 50.0833, 14.4167, 'CZ', 1324277, True], ['Bursa', 40.1833, 29.0667, 'TR', 2901396, False], ['Brno', 49.1953, 16.6083, 'CZ', 381346, False], ['Zagreb', 45.8, 15.95, 'HR', 790017, True], ['Chicago', 41.8373, -87.6862, 'US', 8604203, False], ['Phoenix', 33.5722, -112.089, 'US', 4219697, False], ['Singapore', 1.3, 103.8, 'SG', 5745000, True], ['Honolulu', 21.3294, -157.846, 'US', 820987, False], ['Philadelphia', 40.0077, -75.1339, 'US', 5649300, False], ['Birmingham', 52.48, -1.9025, 'GB', 2897303, False], ['Timisoara', 45.7597, 21.23, 'RO', 319279, False], ['Lisbon', 38.7452, -9.1604, 'PT', 506654, True], ['Manchester', 53.4794, -2.2453, 'GB', 2705000, False], ['Taipei', 25.0478, 121.532, 'TW', 2684567, True], ['Tel Aviv-Yafo', 32.0833, 34.8, 'IL', 451523, False], ['Miami', 25.7839, -80.2102, 'US', 6445545, False], ['Jeddah', 21.5428, 39.1728, 'SA', 3976000, False], ['Cluj-Napoca', 46.78, 23.5594, 'RO', 324576, False], ['Riyadh', 24.65, 46.71, 'SA', 6881000, True], ['Brussels', 50.8467, 4.3517, 'BE', 185103, True], ['Riga', 56.9475, 24.1069, 'LV', 698529, True], ['Toronto', 43.7417, -79.3733, 'CA', 5429524, False], ['Cape Town', -33.925, 18.425, 'ZA', 433688, True], ['Bratislava', 48.1447, 17.1128, 'SK', 429564, True], ['Limassol', 34.675, 33.0443, 'CY', 235056, False], ['Las Vegas', 36.2333, -115.265, 'US', 2104198, False], ['Bangalore', 12.9699, 77.598, 'IN', 13707000, False]]

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