import pandas as pd
import datetime
import seaborn as sn
import numpy as np
import math
import pypinyin
from itertools import compress
import matplotlib.pyplot as plt

today=datetime.date.today()-datetime.timedelta(days=1)
data=pd.read_csv(f'../../dxy-data/nice-dxy-data/city-pivot-day-summary-2020-02-20.csv')
data.sort_values(by='2020-02-18',inplace=True,ascending=False)
# data=pd.read_csv(f'../../city-pivot-day-summary-2020-02-20.csv')
# data.sort_values(by='2020/2/19',inplace=True,ascending=False)

city_list=list()
infection=list()
for i,r in data[:100].iterrows():
    # city = data[data['cityName-ch'] == r['cityName']]
    r_list=list(r)
    r_list=[x for x in r_list if str(x) != 'nan']
    record = r_list[:-8]
    # final=record[-1]
    record1 = [a - b for a, b in zip(record[1:], record[:-1])]
    v = [m / n for (m, n) in zip(record1, record)]
    # if -np.inf in v[:5]:
    #     continue
    city_list.append(data['cityName'][i])
    infection.append(np.mean(v[:5]))

city_infection=pd.DataFrame()
city_infection['cityName']=city_list
city_infection['infection_rate']=infection
city_infection.to_csv('city_infection_new.csv',index=0,encoding='utf-8-sig',sep=',')

# base=int(np.floor(min(infection)/0.1))
# ceil=int(np.ceil(max(infection)/0.1))
# num_dict=dict.fromkeys([np.round(i*0.1,1) for i in range(base,ceil+1)],0)
base=int(np.floor(min(infection)/0.2))
ceil=int(np.ceil(max(infection)/0.2))
num_dict=dict.fromkeys([np.round(i*0.2,1) for i in range(base,ceil+1)],0)
for i in infection:
    # num_dict[np.round(i, 1)] += 1
    num_dict[np.round(np.round(i/0.2)*0.2,1)]+=1
# sn.distplot(infection,bins = 10,hist = True,kde = False,norm_hist=False,
#             rug = True,vertical = False,
#             color = 'y',label = 'distplot',axlabel = 'x')
plt.bar(range(len(num_dict.keys())),num_dict.values())
plt.xticks(range(len(num_dict.keys())),num_dict.keys(),rotation=60)
# plt.title('infection rate')
plt.xlabel('infection rate')
plt.ylabel('citynum')
plt.savefig('city-infection-rate-hist-0.2.jpg', bbox_inches='tight')
plt.show()
#     bins = [i/10 for i in list(range(int(np.floor(min(data)*10)), int(np.ceil(max(data)*10 + bins_interval*10 - 1)), 1))]
#     print(len(bins))
#     for i in range(0, len(bins)):
#         print(bins[i])
#     plt.xlim(min(data) - margin, max(data) + margin)
#     plt.title("Probability-distribution")
#     plt.xlabel('Interval')
#     plt.ylabel('Probability')
#     # 频率分布normed=True，频次分布normed=False
#     prob,left,rectangle = plt.hist(x=data, bins=bins, normed=True, histtype='bar', color=['r'],edgecolor='black')
#     for x, y in zip(left, prob):
#         # 字体上边文字
#         # 频率分布数据 normed=True
#         plt.text(x + bins_interval / 2, y + 0.003, '%.2f' % y, ha='center', va='top')
#         # 频次分布数据 normed=False
#         # plt.text(x + bins_interval / 2, y + 0.25, '%.2f' % y, ha='center', va='top')
#     plt.show()
# probability_distribution(data=infection, bins_interval=0.1,margin=0)
# plt.hist(infection,10,normed=1,histtype='bar')
# plt.show()