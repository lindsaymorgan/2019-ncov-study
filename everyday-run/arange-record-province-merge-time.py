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
record=pd.read_csv(f'/mnt/data/Lindsay/2019-ncov/program/dxy-data/nice-dxy-data/province-day-summary-{today}.csv')
record1=pd.pivot_table(record, values='province_confirmedCount', index='provinceName',
                    columns='updateTime')
record1['provinceName']=record1.index
record1.drop_duplicates(keep = 'first', inplace = True)

record1=record1.ffill(axis=1)

record1.to_csv(f'/mnt/data/Lindsay/2019-ncov/program/dxy-data/nice-dxy-data/province-pivot-day-summary-{today}.csv',index=0,encoding='utf-8-sig',sep=',')

