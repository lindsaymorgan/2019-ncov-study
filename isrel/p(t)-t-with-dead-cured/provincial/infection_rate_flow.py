import pandas as pd
from scipy.optimize import curve_fit
import datetime
import matplotlib.pyplot as plt
import numpy as np
from itertools import compress

infection=pd.read_csv('province_infection_2020-02-28.csv')

tf=pd.read_csv('../../../china_migration_2005_2010.csv')
tf.index=tf['provinceName']
tf=tf.T
tf=tf[3:-1]
tf['provinceName']=tf.index
tf=tf[['provinceName','湖北省']]

data=pd.merge(infection,tf,on='provinceName',how='left')

plt.loglog(data['湖北省'],data['infection_rate'],'o')
plt.ylabel('Infection Rate',fontsize=15)
plt.xlabel('Population Migration',fontsize=15)
plt.savefig('InfectionRate-PopulationMigration.jpg', bbox_inches='tight')
plt.show()