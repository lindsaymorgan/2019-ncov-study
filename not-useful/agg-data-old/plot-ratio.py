import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from xpinyin import Pinyin

country_data=pd.read_csv('country-day-summary-2020-02-11.csv')
pro_data=pd.read_csv('province-day-summary-2020-02-11.csv')
city_data=pd.read_csv('city-day-summary-2020-02-11.csv')
p = Pinyin()
d=1
# plt.figure(figsize=(9,6))
# country_data["country_confirmedCount_increase"]/country_data["country_confirmedCount_increase"].shift(1)
# plt.plot(country_data['updateTime'],np.log10(country_data["country_confirmedCount_increase"]/country_data["country_confirmedCount_increase"].shift(4)),marker='o',label='all')
plt.plot(country_data['updateTime'],np.log10(country_data["country_confirmedCount"]/country_data["country_confirmedCount"].shift(d)),marker='o',label='all')
# plt.plot(country_data['updateTime'],np.log10(country_data["withouthubei_confirmedCount_increase"]/country_data["withouthubei_confirmedCount_increase"].shift(4)),marker='o',label='WithoutHubei')
plt.plot(country_data['updateTime'],np.log10(country_data["withouthubei_confirmedCount"]/country_data["withouthubei_confirmedCount"].shift(d)),marker='o',label='WithoutHubei')


for i in ['北京市','湖北省']:
    name = p.get_pinyin(f"{i}", "").capitalize()
    # plt.plot(country_data['updateTime'],np.log10(pro_data[pro_data['provinceName']==f'{i}']['province_confirmedCount_increase']/pro_data[pro_data['provinceName']==f'{i}']['province_confirmedCount_increase'].shift(d)),marker='o',label=f'{name}')
    plt.plot(country_data['updateTime'], np.log10(
        pro_data[pro_data['provinceName'] == f'{i}']['province_confirmedCount'] /
        pro_data[pro_data['provinceName'] == f'{i}']['province_confirmedCount'].shift(d)), marker='o',
             label=f'{name}')

i='上海市'
name = p.get_pinyin(f"{i}", "").capitalize()
# plt.plot(country_data['updateTime'][3:],np.log10(pro_data[pro_data['provinceName']==f'{i}']['province_confirmedCount_increase']/pro_data[pro_data['provinceName']==f'{i}']['province_confirmedCount_increase'].shift(d)),marker='o',label=f'{name}')
plt.plot(country_data['updateTime'][3:],np.log10(pro_data[pro_data['provinceName']==f'{i}']['province_confirmedCount']/pro_data[pro_data['provinceName']==f'{i}']['province_confirmedCount'].shift(d)),marker='o',label=f'{name}')

for i in ['广州','武汉']:
    name = p.get_pinyin(f"{i}", "").capitalize()
    # plt.plot(country_data['updateTime'],np.log10(city_data[city_data['cityName']==f'{i}']['city_confirmedCount_increase']/city_data[city_data['cityName']==f'{i}']['city_confirmedCount_increase'].shift(d)),marker='o',label=f'{name}')
    plt.plot(country_data['updateTime'], np.log10(
        city_data[city_data['cityName'] == f'{i}']['city_confirmedCount'] /
        city_data[city_data['cityName'] == f'{i}']['city_confirmedCount'].shift(d)), marker='o',
             label=f'{name}')

plt.legend()
plt.title(f'confirmedCount d={d}')
plt.xticks(rotation=45)
plt.xlabel('Updatetime')
plt.ylabel('log10(Ratio)')
plt.legend()
# plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig(f'plot-ratio-{d}.jpg',bbox_inches='tight')
plt.show()

