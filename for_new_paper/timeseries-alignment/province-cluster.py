from tslearn.clustering import KShape
from tslearn.clustering import TimeSeriesKMeans
from tslearn.clustering import GlobalAlignmentKernelKMeans
import numpy as np
from tslearn.utils import to_time_series_dataset
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler


except_day = '2020-03-01'
data = pd.read_csv(f'../province-pivot-day-summary-{except_day}.csv' )
date=pd.read_csv('data_fig_S4B.csv')
date['level1 response']=pd.to_datetime(date['level1 response'])
response=dict([(a,b) for a,b in zip(date['Province'],date['level1 response'])])


data.index=data["provinceName-En"]
data.drop(columns=['provinceName-En','provinceName','distance-Wuhan'],inplace=True)
data=data.T

data.drop(columns=['Taiwan','Macau','HongKong','Xizang'],inplace=True)
data=data.fillna(value=0)
# raw=[data[i[0]].dropna()[data[i[0]].dropna()!=0] for i in country_first_list]
print(data.info())
# raw=[data[i].dropna()[data[i].dropna()!=0][:30] for i in data.columns]
raw=[data[i][(response[i]-datetime.datetime(2019,12,1)).days:(response[i]-datetime.datetime(2019,12,1)).days+30] for i in data.columns] #一级响应截开
raw=[np.subtract(i[1:],i[:-1]) for i in raw]  #计算新增

# raw=[[(j-min(i))/(max(i)-min(i)) for j in i] for i in raw] #min-max normalization
raw=[[(j-np.mean(i))/np.std(i) for j in i] for i in raw] #z normalization



# X_origin = to_time_series_dataset([np.subtract(i[1:],i[:-1]) for i in raw])
# scaler = MinMaxScaler()

# X = to_time_series_dataset([preprocessing.scale(np.subtract(i[1:],i[:-1])) for i in raw])
# X = to_time_series_dataset([preprocessing.scale(np.subtract(i[1:],i[:-1])) for i in raw])

X = to_time_series_dataset(raw)

# X = to_time_series_dataset([a-b for a,b in zip([data[i[0]].dropna()[data[i[0]].dropna()!=0] for i in country_first_list][1:],[data[i[0]].dropna()[data[i[0]].dropna()!=0] for i in country_first_list])][:-2])

kind=7

model = KShape(n_clusters=kind, n_init=1, random_state=3)
result = model.fit_predict(X)
print([(a,b) for a,b in zip([i for i in data.columns],result)])
sz = X.shape[1]
plt.figure(figsize=(15,6))
# plt.title('level1 response 30 days')
for yi in range(kind):
    plt.subplot(1, kind, yi + 1)
    for xx in X[result == yi]:
        plt.plot(xx.ravel(), "k-")
    plt.plot(model.cluster_centers_[yi].ravel(), "r-")
    # plt.xlim(0, sz)
    # plt.ylim(-4, 4)
    i = 0
    for a,b in  [(a,b) for a,b in zip([i for i in data.columns],result)]:
        if b==yi:
            y=0.95-0.05*i
            i=i+1
            plt.text(0.2, y,a, ha='center', va='center', color='r',transform=plt.gca().transAxes)

    plt.text(0.55, 0.85,'Cluster %d' % (yi + 1),
             transform=plt.gca().transAxes)

# plt.gcf().savefig('KShape-total.jpg',bbox_inches='tight')

plt.show()