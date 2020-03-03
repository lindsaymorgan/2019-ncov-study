import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from sklearn.linear_model import LinearRegression


today = datetime.date.today()-datetime.timedelta(days=1)
dt=pd.read_csv(f'../dxy-data/nice-dxy-data/country-day-summary-{today}.csv')

dt['updateTime'] = pd.to_datetime(dt['updateTime'])

dt['new_confirmedCount']=dt['country_confirmedCount']-dt['country_confirmedCount'].shift(1)
dt['new_confirmedCount']=[(a+b+c)/3 for a,b,c in zip(dt['new_confirmedCount'],dt['new_confirmedCount'].shift(1),dt['new_confirmedCount'].shift(-1))]
dt['new_curedCount']=dt['country_curedCount']-dt['country_curedCount'].shift(1)
# dt=dt[dt['updateTime']!=datetime.datetime(2020,2,12)]
# dt.at[20, 'new_confirmedCount'] = np.mean([dt.at[i, 'new_confirmedCount'] for i in [19,20,21]])
for i in range(12,17):
    dt[f'new_confirmedCount_{i}']=dt['new_confirmedCount'].shift(i)
dt.dropna(how='any',inplace=True)
# dt=dt[dt['updateTime']!=datetime.datetime(2020,2,12)]
X = dt[[f'new_confirmedCount_{i}' for i in range(12,17)]]
Y = dt.new_curedCount
cut=5
# X_train,X_test, y_train, y_test = train_test_split(X, y, random_state=1)
X_train=X[:-cut]
X_test=X[-cut:]
Y_train=Y[:-cut]
Y_test=Y[-cut:]
linreg = LinearRegression()
model=linreg.fit(X_train, Y_train)
Y_pred = linreg.predict(X)



plt.plot(dt['updateTime'][len(Y_train):len(Y)],Y_test,'o-',label="test")
plt.plot(dt['updateTime'][:len(Y_pred)],Y_pred,'o-',label="predict")
plt.plot(dt['updateTime'][:len(Y_train)],Y_train,'o-',label="fit")
plt.xticks(rotation=45)
plt.title('Predict curedCount')
plt.xlabel('Updatetime')
plt.ylabel('curedCount')
plt.legend(loc='best')
# plt.savefig(f'Predict-regression-curedcount-{today}.jpg')
plt.show()

# y_hat_avg.to_csv(f'Predict-curedcount-SARIMA-{today}.csv')
# plt.savefig(f'Predict-regression-curedcount-{today}.jpg')

