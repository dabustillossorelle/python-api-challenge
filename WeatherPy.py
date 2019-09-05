#!/usr/bin/env python
# coding: utf-8

# # WeatherPy
# ----
# 
# #### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time

# Import API key
from api_keys import api_key

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# Output File (CSV)
output_data_file = "output_data/cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)


# ## Generate Cities List

# In[2]:


# List for holding lat_lngs and cities
lat_lngs = []
cities = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(low=-90.000, high=90.000, size=1500)
lngs = np.random.uniform(low=-180.000, high=180.000, size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
len(cities)


# ### Perform API Calls
# * Perform a weather check on each city using a series of successive API calls.
# * Include a print log of each city as it'sbeing processed (with the city number and city name).
# 

# In[3]:


api_key=api_key
url = "http://api.openweathermap.org/data/2.5/weather?units=Imperial&APPID=" + api_key
city_name = []
cloudiness = []
country = []
date = []
humidity = []
lat = []
lng = []
max_temp = []
wind_speed = []
record = 1
print(f"Beginning Data Retrieval")
print(f"________________________")

for city in cities:
    try: 
        response = requests.get(f"{url}&q={city}").json() 
        city_name.append(response["name"])
        cloudiness.append(response["clouds"]["all"])
        country.append(response["sys"]["country"])
        date.append(response["dt"])
        humidity.append(response["main"]["humidity"])
        max_temp.append(response["main"]["temp_max"])
        lat.append(response["coord"]["lat"])
        lng.append(response["coord"]["lon"])
        wind_speed.append(response["wind"]["speed"])
        city_record = response["name"]
        print(f"Processing Record {record} | {city_record}")
        print(f"{url}&q={city}")
        
        record= record + 1
        time.sleep(1.01)
    except:
        print("Skipping City...")
    
    continue


# ### Convert Raw Data to DataFrame
# * Export the city data into a .csv.
# * Display the DataFrame

# In[4]:


city_weather = {
    "City": city_name,
    "Cloud Cover":cloudiness,
    "Country":country, 
    "Date":date, 
    "Humidity":humidity,
    "Latitude": lat, 
    "Longitude":lng, 
    "Highest Temperature":max_temp,
    "Wind Speed":wind_speed
}


# In[5]:


city_weather_df=pd.DataFrame(city_weather)
city_weather_df.head()


# In[6]:


print(city_weather_df.dtypes)


# In[7]:


city_weather_df['Date']=pd.to_datetime(city_weather_df['Date'], unit='s')
city_weather_df.head()


# In[8]:


city_weather_df.to_csv('city_weather_df.csv')


# ### Plotting the Data
# * Use proper labeling of the plots using plot titles (including date of analysis) and axes labels.
# * Save the plotted figures as .pngs.

# #### Latitude vs. Temperature Plot

# In[12]:


plt.scatter(city_weather_df ["Latitude"], city_weather_df ["Highest Temperature"], marker="o", s=10)
plt.title("Latitudes of Cities vs Temperature in Cities (September 4, 2019)")
plt.ylabel("Highest Temperature (Farenheit)")
plt.xlabel("Latitude")
plt.grid(True)


# In[17]:


plt.savefig("Lat_vs_Temp.png")


# #### Latitude vs. Humidity Plot

# In[14]:


plt.scatter(city_weather_df ["Latitude"], city_weather_df ["Humidity"], marker="o", s=10, c='r')
plt.title("Latitudes of Cities vs Humidity in Cities (September 4, 2019)")
plt.ylabel("Humidity")
plt.xlabel("Latitude")
plt.grid(True)


# In[18]:


plt.savefig("Lat_vs_Humid.png")


# #### Latitude vs. Cloudiness Plot

# In[15]:


plt.scatter(city_weather_df ["Latitude"], city_weather_df ["Cloud Cover"], marker="o", s=10, c='g')
plt.title("Latitudes of Cities vs Cloud Cover in Cities (September 4, 2019)")
plt.ylabel("Cloud Cover")
plt.xlabel("Latitude")
plt.grid(True)


# In[19]:


plt.savefig("Lat_vs_Cloud.png")


# #### Latitude vs. Wind Speed Plot

# In[16]:


plt.scatter(city_weather_df ["Latitude"], city_weather_df ["Wind Speed"], marker="o", s=10, c='y')
plt.title("Latitudes of Cities vs Wind Speed in Cities (September 4, 2019)")
plt.ylabel("Wind Speed")
plt.xlabel("Latitude")
plt.grid(True)


# In[20]:


plt.savefig("Lat_vs_Wind.png")


# In[ ]:




