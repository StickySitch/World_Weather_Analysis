# World_Weather_Analysis

## Overview and Purpose
In order to help PlanMyTrip customers find an idle vacation spot, I have utilized the power of the ```gmaps``` API and ```citipy``` to offer travel locations based on customer preference. 

After generating 2000 latitudes and longitudes, ```citipy``` is used to gather cities around those coordinates. These cities are used to request weather data from the ```Open Weather Map API```. Using this weather data, we are able to take the customers prefered temperature range and display the desired locations using ```gmaps```; While also suggesting hotels! Lastly, a travel itinerary was created and routed using the ```Google Directions API```. This itinerary displayed, routes, markers and location information(City Name, Hotel Name, Weather description, Temperature)
