import pandas as pd
from scipy.optimize import curve_fit
import datetime
import matplotlib.pyplot as plt
import numpy as np
from itertools import compress

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif']=['Arial'] #用来正常显示中文标签
today=datetime.date.today()-datetime.timedelta(days=1)
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

plt.loglog([a/b for a,b in zip(data['distance-Wuhan'],data[f'{year}-popu'])],data['湖北省'],'o',color='darkviolet',label='')


x=np.log10([a/b for a,b in zip(data['distance-Wuhan'],data[f'{year}-popu'])])
y=np.log10(list(data['湖北省']))
valid = ~(np.isnan(x) | np.isinf(x) | np.isnan(y) | np.isinf(y) )
popt, pcov = curve_fit(lambda t, k, b: k * t + b, list(compress(x, valid)),
                           list(compress(y, valid)))

y2 = [popt[0] * i + popt[1] for i in list(compress(x, valid))]
fit=plt.plot(np.power(10,list(compress(x, valid))), np.power(10,y2), 'r--',label=f'slope {popt[0]:.2f}')
plt.legend(fontsize=12)
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
plt.xlabel('r/m',fontsize=15)
plt.ylabel('Population Migration',fontsize=15)
plt.savefig('popu-migration-dist-popu.jpg', bbox_inches='tight')
plt.show()


plt.loglog(data['湖北省'],data[f'{date}'],'o',color='yellowgreen',label='')

data=data[data['provinceName']!='西藏自治区']
x=np.log10(list(data['湖北省']))
y=np.log10(data[f'{date}'])
valid = ~(np.isnan(x) | np.isinf(x) | np.isnan(y) | np.isinf(y) )
popt, pcov = curve_fit(lambda t, k, b: k * t + b, list(compress(x, valid)),
                           list(compress(y, valid)))

y2 = [popt[0] * i + popt[1] for i in list(compress(x, valid))]
plt.plot(np.power(10,list(compress(x, valid))), np.power(10,y2), 'r--',label=f'slope {popt[0]:.2f}')
plt.legend(fontsize=12)
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
plt.xlabel('Population Migration',fontsize=15)
plt.ylabel('I',fontsize=15)
plt.savefig(f'I-popu-migration-{date}.jpg', bbox_inches='tight')
plt.show()