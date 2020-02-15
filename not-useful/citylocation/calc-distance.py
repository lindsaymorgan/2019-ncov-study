import csv
from geopy import distance
import pandas as pd
import numpy as np

# approximate radius of earth in km
#
#['Wuhan', '30.52', '114.31']
geo=pd.read_csv('china_coordinates.csv')
dist=list()
with open('china_coordinates.csv',encoding='utf-8') as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        try:
            d=round(distance.distance((row[3],row[2]), (30.5810841269207,114.316200102681)).kilometers)
            dist.append(d)
        except:
            dist.append(np.nan)
geo['distance']=dist
geo.to_csv('china_coordinates.csv',index=0)

