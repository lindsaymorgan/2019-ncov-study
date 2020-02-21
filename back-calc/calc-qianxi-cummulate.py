import pandas as pd
from geopy import distance
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import collections
import math
from itertools import compress
import statsmodels.api as sm
import datetime

date='2020/2/18'
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False

qianxi=pd.read_csv('migration_data_hubei_22_23.csv')
raw_data=pd.read_csv('add-province-pivot-day-summary-2020-02-18.csv')
place=pd.read_csv('china_coordinates.csv')

# base=datetime.datetime.strptime(date,'%y/%m/%d')
today=datetime.date.today()-datetime.timedelta(days=1)
# qianxi['move_out']=qianxi[[f'{i}_out' for i in  [base - datetime.timedelta(days=x) for x in range((today-base).days)]]]
qianxi['move_out']=[(a+b)/2 for a,b in zip(qianxi['20200122_out'],qianxi['20200123_out'])]


data=raw_data[[f'{date}','provinceName']]
data=pd.merge(data,place,on='provinceName',how='left')
data['geo_distance']=0
data=pd.merge(data,qianxi.loc[:,['move_out','provinceName']],on='provinceName',how='left')
data1=data[(data['provinceName']!='香港') & (data['provinceName']!='澳门') & (data['provinceName']!='台湾')
& (data['provinceName']!='安徽省')& (data['provinceName']!='河南省')& (data['provinceName']!='湖南省')& (data['provinceName']!='湖北省')]
# data1=data[(data['provinceName']=='广东') | (data['provinceName']=='上海') | (data['provinceName']=='浙江')
# | (data['provinceName']=='山东')| (data['provinceName']=='北京')| (data['provinceName']=='江苏')| (data['provinceName']=='黑龙江')]
data1.drop_duplicates(keep='first',inplace=True,subset='provinceName')
data1.reset_index(inplace=True)

X = sm.add_constant(np.log10(data1['move_out']))
X_1 = sm.add_constant(np.log10(data['move_out']))
weight_add=2
lm_s = sm.WLS(np.log10(data1[f'{date}']), X,weights=[a+b for a,b in zip([i*weight_add for i in [1,0,0,1,0,0,0,0,0,0,1,0,0,1,0,0,1]]+[0]*(len(data1)-17),[1]*len(data1))]).fit()
plt.plot(np.log10(data1['move_out']), np.log10(data1[f'{date}']),'o')
plt.plot(np.log10(data['move_out']), lm_s.predict(X_1), '--', label='WLS')

# data['guess_by_wls']=data.apply(lambda row: pow(10,lm_s.params[0]*math.log10(row[10])+lm_s.params[1]), axis = 1)
data['guess_qianxi']=[pow(10,i) for i in lm_s.predict(X_1)]
data.drop_duplicates(keep='first',inplace=True,subset='provinceName')
plt.legend()
plt.xlabel('湖北迁入率 %')
plt.ylabel('确诊人数')
ytick=[1,3,6,10,30,60,100,300,600,1000,3000,6000,10000]
plt.yticks( np.log10(ytick),ytick)
xtick=[0.01,0.03,0.06,0.1,0.3,0.6,1,3,6,10,13]
plt.xticks( np.log10(xtick),xtick)
# plt.savefig(f'guess-by-qianxi.jpg', bbox_inches='tight')
plt.show()
# print(popt[0],popt[1])
# data['guess_qianxi']=data.apply(lambda row: pow(10,popt[0]*math.log10(row[10])+popt[1]), axis = 1)
#
# data.drop_duplicates(subset='provinceName',keep='first',inplace=True)
data.sort_values(by='guess_qianxi',inplace=True)
data.reset_index(inplace=True)
data2=data
plt.figure(figsize=(8,12))
plt.title(f'{date}')
valid = ~(np.isnan( data['guess_qianxi']))
# plt.text(math.log10(3),-2.3,f'2020-02-18', fontsize=10)
plt.barh(range(len(data2)-1), list(compress(data2['guess_qianxi'],valid)),color='#ff4c00')
plt.barh(range(len(data2)-1),list(compress(data2[f'{date}'],valid)))
plt.yticks(range(len(data2)-1),list(compress(data2['provinceName'],valid)),fontsize='13')
# plt.barh(range(len(data)-4), list(compress(data['guess_qianxi'],valid)),color='#ff4c00')
# plt.barh(range(len(data)-4),list(compress(data['province_confirmedCount'],valid)))
# plt.yticks(range(len(data)-4),list(compress(data['provinceName'],valid)),fontsize='13')
# plt.xticks([i*200 for i in range(9)],[i*200 for i in range(9)])
# plt.savefig(f'bar-guess-by-qianxi-compare-{weight_add}-20200201.jpg', bbox_inches='tight')

plt.show()
# data.to_csv('guess_by_qianxi.csv',index=0,encoding='utf-8-sig',sep=',')[-11:-1]
