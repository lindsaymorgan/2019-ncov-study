import pandas as pd
from scipy.optimize import curve_fit
import datetime
import matplotlib.pyplot as plt
import numpy as np
from itertools import compress
import statsmodels.api as sm

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif']=['Roman'] #用来正常显示中文标签
# today=datetime.date.today()-datetime.timedelta(days=1)
today=datetime.date(2020,3,1)
# date=today-datetime.timedelta(days=1)
date=today
# date=datetime.date(2020,2,17)
year=2010
tf=pd.read_csv('../../china_migration_2005_2010.csv')
tf.index=tf['provinceName']
tf=tf.T
tf=tf[3:-1]
tf['provinceName']=tf.index
# distance=pd.read_csv(f'../../dxy-data/nice-dxy-data/province-pivot-day-summary-{today}.csv')
distance=pd.read_csv(f'../../new-data-source/agged-record-data/province-pivot-day-summary-{today}.csv')
popu=pd.read_csv('../../province-population-2018.csv')
gdp=pd.read_csv('../../province-gdp-2018.csv')

distance=distance[['provinceName','distance-Wuhan',f'{date}']]
tf=tf[['provinceName','湖北省']]
gdp=gdp[['provinceName',f'{year}']]

data=pd.merge(popu,tf,on='provinceName',how='left')
data=pd.merge(data,distance,on='provinceName',how='left')

ax=plt.loglog(data['distance-Wuhan'],data['湖北省'],'o',color='red',label='')


x=np.log10(data['distance-Wuhan'])
# x=np.log10([a/b for a,b in zip(data['distance-Wuhan'],data[f'{year}-popu'])])
y=np.log10(list(data['湖北省']))
valid = ~(np.isnan(x) | np.isinf(x) | np.isnan(y) | np.isinf(y) )

#计算置信区间
X = sm.add_constant(list(compress(x, valid)))
mod = sm.OLS(list(compress(y, valid)), X)
# print(f'aic={mod.aic}')
res = mod.fit()
residual=res.resid
# print ('popu-migration-dist',res.params )
# print (res.conf_int(0.05)[1][1] )

X = sm.add_constant(list(compress(x, valid)))
mod=sm.WLS(list(compress(y, valid)), X,weights=[1/i**2 for i in residual])
res=mod.fit()
print ('popu-migration-dist',res.params )
popt=res.params
print (res.conf_int(0.05)[1][1] )
y2 = [popt[1] * ii + popt[0] for ii in [i*0.1 for i in range(24,36)]]
fit=plt.loglog([pow(10,i*0.1) for i in range(24,36)], np.power(10,y2), 'r--')

# popt, pcov = curve_fit(lambda t, k, b: k * t + b, list(compress(x, valid)),
#                            list(compress(y, valid)))
#
# y2 = [popt[0] * ii + popt[1] for ii in [i*0.1 for i in range(20,40)]]
# fit=plt.loglog([pow(10,i*0.1) for i in range(20,40)], np.power(10,y2), 'r--',label=f'slope={popt[0]:.2f}')
plt.xticks([4*10**2,10**3,3*10**3],[r'$4 \times 10^{2}$',r'$10^{3}$',r'$3 \times 10^{3}$'])
# plt.legend(fontsize=15)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.xlabel('r',fontsize=20)
plt.ylabel('Population Migration',fontsize=20)
# plt.text(pow(10,-1.4),pow(10,2.5),r'${\psi}=$'+f'{popt[0]:.2f}'+r'${\pm}$'+f'{res.conf_int(0.05)[1][1]-popt[0]:.2f}', fontsize=20)
plt.savefig('popu-migration-dist.jpg', bbox_inches='tight')
plt.show()
#
# plt.loglog(data[f'{year}-popu'],data['湖北省'],'o',color='cyan',label='')
# x=np.log10(data[f'{year}-popu'])
# # x=np.log10([a/b for a,b in zip(data['distance-Wuhan'],data[f'{year}-popu'])])
# y=np.log10(list(data['湖北省']))
# valid = ~(np.isnan(x) | np.isinf(x) | np.isnan(y) | np.isinf(y) )
#
# #计算置信区间
# X = sm.add_constant(list(compress(x, valid)))
# mod = sm.OLS(list(compress(y, valid)), X)
# # print(f'aic={mod.aic}')
# res = mod.fit()
# residual=res.resid
#
# X = sm.add_constant(list(compress(x, valid)))
# mod=sm.WLS(list(compress(y, valid)), X,weights=[1/i**2 for i in residual])
# res=mod.fit()
#
# print ('popu-migration-m',res.params )
# popt=res.params
# print (res.conf_int(0.05)[1][1] )
# y2 = [popt[1] * ii + popt[0] for ii in [i*0.1 for i in range(22,45)]]
# fit=plt.loglog([pow(10,i*0.1) for i in range(22,45)], np.power(10,y2), 'r--',label=f'slope={popt[1]:.2f}')
#
#
# # popt, pcov = curve_fit(lambda t, k, b: k * t + b, list(compress(x, valid)),
# #                            list(compress(y, valid)))
# #
# # y2 = [popt[0] * ii + popt[1] for ii in [i*0.1 for i in range(22,45)]]
# # fit=plt.loglog([pow(10,i*0.1) for i in range(22,45)], np.power(10,y2), 'r--',label=f'slope={popt[0]:.2f}')
# plt.legend(fontsize=15)
# plt.xticks(fontsize=18)
# plt.yticks(fontsize=18)
# plt.xlabel('m',fontsize=20)
# plt.ylabel('Population Migration',fontsize=20)
# # plt.text(pow(10,-1.4),pow(10,2.5),r'${\psi}=$'+f'{popt[0]:.2f}'+r'${\pm}$'+f'{res.conf_int(0.05)[1][1]-popt[0]:.2f}', fontsize=20)
# plt.savefig('popu-migration-m.jpg', bbox_inches='tight')
# plt.show()
