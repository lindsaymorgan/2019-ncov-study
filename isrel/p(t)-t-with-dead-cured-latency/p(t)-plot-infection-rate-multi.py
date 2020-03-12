import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

today=datetime.date.today()-datetime.timedelta(days=3)
result=pd.read_csv(f'city_infection_2020-02-23.csv')
result=result[(result['infection_rate']<=2) & (result['infection_rate']>=0)]
data=pd.read_csv(f'../../dxy-data/nice-dxy-data/city-pivot-day-summary-{today}.csv')

plt.figure(figsize=(15,8))
bins=0.2
# base=int(np.floor(min(result['infection_rate'])/bins))
base=0
ceil=int(np.ceil(max(result['infection_rate'])/bins))

result1=result[result['cityName'].isin(['北京','上海','广州','深圳','成都','杭州','重庆','西安','苏州','天津','南京','长沙','郑州','东莞','青岛','沈阳','宁波','昆明'])]
infection=result1['infection_rate']


num_dict=dict.fromkeys([np.round(i*bins,1) for i in range(base,ceil+1)],0)
for i in infection:
    num_dict[np.round(np.round(i/bins)*bins,1)]+=1

plt.bar([i*4+1 for i in range(len(num_dict.keys()))],[i/18 for i in num_dict.values()],label='Large cities')



result1=result[result['provinceName']=='湖北省']
infection=result1['infection_rate']

num_dict=dict.fromkeys([np.round(i*bins,1) for i in range(base,ceil+1)],0)
for i in infection:
    num_dict[np.round(np.round(i/bins)*bins,1)]+=1

plt.bar([i*4+2 for i in range(len(num_dict.keys()))],[i/len(result1) for i in num_dict.values()],label='Hubei cities')



data=data[(data['provinceName']!='湖北省') & (~data['cityName'].isin(['北京','上海','广州','深圳','成都','杭州','重庆','武汉','西安','苏州','天津','南京','长沙','郑州','东莞','青岛','沈阳','宁波','昆明']))]
data.sort_values(by=f'{today-datetime.timedelta(days=1)}',inplace=True,ascending=False)
data=data[:30]
result1=result[result['cityName'].isin(data['cityName'])]
# result1=result[(result['provinceName']!='湖北省') & (~result['cityName'].isin(['北京','上海','广州','深圳','成都','杭州','重庆','武汉','西安','苏州','天津','南京','长沙','郑州','东莞','青岛','沈阳','宁波','昆明']))]
infection=result1['infection_rate']

num_dict=dict.fromkeys([np.round(i*bins,1) for i in range(base,ceil+1)],0)
for i in infection:
    num_dict[np.round(np.round(i/bins)*bins,1)]+=1

plt.bar([i*4+3 for i in range(len(num_dict.keys()))],[i/30 for i in num_dict.values()],label='Small cities')
plt.xticks([i*4+2 for i in range(len(num_dict.keys()))],num_dict.keys(),fontsize=20)
plt.yticks(fontsize=20)
plt.legend(fontsize=20)
plt.xlabel('InfectionRate',fontsize=25,fontstyle='italic')
plt.ylabel('${P_{InfectionRate}}$',fontsize=30)
plt.savefig(f'limit-city-infection-rate-multi-2020-02-23.jpg', bbox_inches='tight')
plt.show()