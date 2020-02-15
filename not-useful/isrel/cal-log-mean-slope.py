import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from xpinyin import Pinyin
import scipy as sp
import matplotlib
import datetime
import time
from matplotlib.ticker import FuncFormatter

p = Pinyin()
# zhfont1 = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simhei.ttf')

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
country_data=pd.read_csv('../agg-data-old/country-day-summary-2020-02-11.csv')
data=pd.read_csv('../agg-data-old/all-city-day-summary-new.csv')
result=pd.read_csv('slope-log-mean.csv')
city_list=list(Counter(data['cityName']))
city=list()
a_list=list()
b_list=list()
result=result.sort_values(by=['a'], ascending=False).reset_index(drop=True)
#, label=f'fit-{name}-{round(popt[0],2)}'
color=['r','y','g','b','m','c','lawngreen','sandybrown','darkviolet','hotpink']
def rmse(y_test, y):
    return sp.sqrt(sp.mean((y_test - y) ** 2))

for x in range(10):
    i=result['city'][x]
    value = np.log10(data[data['cityName'] == i]['city_confirmedCount'])
    # value=value-value.shift(1)
    value=value.rolling(3).mean()
    if len(value[8:])<=8:
        continue
    name = p.get_pinyin(f"{i}", "").capitalize()
    try:
        popt, pcov = curve_fit(lambda t, a, b: a * t+b, list(range(len(value)))[8:],value[8:])
        city.append(i)
        a_list.append(popt[0])
        b_list.append(popt[1])
        y2 = [popt[0]* i+popt[1] for i in list(range(len(value)+2))[8:]]
        plt.plot(range(len(value)), value, marker='o', label=f'{i}',color=color[x])
        plt.plot(list(range(len(value)+2))[8:], y2, '--',color=color[x])
        # plt.plot(range(len(value)), value, marker='o', label=f'{i}', color=color[x])
        # plt.plot(list(range(len(value) + 2))[8:], y2, '--', color=color[x])

        # plt.title(f'{popt[0]}')
        # plt.show()
        # plt.close()
    except:
        continue
#
# result=pd.DataFrame()
# result['city']=city
# result['a']=a_list
# result['b']=b_list
# result.to_csv('slope-log-mean-2020-02-09.csv',index=0)

# formatter = FuncFormatter(formatnum)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.xlabel('日期')
date=list()
m=datetime.datetime(2020,1,24)
for i in range(2,20,2):
    m=m+datetime.timedelta(days = 2)
    date.append( m.strftime("%m-%d"))
plt.xticks( range(2,20,2), date ,rotation=45)

ytick=[1,3,6,10,30,60,100,300,600,1000,3000,6000,10000]
plt.yticks( np.log10(ytick),ytick)
# plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.ylabel('确诊人数规模-对数坐标')
plt.show()
plt.savefig('top10.jpg',bbox_inches='tight')
