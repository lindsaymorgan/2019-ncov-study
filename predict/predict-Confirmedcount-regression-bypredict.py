import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from sklearn.linear_model import LinearRegression


today = datetime.date.today()-datetime.timedelta(days=1)
dt=pd.read_csv(f'../dxy-data/nice-dxy-data/country-day-summary-{today}.csv')
pr=pd.read_csv('Shiyan-country-predict-2020-02-28.csv')
dt['updateTime'] = pd.to_datetime(dt['updateTime'])
pr['updateTime'] = pd.to_datetime(pr['updateTime'])

dt.index=dt.updateTime
# dt=dt.reindex(dt.index + [datetime.datetime(2020, 2, i) for i in range(10,15)])
for i in range(20):
    dt=dt.append(pd.Series(name=today+datetime.timedelta(days=i)))
dt['updateTime'] =dt.index


# dt['updateTime'] = pd.to_datetime(dt['updateTime'])

dt['new_curedCount']=dt['country_curedCount']-dt['country_curedCount'].shift(1)
# dt=dt[dt['updateTime']!=datetime.datetime(2020,2,12)]
# dt.at[20, 'new_confirmedCount'] = np.mean([dt.at[i, 'new_confirmedCount'] for i in [19,20,21]])

for i in range(12,17):
    pr[f'y_best_Quanguo_delta_{i}']=pr['y_best_Quanguo_delta'].shift(i)
pr.dropna(how='any',inplace=True)
dt=pd.merge(dt,pr,how='right',on='updateTime')



X = dt[[f'y_best_Quanguo_delta_{i}' for i in range(12,17)]]
Y = dt.new_curedCount
cut=19
# X_train,X_test, y_train, y_test = train_test_split(X, y, random_state=1)
X_train=X[:-cut]
X_test=X[-cut:]
Y_train=Y[:-cut]
Y_test=Y[-cut:]
linreg = LinearRegression()
model=linreg.fit(X_train, Y_train)
Y_pred = linreg.predict(X)
print(linreg.coef_)



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

