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
# today=datetime.date.today()-datetime.timedelta(days=1)
today=datetime.date(2020,3,1)
data=pd.read_csv(f'../../new-data-source/agged-record-data/city-confirmed-pivot-day-summary-{today}.csv')
data_D=pd.read_csv(f'../../new-data-source/agged-record-data/city-D-pivot-day-summary-{today}.csv')
data.sort_values(by=f'{today}',inplace=True)
data=data[data[f'{today}']>=50]
data.fillna(0, inplace=True)
data_D.fillna(0, inplace=True)
# day=np.log10(list(range(1,(today-datetime.date(2020,1,23)).days)))
# data=pd.read_csv('province-pivot-day-summary-2020-02-18.csv')
# data=pd.read_csv(f'../../dxy-data/nice-dxy-data/city-pivot-day-summary-2020-02-18.csv')
# day=np.log10(list(range(1,(datetime.datetime.today().date()-datetime.date(2020,1,24)).days)))
day=list(range(0,(today-datetime.date(2020,1,23)).days))
cut=6
plt.figure(figsize=(15,8))
#'北京','上海','广州','深圳'
#'合肥','重庆','长沙','南昌','哈尔滨'
#g'广州','深圳','珠海','成都','台州','威海','保定','金华'
#'武汉','孝感','黄冈','随州','荆州'

def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s

k_list=list()
b_list=list()
city_list=list()
latent=4
# data_D.drop(columns=[f'{datetime.date(2019,12,1)+datetime.timedelta(days=i)}' for i in range((datetime.datetime(2020,1,23)-datetime.datetime(2019,12,1)).days)],inplace=True)
for r,pl in enumerate(data['cityName']): #data['cityName']
    city = data[data['cityName'] == pl]
    record = city.values.tolist()[0][:-9]

    city_D = data_D[data_D['cityName'] == pl]
    record_D = city_D.values.tolist()[0][:-4]

    # final=record[-1]
    record1 = [a - b for a, b in zip(record[latent:], record[:-latent])]
    record2 = [a - b for a, b in zip(record[:-latent], record_D[:-latent])]
    v = np.log10([np.float64(m) / n for (m, n) in zip(record1, record2)])

    try:
        valid = ~(np.isnan(v[cut:]) | np.isnan(day[cut+latent-1:]) | np.isinf(v[cut:]) | np.isinf(
            day[cut+latent-1:]))
        popt, pcov = curve_fit(lambda t, k, b: k * t + b, list(compress(day[cut+latent-1:], valid)),
                               list(compress(v[cut :], valid)))
        k_list.append(popt[0])
        b_list.append(popt[1])
        city_list.append(pl)
    except:
        continue

result=pd.DataFrame()
result['k']=k_list
result['tau']=[-1/i for i in k_list]
result['b']=b_list
result['cityName']=city_list
result=pd.merge(result,data[['cityName','provinceName',f'{today}']],on='cityName',how='left')
result.to_csv(f'latency{latent+1}-p(t)-slope-I-D-{today}.csv',index=0,encoding='utf-8-sig',sep=',')
# print(min(k_list),max(k_list))
#
# base=int(np.floor(min(k_list)/0.02))
# ceil=int(np.ceil(max(k_list)/0.02))
# num_dict=dict.fromkeys([round(i*0.02,2) for i in range(base,ceil+1)],0)
# for i in k_list:
#     # num_dict[np.round(i, 1)] += 1
#     num_dict[np.round(np.round(i/0.02)*0.02,2)]+=1
# # sn.distplot(infection,bins = 10,hist = True,kde = False,norm_hist=False,
# #             rug = True,vertical = False,
# #             color = 'y',label = 'distplot',axlabel = 'x')
# plt.bar(range(len(num_dict.keys())),num_dict.values())
# plt.xticks(range(len(num_dict.keys())),num_dict.keys(),rotation=90)
# plt.text(2,30,f'Update on {today-datetime.timedelta(days=1)}', fontsize=10)
# plt.xlabel('decaying exponent')
# plt.ylabel('citynum')
# plt.savefig('decaying-exponent-hist-0.02.jpg', bbox_inches='tight')
# plt.show()

