import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
from xpinyin import Pinyin
import collections
from itertools import compress
import datetime
import matplotlib

matplotlib.rcParams['axes.unicode_minus'] = False
p = Pinyin()
today=datetime.date.today()-datetime.timedelta(days=1)
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
data=pd.read_csv(f'../../dxy-data/nice-dxy-data/city-pivot-day-summary-{today}.csv')
color=['r','y','g','b','m','c','lawngreen','sandybrown','darkviolet','hotpink']

date_list = [(datetime.datetime(2020,1,23) + datetime.timedelta(days=x)).date() for x in range((today-datetime.date(2020,1,23)).days)]
slope_list=list()
for x, date in enumerate (date_list):
    dict_dis=dict()
    # [1.875+i*0.25 for i in range(8)]
    for i in range(len(data)):
        if data[f'distance-Wuhan'][i]!=0:
            t=int((np.log10(data[f'distance-Wuhan'])[i]-1.875)/0.25)
            dict_dis.setdefault(1.875+t*0.25, []).append(np.log10(data[f'{date}'])[i])
    dict_dis1=dict.fromkeys([1.875+i*0.25 for i in range(8)],)
    for t in dict_dis.keys():
        dict_dis1[t]=np.nanmean(dict_dis[t])

    dict_dis1 =  {k: dict_dis1[k] for k in dict_dis1 if dict_dis1[k] is not None}
    dict_dis1 = collections.OrderedDict(sorted(dict_dis1.items()))

    valid = ~(np.isnan(list(dict_dis1.values())) |  np.isinf(list(dict_dis1.values())))
    popt, pcov = curve_fit(lambda t, k, b: k * t + b, list(compress(list(dict_dis1.keys()),valid)), list(compress(list(dict_dis1.values()),valid)))
    slope_list.append(popt[0])
    # y2 = [popt[0] * i + popt[1] for i in list(dict_dis1.keys())]
    # plt.plot(list(dict_dis1.keys()), y2, '--', color=color[x])
    # plt.plot(list(dict_dis1.keys()), list(dict_dis1.values()), 'o-', color=color[x], label=f'Wuhan_{popt[0]:.2f}')
    # plt.loglog(np.power(10,list(dict_dis1.keys())),np.power(10,list(dict_dis1.values())),'o-',label=c_name)

plt.plot(date_list,slope_list,'o-')

plt.xlabel('$date$',fontsize=15,fontstyle='italic')
plt.ylabel(r'$Spatial Exponent$',fontsize=15,fontstyle='italic')
# ytick=[1,3,6,10,30,60,100,300,600,1000]
# plt.yticks( np.log10(ytick),ytick)
# xtick=[60,100,300,600,1000,3000]
# plt.xticks( np.log10(xtick),xtick)

plt.savefig(f'distance-cases-multidays-{today}.jpg', bbox_inches='tight')
plt.show()
