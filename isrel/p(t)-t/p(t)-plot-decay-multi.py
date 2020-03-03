import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

today=datetime.date.today()-datetime.timedelta(days=3)
result=pd.read_csv(f'p(t)-slope-2020-02-23.csv')
result=result[(result['k']>=-0.2) & (result['k']<=0)]
data=pd.read_csv(f'../../dxy-data/nice-dxy-data/city-pivot-day-summary-{today}.csv')
bins=0.01
base=int(np.floor(-0.11/bins))
ceil=int(np.ceil(-0.04/bins))
num_dict=dict.fromkeys([round(i*bins,2) for i in range(base,ceil+1)],0)

result1=result[result['cityName'].isin(['北京','上海','广州','深圳','成都','杭州','重庆','西安','苏州','天津','南京','长沙','郑州','东莞','青岛','沈阳','宁波','昆明'])]
k_list=result1['k']

for i in k_list:
    num_dict[np.round(np.round(i/bins)*bins,2)]+=1

plt.bar([i*4+1 for i in range(len(num_dict.keys()))],[i/18 for i in num_dict.values()],label='Large cities')


result1=result[result['provinceName']=='湖北省']
k_list=result1['k']

num_dict=dict.fromkeys([round(i*bins,2) for i in range(base,ceil+1)],0)
for i in k_list:
    num_dict[np.round(np.round(i/bins)*bins,2)]+=1

plt.bar([i*4+2 for i in range(len(num_dict.keys()))],[i/len(result1) for i in num_dict.values()],label='Hubei cities')


data=data[(data['provinceName']!='湖北省') & (~data['cityName'].isin(['北京','上海','广州','深圳','成都','杭州','重庆','武汉','西安','苏州','天津','南京','长沙','郑州','东莞','青岛','沈阳','宁波','昆明']))]
data.sort_values(by=f'{today-datetime.timedelta(days=2)}',inplace=True,ascending=False)
data=data[:30]
result1=result[result['cityName'].isin(data['cityName'])]
# result1=result[(result['provinceName']!='湖北省') & (~result['cityName'].isin(['北京','上海','广州','深圳','成都','杭州','重庆','武汉','西安','苏州','天津','南京','长沙','郑州','东莞','青岛','沈阳','宁波','昆明']))]
k_list=result1['k']
num_dict=dict.fromkeys([round(i*bins,2) for i in range(base,ceil+1)],0)
for i in k_list:
    num_dict[np.round(np.round(i/bins)*bins,2)]+=1
plt.bar([i*4+3 for i in range(len(num_dict.keys()))],[i/30 for i in num_dict.values()],label='Small cities')

plt.xticks([i*4+2 for i in range(len(num_dict.keys()))],num_dict.keys())


# plt.text(5,10,f'Data update on {today-datetime.timedelta(days=2)}', fontsize=10)
plt.legend()
plt.xlabel('DecayingExponent',fontstyle='italic',fontsize=13)
plt.ylabel('$P_{DecayingExponent}$',fontsize=18)
plt.savefig(f'limit-decaying-exponent-multi-cities-hist-2020-02-23.jpg', bbox_inches='tight')
plt.show()