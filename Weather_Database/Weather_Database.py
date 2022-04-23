#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Importing dependencies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from citipy import citipy
from config import weather_api_key
import requests
import time
from datetime import datetime


# In[3]:


# Creating an array of sets of random Latitudes and Longitudes
lats = np.random.uniform(low=-90.000, high=90.000, size=2000)
lngs = np.random.uniform(low=-180.000, high=180.000, size=2000 )

# Pairing the latitudes and longitudes
latLngs = zip(lats,lngs)
latLngs


# In[4]:


# Adding the latitudes & longitudes to a list
coordinates = list(latLngs)


# In[5]:


# Creating list to hold cities
cities = []

# Looping through coordinates finding the nearest city
for coordinate in coordinates:
    city = citipy.nearest_city(coordinate[0], coordinate[1]).city_name

    # Checking to see if the city is unique. If so, it is added to the "cities" list.
    if city not in cities:
        cities.append(city)

# Checking how many cities we have
len(cities)


# In[8]:


# Creating the base URL
url = 'https://api.openweathermap.org/data/2.5/weather?units=Imperial&APPID=' + weather_api_key

# Creating an empty list to hold the weather data
cityData = []

# Printing the beginning  of the logging
print('Beginning Data Retrieval      ')
print('------------------------------')

# Creating counters
recordCount = 1
setCount = 1

# Looping through cities in 'cities' list
for i, city in enumerate(cities):
    # Grouping cities into sets of 50 for logging purposes
    if i % 50 == 0 and i >= 50:
        setCount += 1
        recordCount = 1
        time.sleep(60)

    # Creating endpoint URL with each city
    cityURL = url + '&q=' + city.replace(' ','+')

    # Logging the URL, Record and set numbers and the city.
    print(f'Processing Record {recordCount} of Set {setCount} | {city}')

    #Adding 1 to record count
    recordCount += 1

    # Making API request for each city
    try:
        # Parsing the JSON and retrieving the data
        cityWeather = requests.get(cityURL).json()

        # Parsing out the needed data
        cityLat = cityWeather['coord']['lat']
        cityLng = cityWeather['coord']['lon']
        cityMaxTemp = cityWeather['main']['temp_max']
        cityHumidity = cityWeather['main']['humidity']
        cityClouds = cityWeather['clouds']['all']
        cityWind = cityWeather['wind']['speed']
        cityCountry = cityWeather['sys']['country']
        cityDescription = cityWeather['weather'][0]['description']

        # Appending the city info into the cityData List
        cityData.append({'City': city.title(),
                         'Country': cityCountry,
                         'Lat':cityLat,
                         'Lng':cityLng,
                         'Max Temp':cityMaxTemp,
                         'Humidity':cityHumidity,
                         'Cloudiness':cityClouds,
                         'Wind Speed':cityWind,
                         'Current Description':cityDescription
                         })

    # If an error is experienced, skip the city.
    except:
        print('City not found. Skipping City...')
        pass

#Indicate that data loading is complete
print('--------------------------')
print('Data Retrieval Complete!')
print('--------------------------')


# In[9]:


# Checking the amount of cities we have
len(cityData)


# In[11]:


# Converting the array of dictionaries to a DataFrame
cityDataDf = pd.DataFrame(cityData)

cityDataDf.head()


# In[14]:


# Creating the output file
outputDataFile = 'WeatherPy_Database.csv'

# Exporting the cityData into a CSV
cityDataDf.to_csv(outputDataFile, index_label='City_ID')

