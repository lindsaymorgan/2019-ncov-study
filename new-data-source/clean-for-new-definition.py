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

# today = datetime.date.today()
today=datetime.date(2020,3,2)
yesterday=today-datetime.timedelta(days=1)
former=yesterday-datetime.timedelta(days=1)

raw_data3=pd.read_csv(f'./agged-record-data/city-day-summary-{yesterday}.csv')
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

raw_data3['city_D']=[c-a-b for a,b,c in zip(raw_data3['dead'],raw_data3['cured'],raw_data3['confirmed'])]
raw_data5=pd.pivot_table(raw_data3, values='city_D', index='city',
                    columns='date')
raw_data5['cityName']=raw_data5.index

raw_data5['cityName-en'] = raw_data5.apply(lambda row: pinyin(f'{row["cityName"]}').capitalize(), axis = 1)

raw_data5.drop_duplicates(keep = 'first', inplace = True)
# record1=record1.ffill(axis=1)
raw_data5.to_csv(f'./agged-record-data/city-I-D-pivot-day-summary-{yesterday}.csv',index=0,encoding='utf-8-sig',sep=',')
