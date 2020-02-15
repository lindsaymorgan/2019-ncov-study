import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

data=pd.read_csv('all-city-day-summary-2020-02-11.csv')
country_data=pd.read_csv('country-day-summary-2020-02-11.csv')

# data['country_confirmedCount_increase_ratio']
# data['hubei_confirmedCount_increase_ratio']
# data['withouthubei_confirmedCount_increase_ratio']
data=data.dropna(axis=0,how='any')
plt.figure(figsize=(9,6))

city_list=list(Counter(data['cityName']))
city=list()
a_list=list()
b_list=list()
for i in ['北京市','上海市','广州','武汉']:
    # plt.semilogy(data['updateTime'], data[f'{i}_confirmedCount_ratio'],marker='o',label=f'{i}')
    value = data[data['cityName'] == i]['city_confirmedCount'].rolling(4).mean()
    value=(value-value.shift(1)).dropna(axis=0,how='any')
    plt.semilogy(data[data['cityName'] == i]['updateTime'][4:], value,marker='o',label=f'{i}')
    try:
        popt, pcov =curve_fit(lambda t,a,b: a*np.exp(b*t),  list(range(3,len(data[data['cityName']==i])-1)), value)
        # popt= np.polyfit( list(range(2, len(data[data['cityName'] == i]) - 1)),
        #                        value, 1)
        city.append(i)
        a_list.append(popt[0])
        b_list.append(popt[1])
        y2 = [popt[0]*np.exp(popt[1]*i) for i in list(range(3,len(data[data['cityName']==i])-1))]
        plt.semilogy(data[data['cityName'] == i]['updateTime'][4:],y2,'r--',label=f'{i}-fitting {round(popt[1],2)}')
        print(popt,i)
        plt.show()
        plt.close()
    except:
        continue
#
# result=pd.DataFrame()
# result['city']=city
# result['a']=a_list
# result['b']=b_list
# result.to_csv('slope.csv',index=0)
    # y2 = [popt[0]*np.exp(popt[1]*i) for i in list(range(len(data)))]
    # plt.semilogy(data['updateTime'],y2,'r--',label=f'{i}-fitting {round(popt[1],2)}')

# plt.xticks(rotation=45)
# plt.xlabel('Updatetime')
# plt.ylabel('Slope')
# # plt.title('cured')
# plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
# plt.savefig('country_slope.jpg',index=0)
# plt.show()