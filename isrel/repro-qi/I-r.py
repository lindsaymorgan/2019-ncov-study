import pandas as pd
from scipy.optimize import curve_fit
import datetime
import matplotlib.pyplot as plt
import numpy as np
from itertools import compress

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif']=['Arial'] #用来正常显示中文标签
today=datetime.date.today()-datetime.timedelta(days=1)
date=today
# date=datetime.date(2020,2,17)
year=2018
# data=pd.read_csv(f'../../dxy-data/nice-dxy-data/province-pivot-day-summary-{today}.csv')
popu=pd.read_csv('../../province-population-2018.csv')
data=pd.read_csv(f'../../new-data-source/agged-record-data/province-pivot-day-summary-{today}.csv')
data=data[~data['provinceName'].isin(['台湾省','香港特别行政区','澳门特别行政区'])]
data=data[['provinceName','distance-Wuhan',f'{date}']]

data=pd.merge(data,popu,on='provinceName',how='left')

#I-r/m

data1=data[~data['provinceName'].isin(['西藏自治区','湖北省'])]
plt.loglog([a/b for a,b in zip(data1['distance-Wuhan'],data1[f'{year}-popu'])],data1[f'{date}'],'o',label='')

x=np.log10([a/b for a,b in zip(data1['distance-Wuhan'],data1[f'{year}-popu'])])
y=np.log10(list(data1[f'{date}']))
valid = ~(np.isnan(x) | np.isinf(x) | np.isnan(y) | np.isinf(y) )
popt, pcov = curve_fit(lambda t, k, b: k * t + b, list(compress(x, valid)),
                           list(compress(y, valid)))

y2 = [popt[0] * i + popt[1] for i in list(compress(x, valid))]
fit=plt.plot(np.power(10,list(compress(x, valid))), np.power(10,y2), '--',label=f'slope {popt[0]:.2f}')
plt.legend(fontsize=12)

plt.xlabel('r/m',fontsize=15)
plt.ylabel('I',fontsize=15)
plt.savefig(f'I-r-m-{date}.jpg', bbox_inches='tight')
plt.show()


#I-r
# data1=data
# data1=data[~data['provinceName'].isin(['黑龙江省','安徽省','江西省','湖南省','西藏自治区','湖北省'])]
# plt.loglog(data1['distance-Wuhan'],data1[f'{date}'],'o',label='')
# x=np.log10(list(data1['distance-Wuhan']))
# y=np.log10(data1[f'{date}'])
# valid = ~(np.isnan(x) | np.isinf(x) | np.isnan(y) | np.isinf(y) )
# popt, pcov = curve_fit(lambda t, k, b: k * t + b, list(compress(x, valid)),
#                            list(compress(y, valid)))
#
# y2 = [popt[0] * i + popt[1] for i in list(compress(x, valid))]
# plt.plot(np.power(10,list(compress(x, valid))), np.power(10,y2), '--',label=f'slope {popt[0]:.2f}')
# plt.legend(fontsize=12)
#
# plt.xlabel('r',fontsize=15)
# plt.ylabel('I',fontsize=15)
# plt.savefig(f'I-r-{date}.jpg', bbox_inches='tight')
# plt.show()

#I-m

# data1=data[~data['provinceName'].isin(['辽宁省','海南省','西藏自治区','湖北省'])]
# plt.loglog(data1[f'{year}-popu'],data1[f'{date}'],'o',label='')
# x=np.log10(list(data1[f'{year}-popu']))
# y=np.log10(data1[f'{date}'])
# valid = ~(np.isnan(x) | np.isinf(x) | np.isnan(y) | np.isinf(y) )
# popt, pcov = curve_fit(lambda t, k, b: k * t + b, list(compress(x, valid)),
#                            list(compress(y, valid)))
#
# y2 = [popt[0] * i + popt[1] for i in list(compress(x, valid))]
# plt.plot(np.power(10,list(compress(x, valid))), np.power(10,y2), '--',label=f'slope {popt[0]:.2f}')
# plt.legend(fontsize=12)
#
# plt.xlabel('m',fontsize=15)
# plt.ylabel('I',fontsize=15)
# plt.savefig(f'I-m-{date}.jpg', bbox_inches='tight')
# plt.show()