import pandas as pd
import powerlaw
import matplotlib.pyplot as plt
import numpy as np

# pro_data=pd.read_csv('province-day-summary-2020-02-11.csv')
# country_data=pd.read_csv('country-day-summary-2020-02-11.csv')
city_data=pd.read_csv('all-city-day-summary-new.csv')
# pro_data['updateTime'] = pd.to_datetime(pro_data['updateTime'])
# country_data['updateTime'] = pd.to_datetime(country_data['updateTime'])

#
# country_data['country_confirmedCount_increase']=country_data["country_confirmedCount"]-country_data["country_confirmedCount"].shift(1)
# country_data['country_curedCount_increase']=country_data["country_curedCount"]-country_data["country_curedCount"].shift(1)
# country_data.to_csv('country-day-summary-2020-02-11.csv',index=0)
#
#
# pro_data['province_confirmedCount_increase'] = pro_data.groupby('provinceName')['province_confirmedCount'].diff(1)
# pro_data['province_curedCount_increase'] = pro_data.groupby('provinceName')['province_curedCount'].diff(1)
# pro_data.to_csv('province-day-summary-2020-02-11.csv',index=0)

city_data['city_confirmedCount_increase'] = city_data.groupby('cityName')['city_confirmedCount'].diff(1)

city_data.to_csv('all-city-day-summary-new.csv',index=0)