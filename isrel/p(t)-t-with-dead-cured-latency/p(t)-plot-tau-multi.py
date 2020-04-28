import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

# today=datetime.date.today()-datetime.timedelta(days=1)
today=datetime.date(2020,3,1)
latent=5
result=pd.read_csv(f'latency{latent}-p(t)-slope-I-D-{today}.csv')
# result=pd.read_csv(f'p(t)-slope-2020-02-26.csv')
I_limit=50
result=result[result[f'{today}']>=I_limit]
result=result[(result['k']>=-0.35) & (result['k']<0)]
result['tau']=[-1/i for i in result['k']]
result=result[(result['tau']<=40) & (result['tau']>=0)]
# data=pd.read_csv(f'../../dxy-data/nice-dxy-data/city-pivot-day-summary-{today}.csv')
# data=pd.read_csv(f'../../dxy-data/nice-dxy-data/city-pivot-day-summary-{today}.csv')
bins=5
base=int(np.floor(min(result['tau'])/bins))
ceil=int(np.ceil(max(result['tau'])/bins))
num_dict=dict.fromkeys([round(i*bins,2) for i in range(base,ceil+1)],0)
# plt.figure(figsize=(15,8))
# result1=result[result['cityName'].isin(['北京','上海','广州','深圳','成都','杭州','重庆','西安','苏州','天津','南京','长沙','郑州','东莞','青岛','沈阳','宁波'])]
k_list=result['tau']
print(f'mean {np.mean(k_list)}')
print(f'std {np.std(k_list)}')
for i in k_list:
    num_dict[np.round(np.round(i/bins)*bins,2)]+=1

plt.bar([i for i in range(len(num_dict.keys()))],[i for i in num_dict.values()]) #/len(k_list)


# result1=result[result['provinceName']=='湖北省']
# k_list=result1['tau']
#
# num_dict=dict.fromkeys([round(i*bins,2) for i in range(base,ceil+1)],0)
# for i in k_list:
#     num_dict[np.round(np.round(i/bins)*bins,2)]+=1
#
# plt.bar([i*4+2 for i in range(len(num_dict.keys()))],[i/len(result1) for i in num_dict.values()],label='Hubei cities')
#
#
# data=data[(data['provinceName']!='湖北省') & (~data['cityName'].isin(['北京','上海','广州','深圳','成都','杭州','重庆','武汉','西安','苏州','天津','南京','长沙','郑州','东莞','青岛','沈阳','宁波','昆明']))]
# data.sort_values(by=f'{today-datetime.timedelta(days=1)}',inplace=True,ascending=False)
# data=data[:30]
# result1=result[result['cityName'].isin(data['cityName'])]
# # result1=result[(result['provinceName']!='湖北省') & (~result['cityName'].isin(['北京','上海','广州','深圳','成都','杭州','重庆','武汉','西安','苏州','天津','南京','长沙','郑州','东莞','青岛','沈阳','宁波','昆明']))]
# k_list=result1['tau']
#
# num_dict=dict.fromkeys([round(i*bins,2) for i in range(base,ceil+1)],0)
# for i in k_list:
#     num_dict[np.round(np.round(i/bins)*bins,2)]+=1
# plt.bar([i*4+3 for i in range(len(num_dict.keys()))],[i/30 for i in num_dict.values()],label='Small cities')

plt.xticks([i for i in range(len(num_dict.keys()))],num_dict.keys(),fontsize=18)
plt.yticks(fontsize=18)
# plt.title(f'limit I>={I_limit}',fontsize=30)

# plt.text(5,10,f'Data update on {today-datetime.timedelta(days=2)}', fontsize=10)
# plt.legend(fontsize=20)
plt.xlabel(r'${\tau}$',fontstyle='italic',fontsize=20)
# plt.ylabel(r'$P({\tau})$',fontsize=30)
plt.ylabel(r'citynum',fontsize=20)
plt.savefig(f'latency{latent}-limit-I{I_limit}-multi-cities-hist-{today}.jpg', bbox_inches='tight')
plt.show()