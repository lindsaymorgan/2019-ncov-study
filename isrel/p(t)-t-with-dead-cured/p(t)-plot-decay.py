import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

today=datetime.date.today()-datetime.timedelta(days=1)
result=pd.read_csv(f'p(t)-slope-2020-02-23.csv')
data=pd.read_csv(f'../../dxy-data/nice-dxy-data/city-pivot-day-summary-{today}.csv')

# result1=result[result['cityName'].isin(['北京','上海','广州','深圳','成都','杭州','重庆','西安','苏州','天津','南京','长沙','郑州','东莞','青岛','沈阳','宁波','昆明'])]
# k_list=result1['k']
# print(min(k_list),max(k_list))
# bins=0.01
# base=int(np.floor(min(k_list)/bins))
# ceil=int(np.ceil(max(k_list)/bins))
# num_dict=dict.fromkeys([round(i*bins,2) for i in range(base,ceil+1)],0)
# for i in k_list:
#     # num_dict[np.round(i, 1)] += 1
#     num_dict[np.round(np.round(i/bins)*bins,2)]+=1
# # sn.distplot(infection,bins = 10,hist = True,kde = False,norm_hist=False,
# #             rug = True,vertical = False,
# #             color = 'y',label = 'distplot',axlabel = 'x')
# plt.bar(range(len(num_dict.keys())),num_dict.values())
# plt.xticks(range(len(num_dict.keys())),num_dict.keys(),rotation=90)
# plt.text(0,5,f'Data update on {today-datetime.timedelta(days=1)}', fontsize=10)
# plt.title('big cities')
# plt.xlabel('decaying exponent')
# plt.ylabel('citynum')
# plt.savefig(f'decaying-exponent-big-cities-hist-{today}.jpg', bbox_inches='tight')
# plt.show()
#
# result1=result[result['provinceName']=='湖北省']
# k_list=result1['k']
# print(min(k_list),max(k_list))
# base=int(np.floor(min(k_list)/bins))
# ceil=int(np.ceil(max(k_list)/bins))
# num_dict=dict.fromkeys([round(i*bins,2) for i in range(base,ceil+1)],0)
# for i in k_list:
#     # num_dict[np.round(i, 1)] += 1
#     num_dict[np.round(np.round(i/bins)*bins,2)]+=1
# # sn.distplot(infection,bins = 10,hist = True,kde = False,norm_hist=False,
# #             rug = True,vertical = False,
# #             color = 'y',label = 'distplot',axlabel = 'x')
# plt.bar(range(len(num_dict.keys())),num_dict.values())
# plt.xticks(range(len(num_dict.keys())),num_dict.keys(),rotation=90)
# plt.text(0,4,f'Data update on {today-datetime.timedelta(days=1)}', fontsize=10)
# plt.title('Cities in Hubei')
# plt.xlabel('decaying exponent')
# plt.ylabel('citynum')
# plt.savefig(f'decaying-exponent-hubei-cities-hist-{today}.jpg', bbox_inches='tight')
# plt.show()

# data=data[(data['provinceName']!='湖北省') & (~data['cityName'].isin(['北京','上海','广州','深圳','成都','杭州','重庆','武汉','西安','苏州','天津','南京','长沙','郑州','东莞','青岛','沈阳','宁波','昆明']))]
data.sort_values(by=f'{today-datetime.timedelta(days=1)}',inplace=True,ascending=False)
data=data[:30]
result1=result[result['cityName'].isin(data['cityName'])]
# result1=result[(result['provinceName']!='湖北省') & (~result['cityName'].isin(['北京','上海','广州','深圳','成都','杭州','重庆','武汉','西安','苏州','天津','南京','长沙','郑州','东莞','青岛','沈阳','宁波','昆明']))]
k_list=result1['k']
bins=0.01
print(min(k_list),max(k_list))
base=int(np.floor(min(k_list)/bins))
ceil=int(np.ceil(max(k_list)/bins))
num_dict=dict.fromkeys([round(i*bins,2) for i in range(base,ceil+1)],0)
for i in k_list:
    # num_dict[np.round(i, 1)] += 1
    num_dict[np.round(np.round(i/bins)*bins,2)]+=1
# sn.distplot(infection,bins = 10,hist = True,kde = False,norm_hist=False,
#             rug = True,vertical = False,
#             color = 'y',label = 'distplot',axlabel = 'x')
plt.bar(range(len(num_dict.keys())),num_dict.values())
plt.xticks(range(len(num_dict.keys())),num_dict.keys(),rotation=90)
plt.text(5,10,f'Data update on {today-datetime.timedelta(days=2)}', fontsize=10)
plt.title('Top30 small cities')
plt.xlabel('decaying exponent')
plt.ylabel('citynum')
plt.savefig(f'decaying-exponent-top30-other-cities-hist-2020-02-23.jpg', bbox_inches='tight')
plt.show()