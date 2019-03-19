import csv
import json
import requests
import os

#using this to suppress FutureWarning about a new pandas version axis concatenation issue
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# ============================
#scrape data from datausa CHR dataset

host = 'http://api.datausa.io/api/'

required_params = "?show=geo&sumlevel=county"
optional_params = ""
columns = "&required=diabetes&year=latest"
url = host + required_params + optional_params + columns

response = requests.request('GET', url)
#print(response)

# parse the JSON data into a python dictionary
diabetes = response.json()

# display the result in an easy-to-read format
data = [dict(zip(diabetes["headers"], d)) for d in diabetes["data"]]

#write the data in a csv file 'diabetes.csv'
fieldnames = diabetes["headers"]

with open("diabetes.csv", "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames)
    writer.writeheader()
    for row in data:
        writer.writerow(row)

#choropleth visualization using geopandas
import plotly as py
import plotly.figure_factory as ff
import numpy as np
import pandas as pd

df = pd.read_csv('diabetes.csv')

#mutate geo header to fips id for counties
fips = [g[-5:] for g in df.geo]

#changing diabetes value to percentage
values = df['diabetes']*100
values = values.tolist()

#defining a colorscale from Viridis
colorscale= ["#f7fbff","#ebf3fb","#deebf7","#d2e3f3","#c6dbef","#b3d2e9","#9ecae1",
              "#85bcdb","#6baed6","#57a0ce","#4292c6","#3082be","#2171b5","#1361a9",
              "#08519c","#0b4083","#08306b"]

#creating endpoints between min and max values of diabetes percentage
endpts = list(np.linspace(int(min(values)), int(max(values)), len(colorscale)-1 ))

#create map
fig = ff.create_choropleth(fips=fips, values=values, colorscale= colorscale, binning_endpoints=endpts, legend_title='Diabetes% by county', title='USA-2017 DIABETES data')
py.offline.plot(fig)
