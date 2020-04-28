import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

today = datetime.date.today()
yesterday=today-datetime.timedelta(days=1)
SP=pd.read_csv('./support-data/SP500.csv')
SP['date'] = pd.to_datetime(SP['date'])
data=pd.read_csv(f'./agged-record-data/country-day-summary-{yesterday}.csv')
data['date'] = pd.to_datetime(data['date'])

data=data[data['country']=='美国']
data['newly confirmed']=-data['confirmed'].shift(1)+data['confirmed']

data=pd.merge(data,SP,how='inner',on='date')
data=data[data['newly confirmed']!=0]
data['log newly confirmed']=np.log10(data['newly confirmed'])
data['收市值变化']=-data['收市'].shift(1)+data['收市']
print(data)

# fig = plt.figure()
#
# ax1 = fig.add_subplot(111)
# # ax1.plot(data['date'], data['收市'],'o-')
# # ax1.set_ylabel('标普500收市值')
#
# ax1.plot(data['date'], data['涨跌幅百分比'],'o-')
# ax1.set_ylabel('标普500涨跌幅')
#
# ax2 = ax1.twinx()  # this is the important function
# ax2.semilogy(data['date'], data['newly confirmed'], 'ro-')
# ax2.set_ylabel('新增确诊人数')
# ax2.set_xlabel('日期')
#
# plt.savefig('US-lognewlyconfirmed-SP500change.jpg', bbox_inches='tight')
# plt.show()

# plt.semilogy(data['收市'],data['newly confirmed'],'o')
# plt.xlabel('标普500收市值')
# plt.ylabel('新增确诊人数')
# plt.savefig('scatter-newlyconfirmed-SP500.jpg', bbox_inches='tight')
# plt.show()

plt.semilogy(data['收市值变化'],data['newly confirmed'],'o')
plt.xlabel('标普500收市值变化')
plt.ylabel('新增确诊人数')
# plt.savefig('scatter-newlyconfirmed-SP500.jpg', bbox_inches='tight')
plt.show()