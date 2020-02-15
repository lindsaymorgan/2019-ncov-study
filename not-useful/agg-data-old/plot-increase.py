import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from xpinyin import Pinyin

country_data=pd.read_csv('country-day-summary-2020-02-11.csv')
pro_data=pd.read_csv('province-day-summary-2020-02-11.csv')
city_data=pd.read_csv('city-day-summary-2020-02-11.csv')
p = Pinyin()
d=4
plt.figure(figsize=(9,6))
country_data['country_confirmedCount_increase-roll'] = (country_data["country_confirmedCount_increase"].shift(-1)+
                                                        country_data["country_confirmedCount_increase"].shift(-2)+
                                                        country_data["country_confirmedCount_increase"].shift(1)+country_data["country_confirmedCount_increase"])/4
# country_data["country_confirmedCount_increase"]/country_data["country_confirmedCount_increase"].shift(1)
plt.plot(country_data['updateTime'],np.log10(country_data["country_confirmedCount_increase-roll"]/country_data["country_confirmedCount_increase-roll"].shift(1)),marker='o',label='all')
# plt.plot(country_data['updateTime'],np.log10(country_data["country_confirmedCount"]/country_data["country_confirmedCount"].shift(1)),marker='o',label='all')
# plt.plot(country_data['updateTime'],np.log10(country_data["withouthubei_confirmedCount_increase"]/country_data["withouthubei_confirmedCount_increase"].shift(4)),marker='o',label='WithoutHubei')
#
#
# pro_data[pro_data['provinceName']==f'{i}']['province_confirmedCount_increase'].rolling(window=4).mean()
# for i in ['北京市','湖北省']:
#     name = p.get_pinyin(f"{i}", "").capitalize()
#     plt.plot(country_data['updateTime'],np.log10(pro_data[pro_data['provinceName']==f'{i}']['province_confirmedCount_increase']/pro_data[pro_data['provinceName']==f'{i}']['province_confirmedCount_increase'].shift(d)),marker='o',label=f'{name}')
# i='上海市'
# plt.plot(country_data['updateTime'][3:],np.log10(pro_data[pro_data['provinceName']==f'{i}']['province_confirmedCount_increase']/pro_data[pro_data['provinceName']==f'{i}']['province_confirmedCount_increase'].shift(d)),marker='o',label=f'{name}')
#
# for i in ['广州','武汉']:
#     name = p.get_pinyin(f"{i}", "").capitalize()
#     plt.plot(country_data['updateTime'],np.log10(city_data[city_data['cityName']==f'{i}']['city_confirmedCount_increase']/city_data[city_data['cityName']==f'{i}']['city_confirmedCount_increase'].shift(d)),marker='o',label=f'{name}')


plt.legend()
plt.title('confirmed increase')
plt.xticks(rotation=45)
plt.xlabel('Updatetime')
plt.ylabel('Population')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()

