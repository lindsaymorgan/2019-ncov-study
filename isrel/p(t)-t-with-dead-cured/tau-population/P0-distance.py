import pandas as pd
import matplotlib.pyplot as plt
import datetime

p=pd.read_csv('../city_infection_2020-02-23.csv')
popu=pd.read_csv('../../../city-population-area-2017.csv')
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
data=pd.merge(p,distance,on='cityName',how='left')
plt.loglog(data['distance-Wuhan'],data['infection_rate'],'o')
plt.xlabel('Distance from Wuhan',fontsize=15)
plt.ylabel('P(0)',fontsize=15)
plt.savefig(f'distance-P0.jpg', bbox_inches='tight')
plt.show()