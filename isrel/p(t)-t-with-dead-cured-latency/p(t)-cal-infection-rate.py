import pandas as pd
import datetime
import seaborn as sn
import numpy as np
import math
import pypinyin
from itertools import compress
import matplotlib.pyplot as plt

today=datetime.date(2020,3,1)
# today=datetime.date.today()-datetime.timedelta(days=1)
# data=pd.read_csv(f'../../dxy-data/nice-dxy-data/city-pivot-day-summary-{today}.csv')
# data.sort_values(by='2020-02-21',inplace=True,ascending=False)
data=pd.read_csv(f'../../new-data-source/agged-record-data/city-confirmed-pivot-day-summary-{today}.csv')
data_D=pd.read_csv(f'../../new-data-source/agged-record-data/city-D-pivot-day-summary-{today}.csv')
data.sort_values(by=f'{today}',inplace=True)

city_list=list()
infection=list()
data_D.drop(columns=[f'{datetime.date(2019,12,1)+datetime.timedelta(days=i)}' for i in range((datetime.datetime(2020,1,23)-datetime.datetime(2019,12,1)).days)],inplace=True)

for r,pl in enumerate(data['cityName']):
    city = data[data['cityName'] == pl]
    record = city.values.tolist()[0][:-7]

    city_D = data_D[data_D['cityName'] == pl]
    record_D = city_D.values.tolist()[0][:-2]

    record1 = [a - b for a, b in zip(record[1:], record[:-1])]
    record2 = [a - b for a, b in zip(record, record_D)]
    v = [np.float64(m) / n for (m, n) in zip(record1, record2)]

    # r_list=[x for x in r_list if str(x) != 'nan']
    valid = ~(np.isnan(v) | np.isinf(v))
    v=list(compress(v,valid))
    if len(v)>=5:
        city_list.append(pl)
        infection.append(np.mean(v[:5]))

city_infection=pd.DataFrame()
city_infection['cityName']=city_list
city_infection['infection_rate']=infection

# city_infection=pd.merge(city_infection,data[['cityName','provinceName']],on='cityName',how='left')
city_infection.to_csv(f'city_infection_I_D_{today}.csv',index=0,encoding='utf-8-sig',sep=',')

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
