import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools as ts
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
from statsmodels.tsa.stattools import adfuller
import datetime

today = datetime.date.today()-datetime.timedelta(days=1)
dt=pd.read_csv(f'../dxy-data/nice-dxy-data/country-day-summary-{today}.csv')
dt['updateTime'] = pd.to_datetime(dt['updateTime'])
dt['updateTime'] = [i.date for i in dt['updateTime']]

dt.index=dt.updateTime
# dt=dt.reindex(dt.index + [datetime.datetime(2020, 2, i) for i in range(10,15)])
for i in range(5):
    dt=dt.append(pd.Series(name=datetime.date.today()+datetime.timedelta(days=i)))
dt['updateTime'] =dt.index
train=dt[0:-10]
test=dt[-10:]

y_hat_avg = test.copy()
fit1 = sm.tsa.statespace.SARIMAX(train.country_curedCount, order=(2, 2, 0),seasonal_order=(0,1,1,7)).fit()
y_hat_avg['SARIMA'] = fit1.predict(start=f"{today-datetime.timedelta(days=5)}", end=f"{today+datetime.timedelta(days=4)}", dynamic=True)
plt.plot(train['country_curedCount'], label='Train',marker='o')
plt.plot(test['country_curedCount'], label='Test',marker='o')
plt.plot(y_hat_avg['SARIMA'], label='SARIMA',marker='o')
plt.xticks(rotation=45)
plt.title('Predict curedCount')
plt.xlabel('Updatetime')
plt.ylabel('Population')
plt.legend(loc='best')
plt.show()
print(y_hat_avg['SARIMA'] )
# y_hat_avg.to_csv(f'Predict-curedcount-SARIMA-{today}.csv')
# plt.savefig(f'Predict-curedcount-{today}.jpg')

