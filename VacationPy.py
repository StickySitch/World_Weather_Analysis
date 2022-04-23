#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Importing dependencies
import  pandas as pd
import gmaps
import  requests

#import API key
#from config import g_key


# In[16]:


# Storing the cities.csv file
city_data_df = pd.read_csv('weather_data/cities.csv')
city_data_df.head()


# In[17]:


# Checking data types for DataFrame
city_data_df.dtypes


# In[18]:


# Configuring gmaps to use api key
gmaps.configure(api_key=g_key)


# In[35]:


# Heatmap of temperature
# Getting the lat and long
locations = city_data_df[['Lat', 'Lng']]
# Getting the maximum temperature
max_temp = city_data_df['Max Temp']

# Assigning figure variable
# Adding zoom level and center
fig = gmaps.figure(center=(30.0,31.0), zoom_level=1.5)

# Assigning the heatmap variable
heat_layer = gmaps.heatmap_layer(locations, 
                                 weights=[max(temp,0) for temp in max_temp],
                                 dissipating=False,
                                 max_intensity=300,
                                 point_radius=4)
# Adding the heatmap layer
fig.add_layer(heat_layer)



# Call the figure to plot the data
fig


# In[36]:


# Creating heatmap for % humidity
locations = city_data_df[['Lat','Lng']]
humidity = city_data_df['Humidity']
fig = gmaps.figure(center=(30.0,31.0), zoom_level=1.5)
heat_layer = gmaps.heatmap_layer(locations,
                                 weights=humidity,
                                 dissipating=False,
                                 max_intensity=300,
                                 point_radius=4)
fig.add_layer(heat_layer)
fig


# In[37]:


# Creating heatmap for % cloudiness
locations = city_data_df[['Lat','Lng']]
cloudiness = city_data_df['Cloudiness']
fig = gmaps.figure(center=(30.0,31.0), zoom_level=1.5)
heat_layer = gmaps.heatmap_layer(locations,
                                 weights=cloudiness,
                                 dissipating=False,
                                 max_intensity=300,
                                 point_radius=4)
fig.add_layer(heat_layer)
fig


# In[39]:


# Creating heatmap for Wind Speed
locations = city_data_df[['Lat','Lng']]
wind_speed = city_data_df['Wind Speed']
fig = gmaps.figure(center=(30.0,31.0), zoom_level=1.5)
heat_layer = gmaps.heatmap_layer(locations,
                                 weights=wind_speed,
                                 dissipating=False,
                                 max_intensity=300,
                                 point_radius=4)
fig.add_layer(heat_layer)
fig


# In[44]:


# Asking customer the temperature range
min_temps = float(input('What is the minimum temperature you would like for your trip?'))
max_temps = float(input('What is the maximum temperature you would like for your trip?'))


# In[47]:


pref_cities_df = city_data_df.loc[(city_data_df['Max Temp'] <= max_temps) & (city_data_df['Max Temp'] >= min_temps)]
pref_cities_df.head()


# In[55]:


# Checking for null values
pref_cities_df.isnull().sum()


# In[56]:


#Creating hotel map DataFrame
hotel_df = pref_cities_df[['City','Country', 'Max Temp','Lat','Lng']]
hotel_df['Hotel Name'] = ''
hotel_df.head()


# In[62]:


# Setting search parameters for hotels
params = {
    'radius':5000,
    'type':'lodging',
    'key':g_key
}

# Iterating through the DataFrame
for index, row in hotel_df.iterrows():
    # Getting the Lat and Long
    lat = row['Lat']
    lng = row['Lng']

    #Adding the lat and lng to the location key for the params dict
    params['location'] = f'{lat},{lng}'

    # Using the search term: lodging and our lat and long
    base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    #Making request
    hotels = requests.get(base_url,params=params).json()

    #Grabbing the first hotel from the results and storing the name
    try:
        hotel_df.loc[index, 'Hotel Name'] = hotels['results'][0]['name']
    except (IndexError):
        print('Hotel not found... skipping.')


# In[63]:


hotel_df.head(10)


# In[67]:


info_box_template = """
<dl>
<dt>Hotel Name</dt><dd>{Hotel Name}</dd>
<dt>City</dt><dd>{City}</dd>
<dt>Country</dt><dd>{Country}</dd>
<dt>Max Temp</dt><dd>{Max Temp} °F</dd>
</dl>
"""

# Storing the dataframe row
hotel_info = [info_box_template.format(**row) for index, row in hotel_df.iterrows()]


# In[69]:


# Adding a heatmap of temperature for the vacation spots.
locations = hotel_df[['Lat','Lng']]
max_temp = hotel_df['Max Temp']
fig = gmaps.figure(center=(30.0,31.0), zoom_level=1.5)
heat_layer = gmaps.heatmap_layer(locations,
                                 weights=max_temp,
                                 dissipating=False,
                                 max_intensity=300,
                                 point_radius=4)
marker_layer = gmaps.marker_layer(locations, info_box_content=hotel_info)

fig.add_layer(heat_layer)
fig.add_layer(marker_layer)
fig


# In[ ]:




