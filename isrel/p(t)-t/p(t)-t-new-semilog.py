import pandas as pd
import datetime
import matplotlib.pyplot as plt
from xpinyin import Pinyin
from scipy.optimize import curve_fit
import numpy as np
import math
import pypinyin
from itertools import compress

p = Pinyin()
color=['r','y','g','b','m','c','lawngreen','sandybrown','darkviolet','hotpink']
today=datetime.date.today()-datetime.timedelta(days=1)
# data=pd.read_csv(f'../../dxy-data/nice-dxy-data/city-pivot-day-summary-{today}.csv')
# data=pd.read_csv('province-pivot-day-summary-2020-02-18.csv')
data=pd.read_csv(f'../../new-data-source/agged-record-data/city-confirmed-pivot-day-summary-{today}.csv')
# day=np.log10(list(range(1,(datetime.datetime.today().date()-datetime.date(2020,1,24)).days)))
day=list(range(0,(today-datetime.date(2020,1,23)).days-1))
cut=8

#'北京','上海','广州','深圳'
#'合肥','信阳','蚌埠','南昌','哈尔滨'
#g'广州','深圳','珠海','成都','台州','威海','保定','金华'
#'武汉','孝感','黄冈','随州','荆州'
#'昆明','济宁','佛山'

def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s

for r,pl in enumerate(['北京','上海','广州','深圳']):
    city=data[data['cityName']==pl]
    record=city.values.tolist()[0][:-8]
    # final=record[-1]
    record1=[ a-b for a, b in zip(record[1:],record[:-1])]
    v=np.log10([m/n for (m,n) in zip(record1,record)])

    valid = ~(np.isnan(v[cut:]) | np.isinf(v[cut:]))
    popt=np.polyfit(list(compress(day[cut:],valid)), list(compress(v[cut:],valid)),1)
    p1 = np.poly1d(popt)
    y2 = p1(list(compress(day[cut:],valid)))

    # popt, pcov = curve_fit(lambda t, k, b: k * t + b, list(compress(day[cut:],valid)), list(compress(v[cut:],valid)))
    # y2 = [popt[0] * i + popt[1] for i in day[cut:]]

    # plt.plot(day[cut:], y2, '--', color=color[r])
    plt.plot(list(compress(day[cut:],valid)), y2, '--', color=color[r])
    plt.plot(day, v, 'o-', label=f'{pinyin(pl).capitalize()},'+r'$\tau$'+f'={-1/popt[0]:.2f}', color=color[r])
    plt.title('log10 linear')
    ytick=[0.001,0.003,0.006,0.01,0.02,0.03,0.06,0.1,0.3,0.6,1,3]
    plt.yticks( np.log10(ytick),ytick)

    # v = [m / n for (m, n) in zip(record1, record)]
    # popt, pcov = curve_fit(lambda t, b,c: np.exp(-t/b)*c , day[cut:], v[cut:])
    # # print(popt[1])
    # y2 = [np.exp(-i/popt[0])*popt[1] for i in day[cut:]]
    # plt.title('exp')
    # plt.semilogy(day[cut:], y2, '--', color=color[r])
    # plt.semilogy(day, v, 'o-', label=f'{pinyin(pl).capitalize()},'+r'$\tau$'+f'={popt[0]:.2f}', color=color[r])

    # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    # plt.show()
#,0.1,0.2,0.3,0.6,1

xtick=[1,2,3,4,5,6,7,8,9,10,13,16,20,23]
# plt.text(5,np.log10(0.003),f'Data updated on {today}', fontsize=10)
# plt.text(5,np.log10(0.003),f'Data updated on 2020-02-23', fontsize=10)
# plt.xticks( np.log10(xtick),xtick)
plt.ylabel('P(t)',fontsize=15)
plt.xlabel('days',fontsize=15)
plt.legend()
# plt.savefig(f'illustrate-semilog-P(t)-days-{today}-with-fit.jpg', bbox_inches='tight')
plt.show()

# for r,pl in enumerate(['孝感','天津']):
#     city=data[data['cityName']==pl]
#     record=city.values.tolist()[0][:-8]
#     # final=record[-1]
#     record1=[ a-b for a, b in zip(record[1:],record[:-1])]
#     plt.semilogy(day,record1,'o-',label=f'{pinyin(pl).capitalize()}')
# plt.legend()
# plt.ylabel('newly confirmed')
# plt.xlabel('days')
# plt.savefig(f'illustrate-newlyconfirmed-days-{today}-with-fit.jpg', bbox_inches='tight')
# plt.show()