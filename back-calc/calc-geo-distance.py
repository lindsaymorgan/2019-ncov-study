import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
from xpinyin import Pinyin
import collections
import datetime
import math

#杭州距武汉550km
p = Pinyin()
today=datetime.date.today()-datetime.timedelta(days=2)
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
data=pd.read_csv(f'city-pivot-day-summary-{today}.csv')
color=['r','y','g','b','m','c','lawngreen','sandybrown','darkviolet','hotpink']
# plt.scatter(np.log10(data['distance']),np.log10(data['2020-02-11']))
cut=4
for x, c_name in enumerate (['武汉']):
    name=p.get_pinyin(c_name, "").capitalize()
    dict_dis=dict()
    # [1.875+i*0.25 for i in range(8)]
    for i in range(len(data)):
        if data[f'distance-{name}'][i]!=0:
            t=int((np.log10(data[f'distance-{name}'])[i]-1.875)/0.25)
            # dict_dis.setdefault(1.875+t*0.25, []).append(np.log10(data[f'{today}'])[i])
            dict_dis.setdefault(1.875 + t * 0.25, []).append(np.log10(data['2020-01-25'])[i])
    dict_dis1=dict.fromkeys([1.875+i*0.25 for i in range(8)],)
    for t in dict_dis.keys():
        dict_dis1[t]=np.nanmean(dict_dis[t])

    dict_dis1 =  {k: dict_dis1[k] for k in dict_dis1 if dict_dis1[k] is not None}
    dict_dis1 = collections.OrderedDict(sorted(dict_dis1.items()))

    popt, pcov = curve_fit(lambda t, k, b: k * t + b, list(dict_dis1.keys())[-cut:], list(dict_dis1.values())[-cut:])
    y2 = [popt[0] * i + popt[1] for i in list(dict_dis1.keys())]
    plt.plot(list(dict_dis1.keys()), y2, '--', color=color[x])
    plt.plot(list(dict_dis1.keys()), list(dict_dis1.values()), 'o-', color=color[x], label=f'{c_name}_{popt[0]:.2f}_{popt[1]:.2f}')
    # plt.loglog(np.power(10,list(dict_dis1.keys())),np.power(10,list(dict_dis1.values())),'o-',label=c_name)
data['guess_count']=0
for i,row in data.iterrows():
    if row[-6]!=0:
        data.at[i, 'guess_count']=pow(10,popt[0]*math.log10(row[-6])+popt[1])
# data.to_csv('guess-by-geo-distance-2020-02-01.csv',index=0,encoding='utf-8-sig',sep=',')
# plt.title('武汉',fontsize=15)
plt.text(1,0.5,f'确诊人数截至{today}', fontsize=10)
plt.xlabel('与该城市的距离-对数坐标',fontsize=15)
plt.ylabel('确诊人数-对数坐标',fontsize=15)
ytick=[1,3,6,10,30,60,100,300,600,1000]
plt.yticks( np.log10(ytick),ytick)
xtick=[60,100,300,600,1000,3000]
plt.xticks( np.log10(xtick),xtick)
plt.legend()
# plt.savefig(f'guess-by-geo-distance.jpg', bbox_inches='tight')
plt.show()
