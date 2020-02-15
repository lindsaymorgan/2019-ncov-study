import pandas as pd
import powerlaw
import matplotlib.pyplot as plt
import numpy as np

raw_data=pd.read_csv('../rawdata.csv')
raw_data['updateTime'] = pd.to_datetime(raw_data['updateTime'])

raw_data1 = pd.pivot_table(raw_data, index=[raw_data['updateTime'].dt.date, 'provinceName'], values=['province_confirmedCount', 'province_suspectedCount', 'province_curedCount'], aggfunc=np.max)
raw_data1=pd.DataFrame(raw_data1.to_records())
raw_data3= pd.pivot_table(raw_data1, index=raw_data1['updateTime'], values=['province_confirmedCount', 'province_suspectedCount', 'province_curedCount'], aggfunc=np.sum)
raw_data3=pd.DataFrame(raw_data3.to_records())
# # group_province_confirmedCount=raw_data.groupby([raw_data['updateTime'].dt.date,'provinceName'])['province_confirmedCount'].max().to_frame(name = 'province_confirmedCount').reset_index()
# # group_province_confirmedCount=raw_data.groupby([raw_data['updateTime'].dt.date,'provinceName'])['province_suspectedCount'].max().to_frame(name = 'province_suspectedCount').reset_index()
# raw_data1.to_csv('province-day-summary-2020-02-11.csv',index=0)
# raw_data3.to_csv('country-day-summary-2020-02-11.csv',index=0)
# print(raw_data3)
# fit = powerlaw.Fit(data)
# fit.power_law.plot_pdf(color = ‘b’, linestyle = ‘–’, ax = fig2)
# plt.ylabel('population')
# plt.show()
# raw_data=raw_data[(raw_data['provinceName']!='北京市') & (raw_data['provinceName']!='上海市') & (raw_data['provinceName']!='重庆市') & (raw_data['provinceName']!='天津市')]
raw_data2 = pd.pivot_table(raw_data, index=[raw_data['updateTime'].dt.date, 'cityName'], values=['provinceName','city_confirmedCount', 'city_suspectedCount', 'city_curedCount'], aggfunc=np.max)
raw_data2=pd.DataFrame(raw_data2.to_records())
raw_data2.to_csv('city-day-summary-2020-02-11.csv',index=0)