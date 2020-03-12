from scipy import stats
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
data=pd.read_csv(f'../../../new-data-source/agged-record-data/city-confirmed-pivot-day-summary-{today}.csv')
data_D=pd.read_csv(f'../../../new-data-source/agged-record-data/city-D-pivot-day-summary-{today}.csv')
# day=np.log10(list(range(1,(datetime.datetime.today().date()-datetime.date(2020,1,24)).days)))
day=list(range(0,(today-datetime.date(2020,1,23)).days))
cut=8

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
    v2_raw = [np.float64(m) / n for (m, n) in zip(record1, record2)]
    v2 = np.log10([np.float64(m) / n for (m, n) in zip(record1, record2)])

    try:
        valid = ~(np.isnan(v2[cut:]) | np.isnan(day[cut:]) | np.isinf(v2[cut:]) | np.isinf(day[cut:]))

        X = sm.add_constant(list(compress(day[cut:], valid)))
        mod = sm.OLS(list(compress(v2[cut:], valid)), X)
        res1 = mod.fit()
        # mod_result1=sm.regression.linear_model.OLSResults(mod,res.params)

        # print(f'exp aic={mod_result.aic}')

        valid = ~(np.isnan(v2[cut:]) | np.isnan(np.log10(day[cut:])) | np.isinf(v2[cut:]) | np.isinf(np.log10(day[cut:])))
        X = sm.add_constant(list(compress(np.log10(day[cut:]), valid)))
        mod = sm.OLS(list(compress(v2[cut:], valid)), X)
        res2 = mod.fit()
        # mod_result2=sm.regression.linear_model.OLSResults(mod,res.params)

        # if res1.aic!=-np.inf and res2.aic!=-np.inf:
        # cityName_list.append(f'{pinyin(pl).capitalize()}')
        # exp_aic.append(res1.aic+2*2*3/(len(v2)-2-1))
        # pl_aic.append(res2.aic+2*2*3/(len(v2)-2-1))
    except:
        continue


result=pd.DataFrame()
result['cityName-en']=cityName_list
result['exp_aic']=exp_aic
result['powerlaw_aic']=pl_aic
result=pd.merge(result,data[['cityName-en','provinceName-en']])

# result.to_csv('withoutinf-AIC-compare-exp-powerlaw.csv',index=0)
# result.to_csv('AIC-compare-exp-powerlaw.csv',index=0)

