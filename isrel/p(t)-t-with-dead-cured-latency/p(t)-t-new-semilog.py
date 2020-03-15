import pandas as pd
import datetime
import matplotlib.pyplot as plt
from xpinyin import Pinyin
from scipy.optimize import curve_fit
import numpy as np
import math
import pypinyin
from itertools import compress
import statsmodels.api as sm

p = Pinyin()
color=['r','y','g','b','m','c','lawngreen','sandybrown','darkviolet','hotpink']
# today=datetime.date.today()-datetime.timedelta(days=1)
today=datetime.date(2020,3,1)
# data=pd.read_csv(f'../../dxy-data/nice-dxy-data/city-pivot-day-summary-{today}.csv')
# data_D=pd.read_csv(f'../../dxy-data/nice-dxy-data/city-D-pivot-day-summary-{today}.csv')
data=pd.read_csv(f'../../new-data-source/agged-record-data/city-confirmed-pivot-day-summary-{today}.csv')
data_D=pd.read_csv(f'../../new-data-source/agged-record-data/city-D-pivot-day-summary-{today}.csv')
# day=np.log10(list(range(1,(datetime.datetime.today().date()-datetime.date(2020,1,24)).days)))
day=list(range(0,(today-datetime.date(2020,1,23)).days))
data.sort_values(by=f'{today}',inplace=True)
data=data[data[f'{today}']>=50]
data.fillna(0, inplace=True)
data_D.fillna(0, inplace=True)
cut=8
# data.drop(columns=[f'{datetime.date(2019,12,1)+datetime.timedelta(days=i)}' for i in range((datetime.datetime(2020,1,23)-datetime.datetime(2019,12,1)).days)],inplace=True)
# data_D.drop(columns=[f'{datetime.date(2019,12,1)+datetime.timedelta(days=i)}' for i in range((datetime.datetime(2020,1,23)-datetime.datetime(2019,12,1)).days)],inplace=True)

#'北京','上海','广州','深圳'
#'合肥','信阳','蚌埠','南昌','哈尔滨'
#g'广州','深圳','珠海','成都','台州','威海','保定','金华'
#'武汉','孝感','黄冈','随州','荆州'
#'昆明','济宁','佛山'
#'扬州','厦门','漳州','汉中'

def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s

for r,pl in enumerate(['合肥','信阳']):
    city=data[data['cityName']==pl]
    record=city.values.tolist()[0][:-9]
    r=0

    city_D = data_D[data_D['cityName'] == pl]
    record_D = city_D.values.tolist()[0][:-4]

    # final=record[-1]
    record1=[ a-b for a, b in zip(record[1:],record[:-1])]
    record2=[ a-b for a, b in zip(record,record_D)]
    v2=np.log10([np.float64(m)/n for (m,n) in zip(record1,record2)])
    v1 = np.log10([np.float64(m) / n for (m, n) in zip(record1, record)])

    valid = ~(np.isnan(v2[cut:]) | np.isinf(v2[cut:]))
    popt = np.polyfit(list(compress(day[cut:], valid)), list(compress(v2[cut:], valid)), 1)
    p1 = np.poly1d(popt)
    y2 = p1(list(compress(day[cut:], valid)))

    plt.plot(list(compress(day[cut:], valid)), y2, '--', color=color[r])
    plt.plot(day, v2, 'o-', label=f'withD {pinyin(pl).capitalize()},' + r'$\tau$' + f'={-1/popt[0]:.2f}',
             color=color[r])
    plt.title('log10 linear')
    ytick = [0.001, 0.003, 0.006, 0.01, 0.02, 0.03, 0.06, 0.1, 0.3, 0.6, 1, 3]
    plt.yticks(np.log10(ytick), ytick)
    r+=1

    for latent in range(2,6):
        record1 = [a - b for a, b in zip(record[latent:], record[:-latent])]
        record2 = [a - b for a, b in zip(record[latent:], record_D[latent:])]
        v = np.log10([np.float64(m) / n for (m, n) in zip(record1, record2)])

        valid = ~(np.isnan(v[cut - latent + 1:]) | np.isnan(day[cut:]) | np.isinf(v[cut - latent + 1:]) | np.isinf(
            day[cut:]))
        popt, pcov = curve_fit(lambda t, k, b: k * t + b, list(compress(day[cut:], valid)),
                               list(compress(v[cut - latent + 1:], valid)))
        p1 = np.poly1d(popt)
        y2 = p1(list(compress(day[cut:], valid)))

        plt.plot(list(compress(day[cut:], valid)), y2, '--', color=color[r])
        plt.plot(day[latent-1:], v, 'o-', label=f'withlatent{latent} {pinyin(pl).capitalize()},' + r'$\tau$' + f'={-1/popt[0]:.2f}',
                 color=color[r])
        r+=1

    xtick=[1,2,3,4,5,6,7,8,9,10,13,16,20,23]
    # plt.text(5,np.log10(0.003),f'Data updated on {today}', fontsize=10)
    # plt.text(5,np.log10(0.003),f'Data updated on 2020-02-23', fontsize=10)
    # plt.xticks( np.log10(xtick),xtick)
    plt.ylabel('P(t)',fontsize=15)
    plt.xlabel('days',fontsize=15)
    plt.legend()
    plt.savefig(f'{pinyin(pl).capitalize()}-latent-P(t)-days-{today}-with-fit.jpg', bbox_inches='tight')
    plt.show()

# for r,pl in enumerate(['佛山','昆明','成都']):
#     city=data[data['cityName']==pl]
#     record=city.values.tolist()[0][:-9]
#     # final=record[-1]
#     record1=[ a-b for a, b in zip(record[1:],record[:-1])]
#     plt.plot(day,record1,'o-',label=f'{pinyin(pl).capitalize()}')
# plt.legend()
# plt.ylabel('newly confirmed')
# plt.xlabel('days')
# plt.savefig(f'speicalpoint-newlyconfirmed-days-{today}-with-fit.jpg', bbox_inches='tight')
# plt.show()