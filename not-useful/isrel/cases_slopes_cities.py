import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from xpinyin import Pinyin
import scipy as sp

p = Pinyin()
data=pd.read_csv('../increase-log/all-city-day-summary-new.csv')

city_list=list(Counter(data['cityName']))
city=list()
a_list=list()
b_list=list()
# city_list[:20]
def rmse(y_test, y):
    return sp.sqrt(sp.mean((y_test - y) ** 2))

for i in ['武汉']:
    value = np.log10(data[data['cityName'] == i]['city_confirmedCount'])
    value=value-value.shift(1)
    value=value.rolling(3).mean()
    if len(value[8:])<=8:
        continue
    name = p.get_pinyin(f"{i}", "").capitalize()
    try:
        popt, pcov = curve_fit(lambda t, a, b: a * t+b, list(range(8,len(value))),value[8:])
        city.append(i)
        a_list.append(popt[0])
        b_list.append(popt[1])
        y2 = [popt[0]* i+popt[1] for i in list(range(8,len(value)))]
        print(rmse(value[8:],y2))
        plt.plot(range(8,len(value)), y2, marker='o', label=f'{name}')
        plt.plot(range(len(value)),value,marker='o',label=f'{name}')
        plt.title(f'{popt[0]}')
        plt.show()
        plt.close()
    except:
        continue

# result=pd.DataFrame()
# result['city']=city
# result['a']=a_list
# result['b']=b_list
# result.to_csv('slope-new-8.csv',index=0)
# plt.legend()
# plt.show()