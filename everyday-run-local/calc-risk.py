import pandas as pd
import datetime
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
today= datetime.date.today()-datetime.timedelta(days=1)

qianxi=pd.read_csv(f'./country-data/baiduqianxi_country_level_20{today.strftime("%y%m%d")}.csv')
raw_data=pd.read_csv(f'../dxy-data/nice-dxy-data/province-day-summary-{today}.csv')

data=raw_data[raw_data['updateTime']==f'{today}'][['provinceName','province_confirmedCount']]
data=data.merge(qianxi, on=('provinceName'))
data['ill_rate']=data['province_confirmedCount']/sum(data['province_confirmedCount'])
data['move_out_ill_rate']=[a*b for a,b in zip(data['move_out'],data['ill_rate'])]
overall=sum(data['move_out_ill_rate'])
data['risk']=[0]*len(data)
for i,row in data.iterrows():
    data.at[i,'risk']=row['move_in']*(overall-row['move_out_ill_rate'])
data.sort_values(by='risk',ascending=False,inplace=True)

data=data[:10]
city_name = list(data['provinceName'])
city_name.reverse()
data = list(data['risk'])
data.reverse()

plt.barh(range(len(data)), data,color='#ff4c00')
plt.yticks(range(len(city_name)),city_name,fontsize='13')
plt.xticks()


plt.title('疫情风险值前十名', loc='center', fontsize='20',
          fontweight='bold')
plt.savefig(f'./result/risk-top10-{today}.jpg', bbox_inches='tight')