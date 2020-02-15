import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
today=datetime.date.today()-datetime.timedelta(days=1)
raw_data=pd.read_csv(f'/mnt/data/Lindsay/2019-ncov/program/dxy-data/nice-dxy-data/city-pivot-day-summary-{today}.csv')

raw_data=raw_data.sort_values(by=f'{today}',ascending=False)[:10]

base=datetime.datetime(2020,1,24).date()
length=(datetime.datetime.today()-datetime.datetime(2020,1,24)).days
result=dict()

for date in [base + datetime.timedelta(days=x) for x in range(1,length)]:
    result[f'{date.strftime("%m-%d")}']=np.nansum([a*b for a,b in zip(np.subtract(raw_data[f'{date}'],raw_data[f'{date-datetime.timedelta(days=1)}']),raw_data['distance-Wuhan'])])/np.nansum(np.subtract(raw_data[f'{date}'],raw_data[f'{date-datetime.timedelta(days=1)}']))
plt.plot(list(result.keys()),list(result.values()),'o-')
plt.ylabel('新增确诊病例与武汉市的平均距离/公里')
plt.xlabel('日期')
# plt.ylabel('newlyconfirmcount-average-distance/km')
# plt.xlabel('date')
plt.xticks(rotation=45)
plt.savefig(f'/mnt/data/Lindsay/2019-ncov/program/everyday-run/result/newlyconfirmcount-average-distance-{today}.jpg', bbox_inches='tight')
plt.show()

# result1=dict()
# for date in [base + datetime.timedelta(days=x) for x in range(19)]:
#     result1[f'{date.strftime("%m-%d")}']=np.nansum([a*b for a,b in zip(raw_data[f'{date}'],raw_data['distance-Wuhan'])])/np.nansum(raw_data[f'{date}'])
# print(result1)
# plt.plot(result1.keys(),result1.values(),'o-')
# plt.ylabel('总确诊病例与武汉市的平均距离/公里')
# plt.xlabel('日期')
# # plt.ylabel('confirmcount-average-distance/km')
# # plt.xlabel('date')
# plt.xticks(rotation=45)
# plt.savefig('confirmcount-average-distance-2020-02-12.jpg', bbox_inches='tight')
# plt.show()


