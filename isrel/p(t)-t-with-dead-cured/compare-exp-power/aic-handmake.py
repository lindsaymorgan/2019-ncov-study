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
from scipy.stats import kstest

p = Pinyin()
color=['r','y','g','b','m','c','lawngreen','sandybrown','darkviolet','hotpink']
# today=datetime.date.today()-datetime.timedelta(days=1)
today=datetime.date(2020,3,1)
# data=pd.read_csv(f'../../dxy-data/nice-dxy-data/city-pivot-day-summary-{today}.csv')
# data_D=pd.read_csv(f'../../dxy-data/nice-dxy-data/city-D-pivot-day-summary-{today}.csv')
data=pd.read_csv(f'../../../new-data-source/agged-record-data/city-confirmed-pivot-day-summary-{today}.csv')
data_D=pd.read_csv(f'../../../new-data-source/agged-record-data/city-D-pivot-day-summary-{today}.csv')
data=data[data[f'{today}']>=50]
# day=np.log10(list(range(1,(datetime.datetime.today().date()-datetime.date(2020,1,24)).days)))
day=list(range(0,(today-datetime.date(2020,1,23)).days))
cut=8
# data.drop(columns=[f'{datetime.date(2019,12,1)+datetime.timedelta(days=i)}' for i in range((datetime.datetime(2020,1,23)-datetime.datetime(2019,12,1)).days)],inplace=True)
# data_D.drop(columns=[f'{datetime.date(2019,12,1)+datetime.timedelta(days=i)}' for i in range((datetime.datetime(2020,1,23)-datetime.datetime(2019,12,1)).days)],inplace=True)

cityName_list=list()
exp_aic=list()
pl_aic=list()
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

for r,pl in enumerate(data['cityName']):
    city=data[data['cityName']==pl]
    record=city.values.tolist()[0][:-9]

    city_D = data_D[data_D['cityName'] == pl]
    record_D = city_D.values.tolist()[0][:-4]

    # final=record[-1]
    record1=[ a-b for a, b in zip(record[1:],record[:-1])]
    record2=[ a-b for a, b in zip(record,record_D)]
    v2 = np.log10([np.float64(m) / n for (m, n) in zip(record1, record2)])

    try:
        valid = ~(np.isnan(v2[cut:]) | np.isnan(day[cut:]) | np.isinf(v2[cut:]) | np.isinf(day[cut:]))

        X = sm.add_constant(list(compress(day[cut:], valid)))
        mod = sm.OLS(list(compress(v2[cut:], valid)), X)
        res1 = mod.fit()

        #确定残差是否是正态分布
        resident= res1.resid
        # fig = sm.qqplot(resident)
        # plt.show()
        print(kstest(resident, 'norm',(0,math.sqrt(np.mean([pow(resident,2)])))))

        #计算AICc
        AICc=2*2+2*(1/(2*pow(np.std(resident),2))+len(v2[cut:])*np.log(math.sqrt(2*math.pi)*np.std(resident))+np.sum([pow(resident,2)]))
        print(f'AIC-hand {AICc} {res1.aic}')
        # mod_result1=sm.regression.linear_model.OLSResults(mod,res.params)

        # print(f'exp aic={mod_result.aic}')

        # valid = ~(np.isnan(v2[cut:]) | np.isnan(np.log10(day[cut:])) | np.isinf(v2[cut:]) | np.isinf(np.log10(day[cut:])))
        # X = sm.add_constant(list(compress(np.log10(day[cut:]), valid)))
        # mod = sm.OLS(list(compress(v2[cut:], valid)), X)
        # res2 = mod.fit()
        #
        # # 确定残差是否是正态分布
        # resident = res2.resid
        # print(kstest(resident, 'norm', (0, np.std(resident))))

        # # mod_result2=sm.regression.linear_model.OLSResults(mod,res.params)
        #
        # # if res1.aic!=-np.inf and res2.aic!=-np.inf:
        # cityName_list.append(f'{pinyin(pl).capitalize()}')
        # exp_aic.append(res1.aic+2*2*3/(len(v2)-2-1))
        # pl_aic.append(res2.aic+2*2*3/(len(v2)-2-1))
    except:
        continue
    # print(f'exp aic={mod_result.aic}')

    # popt, pcov = curve_fit(lambda t, k, b: k * t + b, list(compress(day[cut:],valid)), list(compress(v[cut:],valid)))
    # y2 = [popt[0] * i + popt[1] for i in day[cut:]]

    # plt.plot(day[cut:], y2, '--', color=color[r])
    # plt.plot(list(compress(day[cut:], valid)), y2, '--', color=color[r])
    # plt.plot(day, v2, 'o-', label=f'withD {pinyin(pl).capitalize()},' + r'$\tau$' + f'={-1/popt[0]:.2f}',
    #          color=color[2*r+1])
    # plt.title('log10 linear')
    # ytick = [0.001, 0.003, 0.006, 0.01, 0.02, 0.03, 0.06, 0.1, 0.3, 0.6, 1, 3]
    # plt.yticks(np.log10(ytick), ytick)
#,0.1,0.2,0.3,0.6,1

# result=pd.DataFrame()
# result['cityName-en']=cityName_list
# result['exp_aic']=exp_aic
# result['powerlaw_aic']=pl_aic
# result=pd.merge(result,data[['cityName-en','provinceName-en',f'{today}']])
#
# # result.to_csv('withoutinf-AIC-compare-exp-powerlaw.csv',index=0)
# result.to_csv('AIC-compare-exp-powerlaw.csv',index=0)

# xtick=[1,2,3,4,5,6,7,8,9,10,13,16,20,23]
# # plt.text(5,np.log10(0.003),f'Data updated on {today}', fontsize=10)
# # plt.text(5,np.log10(0.003),f'Data updated on 2020-02-23', fontsize=10)
# # plt.xticks( np.log10(xtick),xtick)
# plt.ylabel('P(t)',fontsize=15)
# plt.xlabel('days',fontsize=15)
# plt.legend()
# # plt.savefig(f'testD-{pinyin(pl).capitalize()}-semilog-P(t)-days-{today}-with-fit.jpg', bbox_inches='tight')
# plt.show()

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