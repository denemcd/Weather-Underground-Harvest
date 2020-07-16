import requests
import json

# Set Default Values
weatherreadings = {}
url = "https://api.weather.com/v2/pws/observations/current?stationId=REPLACESTATIONID&format=json&units=REPLACEUNITS&numericPrecision=decimal&apiKey=REPLACEAPI"
units = "m" # for imperial units change to e

# Get Config Data from config.json
configuration = open("config.json")
config = json.load(configuration)
configuration.close()
apikey = config["apikey"]
stationid = config["stationid"]
units = config["units"] # If you require imperial change this in the config file to
if units == "m":
    unitfull = "Metric"
if units == "e":
    untilfull = "Imperial"

# Build URL
url = url.replace("REPLACESTATIONID", stationid)
url = url.replace("REPLACEAPI", apikey)
url = url.replace("REPLACEUNITS", units)

# Get the JSON data from Weather Underground
print("Retrieving data from: " + url)
response = requests.get(url) # need to add error handling for invalid data

if response.status_code == 200: # If the response code is 200 (sucessful)
    print("Success")
    weatherdata = response.json()

    # Convert the data into a dict

    for key in weatherdata["observations"][0]:
        if (key != "metric") and (key != "imperial"):  # Don't take the Metric or Imperial at this stage as it nests a dict within a dict
            weatherreadings.update([(key, weatherdata["observations"][0][key])])

    if units == "m": # Grab the Metric or Imperial now
        for key in weatherdata["observations"][0]["metric"]:
            weatherreadings.update([(key, weatherdata["observations"][0]["metric"][key])])
    elif units == "e":
        for key in weatherdata["observations"][0]["imperial"]:
            weatherreadings.update([(key, weatherdata["observations"][0]["imperial"][key])])

    # Output the data to an HTML File
    print("Writing to file")
    f = open("current_observations.html", "w")
    f.write('<!DOCTYPE html>\n<html lang="en">\n<head>\n')
    f.write("<title>Weather Py</title>\n")
    f.write(
        '<link rel="stylesheet" hrf="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">\n')
    f.write("</head>\n<body>\n")
    f.write("<h1>" + weatherreadings["neighborhood"] + "</h1>\n")  # Write the station name as the header
    f.write('<table class="table">')
    for key in weatherreadings:
        f.write("<tr><td><b>" + key + ": </b></td><td>" + str(
            weatherreadings[key]) + "</td></tr>\n")  # Insert the individual key and value
    f.write("<tr><td><b>units</b></td><td>" + unitfull + "</td></tr>\n")
    f.write("</table>\n")
    f.write("</body>\n</html>")
    f.close()
    print("Sucessfully saved API data from " + url)

elif response.status_code == 204: # 204 returns a blank response so inform the user
    print("API Error 204: No Data Found for specific query.")
    exit()

elif response.status_code >200 & response.status_code <1000: # Handles all other error code numbers
    result = response.json()
    try:
        print("API Error " + str(response.status_code) + ": " + result["errors"][0]["error"]["message"])
    except: # sometimesthe error messae is in a different nest
        print("API Error " + str(response.status_code) + ": " + result["errors"][0]["message"])
    exit()

else: # Catch any other errors
    print("Unspecified error")
    print(response.text)
