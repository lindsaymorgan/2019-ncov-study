import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools as ts
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
from statsmodels.tsa.stattools import adfuller

from statsmodels.tsa.arima_model import ARIMA
import datetime

dt=pd.read_csv('../increase-log/country-day-summary-with-outsuspect.csv')
dt['updateTime'] = pd.to_datetime(dt['updateTime'])

dt.index=dt.updateTime
# dt=dt.reindex(dt.index + [datetime.datetime(2020, 2, i) for i in range(10,15)])
for i in range(10,13):
    dt=dt.append(pd.Series(name=datetime.datetime(2020, 2, i)))
dt['updateTime'] =dt.index
train=dt[0:12]
test=dt[12:]


y_hat_avg = test.copy()
fit1 = sm.tsa.statespace.ARIMA(train.R0, order=(2, 2, 0),seasonal_order=(0,1,1,7)).fit()
y_hat_avg['SARIMA'] = fit1.predict(start="2020-02-02", end="2020-02-13", dynamic=True)
plt.plot(train['R0'], label='Train',marker='o')
plt.plot(test['R0'], label='Test',marker='o')
plt.plot(y_hat_avg['SARIMA'], label='SARIMA',marker='o')
plt.xticks(rotation=45)
plt.title('Predict Confimedcount')
plt.xlabel('Updatetime')
plt.ylabel('Population')
plt.legend(loc='best')
plt.show()

# y_hat_avg.to_csv('Predict-Confimedcount-SARIMA.csv')
# plt.savefig('Predict-Confimedcount.jpg')

