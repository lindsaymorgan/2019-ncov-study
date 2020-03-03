import pandas as pd
import datetime
import seaborn as sn
import numpy as np
import math
import pypinyin
from itertools import compress
import matplotlib.pyplot as plt

today=datetime.date(2020,2,23)
# today=datetime.date.today()-datetime.timedelta(days=1)
data=pd.read_csv(f'../../dxy-data/nice-dxy-data/city-pivot-day-summary-{today}.csv')
data.sort_values(by='2020-02-21',inplace=True,ascending=False)
# data=pd.read_csv(f'../../city-pivot-day-summary-2020-02-20.csv')
# data.sort_values(by='2020/2/19',inplace=True,ascending=False)

city_list=list()
infection=list()
P0=list()
for i,r in data.iterrows():
    # city = data[data['cityName-ch'] == r['cityName']]
    r_list=list(r)
    r_list=[x for x in r_list if str(x) != 'nan']
    record = r_list[:-8]
    if len(record)<6:
        continue
    # final=record[-1]
    try:
        record1 = [a - b for a, b in zip(record[1:], record[:-1])]
        v = [m / n for (m, n) in zip(record1, record)]
        # if -np.inf in v[:5]:
        #     continue
        city_list.append(data['cityName'][i])
        infection.append(np.mean(v[:5]))
        P0.append(v[0])
    except:
        continue

city_infection=pd.DataFrame()
city_infection['cityName']=city_list
city_infection['infection_rate']=infection
city_infection['P0']=P0
city_infection=pd.merge(city_infection,data[['cityName','provinceName']],on='cityName',how='left')
city_infection.to_csv(f'city_infection_{today}.csv',index=0,encoding='utf-8-sig',sep=',')

# base=int(np.floor(min(infection)/0.2))
# ceil=int(np.ceil(max(infection)/0.2))
# num_dict=dict.fromkeys([np.round(i*0.2,1) for i in range(base,ceil+1)],0)
# for i in infection:
#     num_dict[np.round(np.round(i/0.2)*0.2,1)]+=1
#
# plt.bar(range(len(num_dict.keys())),num_dict.values())
# plt.xticks(range(len(num_dict.keys())),num_dict.keys(),rotation=60)
# # plt.title('infection rate')
# plt.xlabel('infection rate')
# plt.ylabel('citynum')
# plt.savefig('city-infection-rate-hist-0.2.jpg', bbox_inches='tight')
# plt.show()
