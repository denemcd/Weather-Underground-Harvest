# Weather Underground Harvest

A Python script for harvesting data for a specific weather station from the Weather Underground API, and saving to a HTML file. Useful for if you want to create a local view of your data.

## Setup

You will need: 
1. A weather underground API key available here: https://www.wunderground.com/member/api-keys
2. The Station ID for the station you want to harvest, eg IDUNEDIN70

Save these details in the config.json file. Within the config.json file you can also specify the units you want returned, m = metric and e = imperial (English).

The data is output to a file named current_observations.html
