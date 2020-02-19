import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
from xpinyin import Pinyin
import collections
import datetime
from geopy import distance

p = Pinyin()
today=datetime.datetime(2003,6,1).date()
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
data=pd.read_csv(f'../../SARS-data/SARS-data.csv')
color=['r','y','g','b','m','c','lawngreen','sandybrown','darkviolet','hotpink']
# plt.scatter(np.log10(data['distance']),np.log10(data['2020-02-11']))
cut=7
for x, c_name in enumerate ([('广东',23.40800373,113.3948176),('北京',39.92998578,116.395645)]):
    lat=c_name[1]
    lon=c_name[2]
    name=p.get_pinyin(c_name[0], "").capitalize()
    dict_dis=dict()
    # [1.875+i*0.25 for i in range(8)]
    for i in range(len(data)):
        if data[f'province'][i]!=c_name[0]:
            # print(f'{(data["lat"][i],data["lon"][i])}')
            t=int((np.log10(distance.distance((data['lat'][i],data['lon'][i]), (lat,lon)).kilometers)-1.875)/0.25)
            dict_dis.setdefault(1.875+t*0.25, []).append(np.log10(data['2003-06-01'])[i])
    dict_dis1=dict.fromkeys([1.875+i*0.25 for i in range(8)],)
    for t in dict_dis.keys():
        dict_dis1[t]=np.nanmean(dict_dis[t])

    dict_dis1 =  {k: dict_dis1[k] for k in dict_dis1 if dict_dis1[k] is not None}
    dict_dis1 = collections.OrderedDict(sorted(dict_dis1.items()))

    popt, pcov = curve_fit(lambda t, k, b: k * t + b, list(dict_dis1.keys()), list(dict_dis1.values()))
    y2 = [popt[0] * i + popt[1] for i in list(dict_dis1.keys())]
    plt.plot(list(dict_dis1.keys()), y2, '--', color=color[x])
    plt.plot(list(dict_dis1.keys()), list(dict_dis1.values()), 'o-', color=color[x], label=f'{name} {popt[0]:.2f}')
    # plt.loglog(np.power(10,list(dict_dis1.keys())),np.power(10,list(dict_dis1.values())),'o-',label=c_name)

# plt.title('武汉',fontsize=15)
plt.xlabel('Distance/km',fontsize=15)
plt.ylabel('Confirmcount',fontsize=15)
ytick=[1,3,6,10,30,60,100,300,600,1000]
plt.yticks( np.log10(ytick),ytick)
xtick=[60,100,300,600,1000,1300,1600,2000,2600]
plt.xticks( np.log10(xtick),xtick)
plt.legend()
plt.savefig(f'SARS-distance-cases.jpg', bbox_inches='tight')
plt.show()
