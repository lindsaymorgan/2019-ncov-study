from tslearn.clustering import KShape
from tslearn.clustering import TimeSeriesKMeans
from tslearn.clustering import GlobalAlignmentKernelKMeans
import numpy as np
from tslearn.utils import to_time_series_dataset
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
import datetime


except_day = '2020-04-07'
data = pd.read_csv(f'../country_confirmed_{except_day}.csv' )

country_first_list=[('Italy','2020-01-30',60482200),('Korea, South','2020-01-20',51269185),('Germany','2020-01-27',82293457),('US','2020-01-21',326766748),('United Kingdom','2020-01-31',66573504),('Denmark','2020-02-27',5754356),
('Iran','2020-02-19',82011735),('Spain','2020-02-01',46397452),('France','2020-01-24',65233271),('Switzerland','2020-02-25',8544034),('Norway','2020-02-26',5353363),('Netherlands','2020-02-27',17084459),
('India','2020-01-30',1354051854),('Africa','2020-02-14',1340598000),('China','2019-12-08',1396984787),('Turkey','2020-03-11',82000000),('Belgium','2020-02-04',11422068),('Canada','2020-01-26',35151728),
('Portugal','2020-03-02',10276617),('Japan','2020-01-22',124800000),('Austria','2020-02-25',9000000),('Australia','2020-01-26',22039500),('Russia','2020-01-31',144500000),('Brazil','2020-02-26',209500000)]

data=data.fillna(value=0)
# raw=[data[i[0]].dropna()[data[i[0]].dropna()!=0] for i in country_first_list]

raw=[data[i[0]] for i in country_first_list]
day_add=25
raw=[data[i[0]][(datetime.datetime.strptime(i[1], '%Y-%m-%d')-datetime.datetime(2019,12,8)).days:(datetime.datetime.strptime(i[1], '%Y-%m-%d')-datetime.datetime(2019,12,8)).days+day_add] for i in country_first_list] #一级响应截开
raw=[np.subtract(i[1:],i[:-1]) for i in raw]

# raw=[[(j-min(i))/(max(i)-min(i)) for j in i] for i in raw] #min-max normalization
raw=[[(j-np.mean(i))/np.std(i) for j in i] for i in raw if np.std(i)!=0] #z normalization



# X_origin = to_time_series_dataset([np.subtract(i[1:],i[:-1]) for i in raw])
# scaler = MinMaxScaler()

# X = to_time_series_dataset([preprocessing.scale(np.subtract(i[1:],i[:-1])) for i in raw])
# X = to_time_series_dataset([preprocessing.scale(np.subtract(i[1:],i[:-1])) for i in raw])

X = to_time_series_dataset(raw)

# X = to_time_series_dataset([a-b for a,b in zip([data[i[0]].dropna()[data[i[0]].dropna()!=0] for i in country_first_list][1:],[data[i[0]].dropna()[data[i[0]].dropna()!=0] for i in country_first_list])][:-2])


# X1=np.array([[[6], [7], [8]],[[2],[3],[4]]])
# X = random_walks(n_ts=50, sz=32, d=1)
# result = TimeSeriesKMeans(n_clusters=4, metric="softdtw").fit_predict(X)
kind=6
# model=GlobalAlignmentKernelKMeans(n_clusters=kind)
# model=TimeSeriesKMeans(n_clusters=kind, metric="softdtw")

model = KShape(n_clusters=kind, n_init=1, random_state=0)
result = model.fit_predict(X)
print([(a,b) for a,b in zip([i[0] for i in country_first_list],result)])
sz = X.shape[1]
plt.figure(figsize=(15,6))
for yi in range(kind):
    plt.subplot(1, kind, yi + 1)
    for xx in X[result == yi]:
        plt.plot(xx.ravel(), "k-")
    # plt.plot(model.cluster_centers_[yi].ravel(), "r-")
    # plt.xlim(0, sz)
    # plt.ylim(-4, 4)
    i = 0
    for a,b in  [(a,b) for a,b in zip([i[0] for i in country_first_list],result)]:
        if b==yi:
            y=0.95-0.05*i
            i=i+1
            plt.text(0.2, y,a, ha='center', va='center', transform=plt.gca().transAxes)

    plt.text(0.55, 0.85,'Cluster %d' % (yi + 1),
             transform=plt.gca().transAxes)

# plt.gcf().savefig('KShape-total.jpg',bbox_inches='tight')
plt.show()