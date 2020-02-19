import pandas as pd
from geopy import distance
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import collections
import math
from itertools import compress
import statsmodels.api as sm

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False
qianxi=pd.read_csv('baiduqianxi_hubei_level_20200122.csv')
raw_data=pd.read_csv('province-day-summary-2020-02-17.csv')
place=pd.read_csv('china_coordinates.csv')

data=raw_data[raw_data['updateTime']=='2020-02-17']
# data.drop(['currentConfirmedCount'],inplace=True)
data=pd.merge(data,place,on='provinceName',how='left')
data['geo_distance']=0
data=pd.merge(data,qianxi.loc[:,['move_out','provinceName']],on='provinceName',how='left')
# data1=data[(data['provinceName']!='香港') & (data['provinceName']!='澳门') & (data['provinceName']!='台湾')
# & (data['provinceName']!='安徽省')& (data['provinceName']!='河南省')& (data['provinceName']!='湖南省')& (data['provinceName']!='湖北省')]
data1=data[(data['provinceName']=='广东') | (data['provinceName']=='上海') | (data['provinceName']=='浙江')
| (data['provinceName']=='山东')| (data['provinceName']=='北京')| (data['provinceName']=='江苏')| (data['provinceName']=='黑龙江')]
data1.reset_index(inplace=True)
# data['geo_distance'] = data.apply(lambda row: distance.distance((row[8],row[7]), (30.52,114.31)).kilometers, axis = 1)

dict_dis=dict()
    # [1.875+i*0.25 for i in range(8)]
for i in range(len(data1)):
    move=int((np.log10(data1['move_out'])[i]+2)/0.5)
    dict_dis.setdefault(-2+move*0.5, []).append(np.log10(data1['province_confirmedCount'])[i])
dict_dis1=dict.fromkeys([-2+i*0.5 for i in range(8)],)
for t in dict_dis.keys():
    dict_dis1[t]=np.nanmean(dict_dis[t])

dict_dis1 =  {k: dict_dis1[k] for k in dict_dis1 if dict_dis1[k] is not None}
dict_dis1 = collections.OrderedDict(sorted(dict_dis1.items()))

# popt, pcov = curve_fit(lambda t, k, b: k * t + b, np.log10(data1['move_out']), np.log10(data1['province_confirmedCount']))
# y2 = [popt[0] * i + popt[1] for i in np.log10(data1['move_out'])]
# plt.plot(np.log10(data1['move_out']), y2, '--')

popt, pcov = curve_fit(lambda t, k, b: k * t + b, list(dict_dis1.keys())[2:], list(dict_dis1.values())[2:])
y2 = [popt[0] * i + popt[1] for i in list(dict_dis1.keys())[2:]+[0.8,1]]
plt.plot(list(dict_dis1.keys())[2:]+[0.8,1], y2, '--', label=f'{popt[0]:.2f}')
plt.plot(list(dict_dis1.keys()), list(dict_dis1.values()), 'o-')
plt.legend()
plt.xlabel('湖北迁入率 %')
plt.ylabel('确诊人数')
ytick=[1,3,6,10,30,60,100,300,600,1000,3000,6000,10000]
plt.yticks( np.log10(ytick),ytick)
xtick=[0.01,0.03,0.06,0.1,0.3,0.6,1,3,6,10,13]
plt.xticks( np.log10(xtick),xtick)
# plt.savefig(f'guess-by-qianxi.jpg', bbox_inches='tight')
plt.show()
print(popt[0],popt[1])
data['guess_qianxi']=data.apply(lambda row: pow(10,popt[0]*math.log10(row[10])+popt[1]), axis = 1)

data.drop_duplicates(subset='provinceName',keep='first',inplace=True)
data.sort_values(by='guess_qianxi',inplace=True)
data.reset_index(inplace=True)
plt.figure(figsize=(8,12))

valid = ~(np.isnan( data['guess_qianxi']))
plt.barh(range(len(data)-4), list(compress(data['guess_qianxi'],valid)),color='#ff4c00')
plt.barh(range(len(data)-4),list(compress(data['province_confirmedCount'],valid)))
plt.yticks(range(len(data)-4),list(compress(data['provinceName'],valid)),fontsize='13')
# plt.xticks([i*200 for i in range(9)],[i*200 for i in range(9)])
# plt.savefig('bar-guess-by-qianxi-compare.jpg', bbox_inches='tight')

plt.show()
# data.to_csv('guess_by_qianxi.csv',index=0,encoding='utf-8-sig',sep=',')
