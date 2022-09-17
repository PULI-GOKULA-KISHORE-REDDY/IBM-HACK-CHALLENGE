import os
import pandas as pd
import requests
import json
from datetime import date

pf=pd.read_csv('https://raw.githubusercontent.com/PULI-GOKULA-KISHORE-REDDY/IBM-HACK-CHALLENGE/main/files/datasets/allindia_cities.csv')
pf=pf.dropna()
pf['SO2']=0.0
pf['NO2']=0.0
pf['O3']=0.0
pf['PM2.5']=0.0
pf['PM10']=0.0
pf['CO']=0.0
pf['Date']=''
def get_data(pin,lat,lon):
    global pf, c
    pin=int(pin)
    print(pin,lat,lon)
    url = "https://air-quality-by-api-ninjas.p.rapidapi.com/v1/airquality"

    querystring = {"lat":lat,"lon": lon}
    headers = {
      "X-RapidAPI-Key": "4f7bb14128msh9b291ceae57c2d4p12b8b5jsn9580099f1b46",
      "X-RapidAPI-Host": "air-quality-by-api-ninjas.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data=response.text
    data=json.loads(data)
    pf.loc[pf["postal_code"] == pin, "Date"] =  date.today()
    pf.loc[pf["postal_code"] == pin, "PM10"] = data["PM10"]['concentration']
    pf.loc[pf["postal_code"] == pin, "PM2.5"] = data["PM2.5"]['concentration'] 
    pf.loc[pf["postal_code"] == pin, "CO"] =  data["CO"]['concentration']
    pf.loc[pf["postal_code"] == pin, "SO2"] =  data["SO2"]['concentration']
    pf.loc[pf["postal_code"] == pin, "O3"] = data["O3"]['concentration']
    pf.loc[pf["postal_code"] == pin, "N02"] = data["NO2"]['concentration'] 
    pf.loc[pf["postal_code"] == pin, "AQI"] = data['overall_aqi']
    """
    # https://api.weatherbit.io/v2.0/history/daily?postal_code=27601&country=US&start_date=2022-09-12&end_date=2022-09-13&key=API_KEY
    url='https://api.weatherbit.io/v2.0/current/airquality?&lat='+str(lat)+'&lon='+str(lon)+'&key=f0defabbf503444c8e4892c942e3f0d1'
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)
    d=json.loads(response.text) 

    update = pd.DataFrame({'postal_code' : int(pin) ,'AQI':d['data'][0]['aqi'] ,'PM10':d['data'][0]['pm10'], 'PM2.5': d['data'][0]['pm25'] , 'CO': d['data'][0]['co'], 'SO2': d['data'][0]['so2'], 'O3': d['data'][0]['o3'],'NO2':d['data'][0]['no2'] }, index=[0])
    pf.loc[pf.postal_code == pin].update(update)"""

pf=pf.iloc[50001:100001] 
pf=pf[['postal_code','latitude','longitude']].apply(lambda x : get_data(*x),axis=1)
pf.to_csv("latest_aqi_reports1.csv")