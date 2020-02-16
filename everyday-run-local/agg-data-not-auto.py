import pandas as pd
import powerlaw
import matplotlib.pyplot as plt
import numpy as np
import datetime
import re

today = datetime.date.today()
yesterday=today-datetime.timedelta(days=1)
raw_data=pd.read_csv('../rawdata_2020_2_16.csv')
raw_data['updateTime'] = pd.to_datetime(raw_data['updateTime'])
raw_data=raw_data[(raw_data['updateTime']<datetime.date.today())]

raw_data1 = pd.pivot_table(raw_data, index=[raw_data['updateTime'].dt.date, 'provinceName'], values=['province_confirmedCount', 'province_suspectedCount', 'province_curedCount'], aggfunc=np.max)
raw_data1=pd.DataFrame(raw_data1.to_records())
raw_data3= pd.pivot_table(raw_data1, index=raw_data1['updateTime'], values=['province_confirmedCount', 'province_suspectedCount', 'province_curedCount'], aggfunc=np.sum)
raw_data3=raw_data3.rename(columns={'province_confirmedCount':'country_confirmedCount','province_curedCount':'country_curedCount','province_suspectedCount':'country_suspectedCount'})
raw_data3=pd.DataFrame(raw_data3.to_records())

raw_data1.to_csv(f'province-day-summary-{yesterday}.csv',index=0)
raw_data3.to_csv(f'country-day-summary-{yesterday}.csv',index=0)

raw_data2=raw_data1[(raw_data1['provinceName']=='北京市') | (raw_data1['provinceName']=='上海市') | (raw_data1['provinceName']=='重庆市') | (raw_data1['provinceName']=='天津市')]
city=raw_data2.rename(columns={'province_confirmedCount':'city_confirmedCount','province_curedCount':'city_curedCount','province_suspectedCount':'city_suspectedCount'})
city['cityName']=city['provinceName']
raw_data=raw_data[(raw_data['provinceName']!='北京市') & (raw_data['provinceName']!='上海市') & (raw_data['provinceName']!='重庆市') & (raw_data['provinceName']!='天津市')]
raw_data2 = pd.pivot_table(raw_data, index=[raw_data['updateTime'].dt.date, 'cityName'], values=['provinceName','city_confirmedCount', 'city_suspectedCount', 'city_curedCount'], aggfunc=np.max)
raw_data2=pd.DataFrame(raw_data2.to_records())
raw_data2 = pd.concat([raw_data2,city]).reset_index(drop=True)

for index, row in raw_data2.iterrows():
    if len(row['cityName']) > 2  and row['cityName'][-1] in ['县', '市', '盟']:
        raw_data2.at[index, 'cityName'] = row['cityName'][:-1]
    elif len(row['cityName']) > 2 and row['cityName'][-1] == '州' and row['cityName'][-3:] != '自治州':
        raw_data2.at[index, 'cityName'] = row['cityName'][:-1]
    elif row['cityName'][-3:] == '管委会':
        raw_data2.at[index, 'cityName'] = row['cityName'][:-3]
    elif row['cityName'][-2:] == '地区':
        raw_data2.at[index, 'cityName'] = row['cityName'][:-2]
    elif row['cityName'][-1] in ['区','旗']:
        raw_data2.at[index, 'cityName'] = np.nan

    if row['cityName'][0] in ['待', '未', '外','第'] or '兵团' in row['cityName']:
        raw_data2.at[index, 'cityName'] = np.nan

    #处理括号
    if '（' in row['cityName']:
        s= re.sub(u'[（]', '(', row['cityName'])
        s = re.sub(u'[）]', ')', s)
        raw_data2.at[index, 'cityName'] = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", s)

raw_data2 = raw_data2.dropna(how='any')
raw_data2 = raw_data2.sort_values(by=['provinceName', 'cityName','updateTime','city_confirmedCount'])
raw_data2.drop_duplicates(keep = 'last', inplace = True)
raw_data2.to_csv(f'city-day-summary-{yesterday}.csv',index=0)