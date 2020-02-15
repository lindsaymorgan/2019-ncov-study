import pandas as pd
import powerlaw
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from xpinyin import Pinyin

p = Pinyin()
pro_data=pd.read_csv('province-day-summary-2020-02-11.csv')
country_data=pd.read_csv('country-day-summary-2020-02-11.csv')
plt.figure(figsize=(9,6))

plt.semilogy(country_data['updateTime'],country_data['country_curedCount'],marker='o',label='curedCount')
# plt.semilogy(country_data['updateTime'],country_data['country_curedCount'],marker='o',label='curedCount')
plt.semilogy(country_data['updateTime'],pro_data[pro_data['provinceName']=='广东省']['province_curedCount'],marker='o',label='Guangdong curedCount')
plt.semilogy(country_data['updateTime'],pro_data[pro_data['provinceName']=='浙江省']['province_curedCount'],marker='o',label='Zhejiang curedCount')
plt.semilogy(country_data['updateTime'],pro_data[pro_data['provinceName']=='河南省']['province_curedCount'],marker='o',label='Henan curedCount')
plt.semilogy(country_data['updateTime'],pro_data[pro_data['provinceName']=='湖北省']['province_curedCount'],marker='o',label='Hubei curedCount')

popt, pcov =curve_fit(lambda t,a,b: a*np.exp(b*t),  list(range(len(country_data))), country_data['country_curedCount'])
y2 = [popt[0]*np.exp(popt[1]*i) for i in list(range(len(country_data)))]
plt.semilogy(country_data['updateTime'],y2,'r--',label=f'curedCount-fitting {round(popt[1],2)}')


for i in ['广东','浙江','河南','湖北']:
    popt, pcov =curve_fit(lambda t,a,b: a*np.exp(b*t),  list(range(len(country_data))), pro_data[pro_data['provinceName']==f'{i}省']['province_curedCount'])
    y2 = [popt[0]*np.exp(popt[1]*i) for i in list(range(len(country_data)))]
    name=p.get_pinyin(f"{i}", "").capitalize()
    plt.semilogy(country_data['updateTime'],y2,'r--',label=f'{name}curedCount {round(popt[1],2)}')

plt.xticks(rotation=45)
plt.xlabel('Updatetime')
plt.ylabel('Population')
plt.title('cured')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
# plt.show()
# # fit.power_law.plot_pdf()
plt.savefig('curedCount_fit_summary_log.jpg',bbox_inches='tight')
#
# plt.figure(figsize=(9,6))
# plt.semilogy(country_data['updateTime'],country_data['country_curedCount'],marker='o',label='curedCount')
# plt.semilogy(country_data['updateTime'],pro_data[pro_data['provinceName']=='广东省']['province_curedCount'],marker='o',label='Guangdong curedCount')
# plt.semilogy(country_data['updateTime'],pro_data[pro_data['provinceName']=='浙江省']['province_curedCount'],marker='o',label='Zhejiang curedCount')
# plt.semilogy(country_data['updateTime'],pro_data[pro_data['provinceName']=='河南省']['province_curedCount'],marker='o',label='Henan curedCount')
# plt.semilogy(country_data['updateTime'],pro_data[pro_data['provinceName']=='湖北省']['province_curedCount'],marker='o',label='Hubei curedCount')
# plt.title('Cured')
# plt.xticks(rotation=45)
# plt.xlabel('Updatetime')
# plt.ylabel('Population')
# plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
# # plt.show()
# plt.savefig('curedCount_summary_log.jpg',bbox_inches='tight')