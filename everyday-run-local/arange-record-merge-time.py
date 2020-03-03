import pandas as pd
import csv
import numpy as np
from xpinyin import Pinyin
from geopy import distance
import datetime
import pypinyin

def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s

# geo=pd.read_csv('./support-data/china_coordinates.csv')

today = datetime.date.today()-datetime.timedelta(days=1)
record=pd.read_csv(f'./agged-record-data/city-day-summary-{today}.csv')
record1=pd.pivot_table(record, values='city_confirmedCount', index='cityName',
                    columns='updateTime')
record1['cityName']=record1.index

record1['cityName-en'] = record1.apply(lambda row: pinyin(f'{row["cityName"]}').capitalize(), axis = 1)

for i in [('Wuhan',30.52,114.31),('Xiaogan',31.92,113.91),('Huanggang',30.44,114.87),('Suizhou',31.7178576081886,113.379358364292),('Jingzhou',30.332590522986,112.241865807191)]:
    geo_dict = dict()
    geo_dict1 = dict()
    with open('./support-data/chinacitylocation.csv',encoding='utf-8') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for row in f_csv:
            geo_dict[row[0]]=distance.distance((row[2],row[3]), (i[1],i[2])).kilometers

    with open('./support-data/china_coordinates.csv',encoding='utf-8') as f:
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

record1=pd.merge(record1,record.loc[:,['cityName','provinceName']],how='left',on = 'cityName')
record1.drop_duplicates(keep = 'first', inplace = True)
# record1=record1.ffill(axis=1)
record1.to_csv(f'./agged-record-data/city-pivot-day-summary-{today}.csv',index=0,encoding='utf-8-sig',sep=',')


record['city_D']=[a+b for a,b in zip(record['city_deadCount'],record['city_curedCount'])]
record2=pd.pivot_table(record, values='city_D', index='cityName',
                    columns='updateTime')
record2['cityName']=record2.index

record2['cityName-en'] = record2.apply(lambda row: pinyin(f'{row["cityName"]}').capitalize(), axis = 1)

record2=pd.merge(record2,record.loc[:,['cityName','provinceName']],how='left',on = 'cityName')
record2.drop_duplicates(keep = 'first', inplace = True)
# record1=record1.ffill(axis=1)
record2.to_csv(f'./agged-record-data/city-D-pivot-day-summary-{today}.csv',index=0,encoding='utf-8-sig',sep=',')