import pandas as pd
import datetime
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# today = datetime.date.today()
today=datetime.date(2020,4,2)
yesterday=today-datetime.timedelta(days=1)
data=pd.read_csv(f'./agged-record-data/country-day-summary-{yesterday}.csv')
data['date'] = pd.to_datetime(data['date'])

grouped=data.groupby('country')

total=grouped['confirmed'].agg(np.max)
total=total[total>=15000]



for name,group in grouped:
    if name in total.index:

        group['newly confirmed'] = -group['confirmed'].shift(1) + group['confirmed']
        group.dropna(how='any',inplace=True)
        group['rolling newly confirmed']=group['newly confirmed'].rolling(window=5).mean()
        group['log newly confirmed']=[np.log10(x) for x in group['rolling newly confirmed']]
        group['slope']=(-group['log newly confirmed'].shift(1)+group['log newly confirmed'].shift(-1))/2
        group['day']=[(i-list(group['date'])[0]).days+1 for i in group['date']]

        max_day=list(group[group['newly confirmed']==max(group['newly confirmed'])]['day'])[0]
        steady_day=max_day-max(group['day'])
        print(name,steady_day)
        # plt.plot(group['day'], group['slope'], 'ro-')
        # plt.title(name)
        # plt.show()
        # plt.close()

        # plt.plot(group['day'], group['slope'], 'o-', label=name)
        plt.semilogy(group['day'], group['newly confirmed'], '-',label=name)

plt.legend()
plt.show()
plt.close()