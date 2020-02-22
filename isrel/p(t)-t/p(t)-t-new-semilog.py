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
data=pd.read_csv(f'../../dxy-data/nice-dxy-data/city-pivot-day-summary-{today}.csv')
day=np.log10(list(range(1,(today-datetime.date(2020,1,23)).days)))
# data=pd.read_csv('province-pivot-day-summary-2020-02-18.csv')
# data=pd.read_csv(f'../../dxy-data/nice-dxy-data/city-pivot-day-summary-2020-02-18.csv')
# day=np.log10(list(range(1,(datetime.datetime.today().date()-datetime.date(2020,1,24)).days)))
day=list(range(1,(datetime.datetime.today().date()-datetime.date(2020,1,24)).days))
cut=5

#'北京','上海','广州','深圳'
#'合肥','重庆','长沙','南昌','哈尔滨'
#g'广州','深圳','珠海','成都','台州','威海','保定','金华'
#'武汉','孝感','黄冈','随州','荆州'

def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s

for r,pl in enumerate(['武汉','孝感','黄冈','随州','荆州']):
    city=data[data['cityName']==pl]
    record=city.values.tolist()[0][:-8]
    # final=record[-1]
    record1=[ a-b for a, b in zip(record[1:],record[:-1])]
    v=np.log10([m/n for (m,n) in zip(record1,record)])
    # v=list([a,b,c] for a,b,c in zip(v[0:-2],v[1:-1],v[2:]))
    # v=[np.mean([v_sub_sub for v_sub_sub in v_sub if not math.isinf(v_sub_sub)]) for v_sub in v]
    valid = ~(np.isnan(v[cut:]) | np.isnan(day[cut:])|np.isinf(v[cut:]) | np.isinf(day[cut:]))
    popt, pcov = curve_fit(lambda t, k, b: k * t + b, list(compress(day[cut:],valid)), list(compress(v[cut:],valid)))
    y2 = [popt[0] * i + popt[1] for i in day[cut:]]
    plt.plot(day[cut:], y2, '--', color=color[r])
    plt.plot(day, v, 'o-', label=f'{pinyin(pl).capitalize()} {popt[0]:.2f}', color=color[r])

    # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    # plt.show()
#,0.1,0.2,0.3,0.6,1
ytick=[0.001,0.003,0.006,0.01,0.02,0.03,0.06,0.1,0.3,0.6,1,3]
plt.yticks( np.log10(ytick),ytick)
xtick=[1,2,3,4,5,6,7,8,9,10,13,16,20,23]
plt.text(10,np.log10(3),f'Data updated on {today}', fontsize=10)
# plt.xticks( np.log10(xtick),xtick)
plt.ylabel('P(t)',fontsize=15)
plt.xlabel('days',fontsize=15)
plt.legend()
plt.savefig(f'semilog-P(t)-days-hubeicities-{today}-with-fit.jpg', bbox_inches='tight')
plt.show()

# for r,pl in enumerate(['湖北省','广东省','浙江省','江苏省']):
#     city=data[data['provinceName']==pl]
#     record=city.values.tolist()[0][:-1]
#     # final=record[-1]
#     record1=[ a-b for a, b in zip(record[1:],record[:-1])]
#     v=np.log10([m/n for (m,n) in zip(record1,record)])
#     # v=list([a,b,c] for a,b,c in zip(v[0:-2],v[1:-1],v[2:]))
#     # v=[np.mean([v_sub_sub for v_sub_sub in v_sub if not math.isinf(v_sub_sub)]) for v_sub in v]
#     valid = ~(np.isnan(v[cut:]) | np.isnan(day[cut:])|np.isinf(v[cut:]) | np.isinf(day[cut:]))
#     popt, pcov = curve_fit(lambda t, k, b: k * t + b, list(compress(day[cut:],valid)), list(compress(v[cut:],valid)))
#     y2 = [popt[0] * i + popt[1] for i in day[cut:]]
#     plt.plot(day[cut:], y2, '--', color=color[r])
#     plt.plot(day, v, 'o-', label=f'{pinyin(pl).capitalize()} {popt[0]:.2f}', color=color[r])
#
#     # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
#     # plt.show()
# #,0.1,0.2,0.3,0.6,1
# ytick=[0.001,0.003,0.006,0.01,0.02,0.03,0.06,0.1,0.3,0.6,1,3]
# plt.yticks( np.log10(ytick),ytick)
# xtick=[1,2,3,4,5,6,7,8,9,10,13,16,20,23]
# plt.text(math.log10(3),-2.3,f'Data updated on {today}', fontsize=10)
# plt.xticks( np.log10(xtick),xtick)
# plt.ylabel('P(t)',fontsize=15)
# plt.xlabel('days',fontsize=15)
# plt.legend()
# # plt.savefig(f'P(t)-days-bigcities-{today}-with-fit.jpg', bbox_inches='tight')
# plt.show()