import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

# today=datetime.date.today()-datetime.timedelta(days=1)
today=datetime.date(2020,3,1)
result=pd.read_csv(f'city_infection_{today}.csv')
# data=pd.read_csv(f'../../dxy-data/nice-dxy-data/city-pivot-day-summary-{today}.csv')
result=result[(result['infection_rate']<=2) & (result['infection_rate']>=0)]
# result1=result[result['cityName'].isin(['北京','上海','广州','深圳','成都','杭州','重庆','西安','苏州','天津','南京','长沙','郑州','东莞','青岛','沈阳','宁波','昆明'])]
infection=result['infection_rate']
print(f'mean {np.mean(infection)}')
print(f'std {np.std(infection)}')

bins=0.2
base=int(np.floor(min(infection)/bins))
ceil=int(np.ceil(max(infection)/bins))
num_dict=dict.fromkeys([np.round(i*bins,1) for i in range(base,ceil+1)],0)
for i in infection:
    num_dict[np.round(np.round(i/bins)*bins,1)]+=1


plt.bar(range(len(num_dict.keys())),[i for i in num_dict.values()]) #/len(infection)
plt.xticks(range(len(num_dict.keys())),num_dict.keys(),fontsize=13)
plt.yticks(fontsize=13)
plt.xlabel(r'$P_{0}$',fontsize=15)
plt.ylabel('citynum',fontsize=15)
plt.savefig(f'P0-all-cities-{today}.jpg', bbox_inches='tight')
plt.show()