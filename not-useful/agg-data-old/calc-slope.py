import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np

data=pd.read_csv('country-day-summary-excel.csv')
# country_data=pd.read_csv('country-day-summary-2020-02-11.csv')

# data['country_confirmedCount_increase_ratio']
# data['hubei_confirmedCount_increase_ratio']
# data['withouthubei_confirmedCount_increase_ratio']
# data=data.dropna(axis=0,how='any')
plt.figure(figsize=(9,6))

# for i in ['country','Hubei','withouthubei']:
#     plt.semilogy(data['updateTime'], data[f'{i}_confirmedCount_ratio'],marker='o',label=f'{i}')
#     popt, pcov =curve_fit(lambda t,a,b: a*np.exp(b*t),  list(range(len(data)))[-5:], data[f'{i}_confirmedCount_ratio'][-5:])
#     y2 = [popt[0]*np.exp(popt[1]*i) for i in list(range(len(data)))]
#     plt.semilogy(data['updateTime'],y2,'r--',label=f'{i}-fitting {round(popt[1],2)}')
#
# plt.xticks(rotation=45)
# plt.xlabel('Updatetime')
# plt.ylabel('Slope')
# # plt.title('cured')
# plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
# plt.savefig('country_slope_1.jpg',bbox_inches='tight')
# plt.show()

for i in ['country','hubei','withouthubei']:
    value = np.log10((data[f'{i}_confirmedCount_increase'] / data[f'{i}_confirmedCount_increase'].shift(1)).dropna())
    value=value.rolling(4).mean().dropna()
    # plt.semilogy(data['updateTime'][5:], value,marker='o',label=f'{i}')
    plt.plot(data['updateTime'][5:], value, marker='o', label=f'{i}')
    # popt, pcov =curve_fit(lambda t,a,b: a*np.exp(b*t),  list(range(len(data)))[5:], value)
    # y2 = [popt[0]*np.exp(popt[1]*i) for i in list(range(len(data)))]
    # plt.semilogy(data['updateTime'],y2,'r--',label=f'{i}-fitting {round(popt[1],2)}')

plt.xticks(rotation=45)
plt.xlabel('Updatetime')
plt.ylabel('Slope')
# plt.title('cured')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
# plt.savefig('country_slope_1.jpg',bbox_inches='tight')
plt.show()