import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
raw_data=pd.read_csv('city-pivot-day-summary-2020-02-12.csv')
raw_data=raw_data.sort_values(by='2020-02-12',ascending=False)[:10]
# raw_data.dropna(how='any',inplace=True)
base=datetime.datetime(2020,1,24).date()
result=dict()
# for date in list(pd.date_range(start='1/24/2018', end='2/11/2020')):
for date in [base + datetime.timedelta(days=x) for x in range(1,19)]:
    result[f'{date.strftime("%m-%d")}']=np.nansum([a*b for a,b in zip(np.subtract(raw_data[f'{date}'],raw_data[f'{date-datetime.timedelta(days=1)}']),raw_data['distance-Wuhan'])])/np.nansum(np.subtract(raw_data[f'{date}'],raw_data[f'{date-datetime.timedelta(days=1)}']))
# key=list(result.keys()).reverse()
# value=list(result.values()).reverse()
plt.plot(result.keys(),result.values(),'o-')
plt.ylabel('新增确诊病例与武汉市的平均距离/公里')
plt.xlabel('日期')
# plt.ylabel('newlyconfirmcount-average-distance/km')
# plt.xlabel('date')
plt.xticks(rotation=45)
plt.savefig('newlyconfirmcount-average-distance-2020-02-12.jpg', bbox_inches='tight')
plt.show()

result1=dict()
for date in [base + datetime.timedelta(days=x) for x in range(19)]:
    result1[f'{date.strftime("%m-%d")}']=np.nansum([a*b for a,b in zip(raw_data[f'{date}'],raw_data['distance-Wuhan'])])/np.nansum(raw_data[f'{date}'])
print(result1)
plt.plot(result1.keys(),result1.values(),'o-')
plt.ylabel('总确诊病例与武汉市的平均距离/公里')
plt.xlabel('日期')
# plt.ylabel('confirmcount-average-distance/km')
# plt.xlabel('date')
plt.xticks(rotation=45)
plt.savefig('confirmcount-average-distance-2020-02-12.jpg', bbox_inches='tight')
plt.show()