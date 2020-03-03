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

today = datetime.date.today()-datetime.timedelta(days=1)
record=pd.read_csv(f'./agged-record-data/province-day-summary-{today}.csv')
record1=pd.pivot_table(record, values='confirmed', index='province',
                    columns='date')
record1['provinceName']=record1.index
record1.drop_duplicates(keep = 'first', inplace = True)


for i in [('Wuhan',30.52,114.31)]:
    geo_dict = dict()
    geo_dict1 = dict()
    with open('./support-data/chinacitylocation.csv',encoding='utf-8') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for row in f_csv:
            geo_dict[row[0]]=distance.distance((row[2],row[3]), (i[1],i[2])).kilometers

    with open('./support-data/china_coordinates.csv',encoding='utf-8') as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            geo_dict1[row[1]]=distance.distance((row[3],row[2]), (i[1],i[2])).kilometers
    dist=list()

    for index,row in record1.iterrows():
        if index in geo_dict.keys():
            dist.append(geo_dict[index])
        elif index in geo_dict1.keys():
            dist.append(geo_dict1[index])
        else:
            dist.append(np.nan)

    record1[f'distance-{i[0]}']=dist

record1.to_csv(f'./agged-record-data/province-pivot-day-summary-{today}.csv',index=0,encoding='utf-8-sig',sep=',')

