import pandas as pd
import matplotlib.pyplot as plt
import datetime

tau=pd.read_csv('../p(t)-slope-2020-02-26.csv')
popu=pd.read_csv('../../../city-population-area-2017.csv')
data=pd.merge(tau,popu,on='cityName',how='left')
today=datetime.date.today()-datetime.timedelta(days=1)

# data1=data[data['provinceName']=='湖北省']
# data.dropna(axis='index',how='any',inplace=True)
# plt.loglog(data['Population'],data['tau'],'o')
# plt.xlabel('City Population',fontsize=15)
# plt.ylabel(r'${\tau}$',fontsize=20)
# plt.savefig('city-population-tau.jpg', bbox_inches='tight')
# plt.show()

distance=pd.read_csv(f'../../../dxy-data/nice-dxy-data/city-pivot-day-summary-{today}.csv')
distance=distance[['cityName','distance-Wuhan']]
data=pd.merge(tau,distance,on='cityName',how='left')
plt.loglog(data['distance-Wuhan'],data['tau'],'o')
plt.xlabel('Distance from Wuhan',fontsize=15)
plt.ylabel(r'${\tau}$',fontsize=20)
plt.savefig(f'distance-tau.jpg', bbox_inches='tight')
plt.show()