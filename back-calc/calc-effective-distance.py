import pandas as pd
from geopy import distance
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import collections
import math

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
data['effect_distance']=data.apply(lambda row: 1-math.log10(row[10]/100), axis = 1)
data1=data[(data['provinceName']!='香港') & (data['provinceName']!='澳门') & (data['provinceName']!='台湾')
& (data['provinceName']!='安徽省')& (data['provinceName']!='河南省')& (data['provinceName']!='湖南省')& (data['provinceName']!='湖北省')]
data1.reset_index(inplace=True)
# data['geo_distance'] = data.apply(lambda row: distance.distance((row[8],row[7]), (30.52,114.31)).kilometers, axis = 1)

dict_dis=dict()
    # [1.875+i*0.25 for i in range(8)]
for i in range(len(data1)):
    move=int((data1['effect_distance'][i]-1)/0.5)
    dict_dis.setdefault(1+move*0.5, []).append(data1['province_confirmedCount'][i])
dict_dis1=dict.fromkeys([1+i*0.5 for i in range(8)],)
for t in dict_dis.keys():
    dict_dis1[t]=math.log10(np.nanmean(dict_dis[t]))

dict_dis1 =  {k: dict_dis1[k] for k in dict_dis1 if dict_dis1[k] is not None}
dict_dis1 = collections.OrderedDict(sorted(dict_dis1.items()))

# popt, pcov = curve_fit(lambda t, k, b: k * t + b, np.log10(data1['move_out']), np.log10(data1['province_confirmedCount']))
# y2 = [popt[0] * i + popt[1] for i in np.log10(data1['move_out'])]
# plt.plot(np.log10(data1['move_out']), y2, '--')

popt, pcov = curve_fit(lambda t, k, b: k * t + b, list(dict_dis1.keys())[:-2], list(dict_dis1.values())[:-2])
y2 = [popt[0] * i + popt[1] for i in list(dict_dis1.keys())[:-2]+[1]]
plt.plot(list(dict_dis1.keys())[:-2]+[1], y2, '--', label=f'{popt[0]:.2f}')
plt.plot(list(dict_dis1.keys()), list(dict_dis1.values()), 'o-')
plt.legend()
plt.xlabel('有效距离')
plt.ylabel('确诊人数')
ytick=[1,3,6,10,30,60,100,300,600,1000,3000,6000,10000]
plt.yticks( np.log10(ytick),ytick)
# xtick=[1,3,6]
# plt.xticks( xtick,xtick)
plt.savefig(f'guess-by-effectivedistance.jpg', bbox_inches='tight')
plt.show()
print(popt[0],popt[1])
data['guess_effectivedistance']=data.apply(lambda row: pow(10,popt[0]*row[11]+popt[1]), axis = 1)
data.to_csv('guess_by_effectivedistance.csv',index=0,encoding='utf-8-sig',sep=',')
