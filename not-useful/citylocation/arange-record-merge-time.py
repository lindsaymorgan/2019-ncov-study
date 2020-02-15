import pandas as pd
import csv
import numpy as np
from xpinyin import Pinyin
from geopy import distance

p = Pinyin()



geo=pd.read_csv('china_coordinates.csv')

record=pd.read_csv('city-day-summary-2020-02-12.csv')
record1=pd.pivot_table(record, values='city_confirmedCount', index='cityName',
                    columns='updateTime')
record1['cityName-ch']=record1.index

record1['cityName'] = record1.apply(lambda row: p.get_pinyin(f"{row['cityName-ch']}", "").capitalize(), axis = 1)

for i in [('Wuhan',30.52,114.31),('Xiaogan',31.92,113.91),('Huanggang',30.44,114.87),('Suizhou',31.7178576081886,113.379358364292),('Jingzhou',30.332590522986,112.241865807191)]:
    geo_dict = dict()
    geo_dict1 = dict()
    with open('chinacitylocation.csv',encoding='utf-8') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for row in f_csv:
            geo_dict[row[0]]=distance.distance((row[2],row[3]), (i[1],i[2])).kilometers

    with open('china_coordinates.csv',encoding='utf-8') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for row in f_csv:
            geo_dict1[row[1][:-1]]=distance.distance((row[3],row[2]), (i[1],i[2])).kilometers


    # record1=pd.read_csv('city-pivot-day-summary-2020-02-11.csv')
    dist=list()
    for index,row in record1.iterrows():
        if index in geo_dict.keys():
            dist.append(geo_dict[index])
        elif index in geo_dict1.keys():
            dist.append(geo_dict1[index])
        else:
            dist.append(np.nan)

    record1[f'distance-{i[0]}']=dist
record1.to_csv('city-pivot-day-summary-2020-02-12.csv',index=0,encoding='utf-8-sig',sep=',')