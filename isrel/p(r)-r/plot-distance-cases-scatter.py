import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
from xpinyin import Pinyin
import collections
import datetime
from itertools import compress

p = Pinyin()
today=datetime.date.today()-datetime.timedelta(days=1)
date=today-datetime.timedelta(days=1)
# date=datetime.datetime(2020,2,20).date()
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
data=pd.read_csv(f'../../dxy-data/nice-dxy-data/city-pivot-day-summary-{today}.csv')
# data=pd.read_csv(f'../../dxy-data/nice-dxy-data/province-pivot-day-summary-{today}.csv')
data=data[data['provinceName']!='澳门']
color=['r','y','g','b','m','c','lawngreen','sandybrown','darkviolet','hotpink']
# plt.scatter(np.log10(data['distance']),np.log10(data['2020-02-11']))
cut=7
# distance=np.log10(data['distance-Hubei'])
distance=np.log10(data['distance-Wuhan'])
confirm=np.log10(data[f'{date}'])
valid = ~(np.isnan(distance) | np.isinf(distance) |np.isnan(confirm) |np.isinf(confirm))
popt, pcov = curve_fit(lambda t, k, b: k * t + b, list(compress(distance,valid)),list(compress(confirm,valid)))

y2 = [popt[0] * i + popt[1] for i in list(compress(distance,valid))]
plt.plot(np.power(10,list(compress(distance,valid))), np.power(10,y2), '--')
# plt.loglog(data[f'distance-Hubei'],data[f'{date}'], 'o',label=f'{date} {popt[0]:.2f}')
plt.loglog(data[f'distance-Wuhan'],data[f'{date}'], 'o',label=f'{date} {popt[0]:.2f}')
plt.title('city-level-without bin')
# plt.title('province-level-without bin')
# plt.text(2,0.5,f'Data updated on {today}', fontsize=10)
# plt.xlabel('Distance From Hubei/km',fontsize=15)
plt.ylabel('Confirmcount',fontsize=15)
plt.xlabel('Distance From Wuhan/km',fontsize=15)

plt.legend()
# plt.savefig(f'distance-cases-provincelevel-withoutbin-{date}.jpg', bbox_inches='tight')
plt.savefig(f'distance-cases-citylevel-withoutbin-{date}.jpg', bbox_inches='tight')
plt.show()

