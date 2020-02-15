import pandas as pd
import powerlaw
import matplotlib.pyplot as plt
import numpy as np

pro_data=pd.read_csv('province-day-summary-2020-02-11.csv')
country_data=pd.read_csv('country-day-summary-2020-02-11.csv')
plt.figure(figsize=(9,6))

plt.semilogy(country_data['updateTime'],country_data['country_confirmedCount'],marker='o',label='confirmedCount')
plt.semilogy(country_data['updateTime'],pro_data[pro_data['provinceName']=='广东省']['province_confirmedCount'],marker='o',label='Guangdong confirmedCount')
plt.semilogy(country_data['updateTime'],pro_data[pro_data['provinceName']=='浙江省']['province_confirmedCount'],marker='o',label='Zhejiang confirmedCount')
plt.semilogy(country_data['updateTime'],pro_data[pro_data['provinceName']=='河南省']['province_confirmedCount'],marker='o',label='Henan confirmedCount')
plt.semilogy(country_data['updateTime'],pro_data[pro_data['provinceName']=='湖北省']['province_confirmedCount'],marker='o',label='Hubei confirmedCount')

plt.xticks(rotation=45)
plt.xlabel('Updatetime')
plt.ylabel('Population')
plt.title('Confirmed')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
fit=powerlaw.Fit(country_data['country_confirmedCount'])
# plt.show()
# fit.power_law.plot_pdf()
plt.savefig('confirmedCount_summary_log.jpg',bbox_inches='tight')

plt.figure(figsize=(9,6))
plt.semilogy(country_data['updateTime'],country_data['country_curedCount'],marker='o',label='curedCount')
plt.semilogy(country_data['updateTime'],pro_data[pro_data['provinceName']=='广东省']['province_curedCount'],marker='o',label='Guangdong curedCount')
plt.semilogy(country_data['updateTime'],pro_data[pro_data['provinceName']=='浙江省']['province_curedCount'],marker='o',label='Zhejiang curedCount')
plt.semilogy(country_data['updateTime'],pro_data[pro_data['provinceName']=='河南省']['province_curedCount'],marker='o',label='Henan curedCount')
plt.semilogy(country_data['updateTime'],pro_data[pro_data['provinceName']=='湖北省']['province_curedCount'],marker='o',label='Hubei curedCount')
plt.title('Cured')
plt.xticks(rotation=45)
plt.xlabel('Updatetime')
plt.ylabel('Population')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
# plt.show()
plt.savefig('curedCount_summary_log.jpg',bbox_inches='tight')