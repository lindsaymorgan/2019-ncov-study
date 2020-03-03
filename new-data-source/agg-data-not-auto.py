import pandas as pd
import powerlaw
from geopy import distance
import numpy as np
import datetime
import csv
import urllib
import pypinyin

def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s

today = datetime.date.today()
yesterday=today-datetime.timedelta(days=1)
former=yesterday-datetime.timedelta(days=1)
urllib.request.urlretrieve("https://raw.githubusercontent.com/canghailan/Wuhan-2019-nCoV/master/Wuhan-2019-nCoV.csv", f"./agged-record-data/new-rawdata-{today}.csv")
raw_data=pd.read_csv(f'./agged-record-data/new-rawdata-{today}.csv')
raw_data['date'] = pd.to_datetime(raw_data['date'])
raw_data['date'] = raw_data['date'].dt.date
raw_data=raw_data[(raw_data['date']<datetime.date.today())] # & (raw_data['date']>=yesterday)

#国家级数据
raw_data1=raw_data[raw_data.isnull()['province']]
raw_data1.drop(columns=['province','provinceCode','city','cityCode'],inplace=True)
raw_data1.to_csv(f'./agged-record-data/country-day-summary-{yesterday}.csv', index=0, encoding='utf-8-sig', sep=',')

#省级数据
raw_data2=raw_data[(~raw_data.isnull()['province']) & (raw_data.isnull()['city'])]
raw_data2.drop(columns=['provinceCode','city','cityCode'],inplace=True)
raw_data2.to_csv(f'./agged-record-data/province-day-summary-{yesterday}.csv', index=0, encoding='utf-8-sig', sep=',')

#市级数据
raw_data2=raw_data2[raw_data2['province'].isin(['北京市','上海市','重庆市','天津市'])]
raw_data2['city']=raw_data2['province']
raw_data3=raw_data[(~raw_data.isnull()['province']) & (~raw_data.isnull()['city']) & (~raw_data['province'].isin(['北京市','上海市','重庆市','天津市']))]
raw_data3.drop(columns=['provinceCode','cityCode'],inplace=True)
raw_data3=pd.concat([raw_data2,raw_data3]).reset_index(drop=True)
raw_data3.sort_values(by=['city','date'],inplace=True)
raw_data3=raw_data3[raw_data3['confirmed']!=0]
raw_data3.to_csv(f'./agged-record-data/city-day-summary-{yesterday}.csv', index=0, encoding='utf-8-sig', sep=',')

#市级数据清洗转pivot
for index, row in raw_data3.iterrows():
    if row['city']in ['兴安盟乌兰浩特']:
        raw_data3.at[index, 'city'] = np.nan
    if len(row['city']) > 2  and row['city'][-1] in ['县', '市', '盟']:
        raw_data3.at[index, 'city'] = row['city'][:-1]
    # elif len(row['city']) > 2 and row['city'][-1] == '州' and row['city'][-3:] != '自治州':
    #     raw_data3.at[index, 'city'] = row['city'][:-1]
    elif row['city'][-3:] in ['管委会','示范区']:
        raw_data3.at[index, 'city'] = row['city'][:-3]
    elif row['city'][-2:] == '地区':
        raw_data3.at[index, 'city'] = row['city'][:-2]
    # elif row['city'][-1] in ['区','旗']:
    #     raw_data3.at[index, 'city'] = np.nan

    if row['city'][0] in ['待', '未', '外','第','所']:
        raw_data3.at[index, 'city'] = np.nan
raw_data4=pd.pivot_table(raw_data3, values='confirmed', index='city', aggfunc=np.max, columns='date')
raw_data4=raw_data4[raw_data4[yesterday]!=0]
raw_data4.dropna(how='all',inplace=True)
raw_data4['cityName']=raw_data4.index
raw_data4['cityName-en'] =raw_data4.apply(lambda row: pinyin(f'{row["cityName"]}').capitalize(), axis = 1)

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
        for row in f_csv:
            geo_dict1[row[1][:-1]]=distance.distance((row[3],row[2]), (i[1],i[2])).kilometers
            geo_dict1[row[1]] = distance.distance((row[3], row[2]), (i[1], i[2])).kilometers


    # record1=pd.read_csv('city-pivot-day-summary-2020-02-11.csv')
    dist=list()
    for index,row in raw_data4.iterrows():
        if index in geo_dict.keys():
            dist.append(geo_dict[index])
        elif index in geo_dict1.keys():
            dist.append(geo_dict1[index])
        else:
            dist.append(np.nan)

    raw_data4[f'distance-{i[0]}']=dist
raw_data4.drop_duplicates(keep = 'first', inplace = True)
raw_data4.drop(columns=[datetime.date(2019,12,1)+datetime.timedelta(days=i) for i in range((datetime.date(2020,1,23)-datetime.date(2019,12,1)).days)],inplace=True)
raw_data4.to_csv(f'./agged-record-data/city-confirmed-pivot-day-summary-{yesterday}.csv',index=0,encoding='utf-8-sig',sep=',')

raw_data3['city_D']=[a+b for a,b in zip(raw_data3['dead'],raw_data3['cured'])]
raw_data5=pd.pivot_table(raw_data3, values='city_D', index='city',
                    columns='date')
raw_data5['cityName']=raw_data5.index

raw_data5['cityName-en'] = raw_data5.apply(lambda row: pinyin(f'{row["cityName"]}').capitalize(), axis = 1)

raw_data5.drop_duplicates(keep = 'first', inplace = True)
# record1=record1.ffill(axis=1)
raw_data5.to_csv(f'./agged-record-data/city-D-pivot-day-summary-{yesterday}.csv',index=0,encoding='utf-8-sig',sep=',')
