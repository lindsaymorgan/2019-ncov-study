import pandas as pd
import datetime
import matplotlib.pyplot as plt
from xpinyin import Pinyin
from scipy.optimize import curve_fit
import numpy as np
import math
from itertools import compress

p = Pinyin()
color=['r','y','g','b','m','c','lawngreen','sandybrown','darkviolet','hotpink']
today=datetime.date.today()-datetime.timedelta(days=1)
data=pd.read_csv(f'../../dxy-data/nice-dxy-data/city-pivot-day-summary-{today}.csv')
day=np.log10(list(range(1,(today-datetime.date(2020,1,25)).days)))
cut=4

#'北京','上海','广州','深圳']
#'合肥','重庆','长沙','南昌','哈尔滨'
#g'广州','深圳','珠海','成都','台州','威海','保定','金华'
#'武汉','孝感','黄冈','随州','荆州'

for r,pl in enumerate(['十堰']):
    city=data[data['cityName-ch']==pl]
    record=city.values.tolist()[0][:-7]
    # final=record[-1]
    record1=[ a-b for a, b in zip(record[1:],record[:-1])]
    v=np.log10([m/n for (m,n) in zip(record1,record[1:])])
    v=list([a,b,c] for a,b,c in zip(v[0:-2],v[1:-1],v[2:]))
    v=[np.mean([v_sub_sub for v_sub_sub in v_sub if not math.isinf(v_sub_sub)]) for v_sub in v]
    valid = ~(np.isnan(v[cut:]) | np.isnan(day[cut:]))
    # print(v)
    popt, pcov = curve_fit(lambda t, k, b: k * t + b, list(compress(day[cut:],valid)), list(compress(v[cut:],valid)))
    y2 = [popt[0] * i + popt[1] for i in day[cut:]]
    plt.plot(day[cut:], y2, '--', color=color[r])
    plt.plot(day, v, 'o-', label=f'{p.get_pinyin(pl, "").capitalize()} {popt[0]:.2f}', color=color[r])

    # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    # plt.show()
#,0.1,0.2,0.3,0.6,1
ytick=[0.01,0.02,0.03,0.06,0.1,0.3,0.6]
plt.yticks( np.log10(ytick),ytick)
xtick=[1,2,3,4,5,6,7,8,9,10,13,16,20,23]
plt.text(math.log10(3),-1.8,f'Data updated on {today}', fontsize=10)
plt.xticks( np.log10(xtick),xtick)
plt.ylabel('P(t)',fontsize=15)
plt.xlabel('days',fontsize=15)
plt.legend()
plt.savefig(f'P(t)-days-othercites-{today}.jpg', bbox_inches='tight')
plt.show()