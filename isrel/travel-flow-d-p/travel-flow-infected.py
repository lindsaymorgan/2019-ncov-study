import pandas as pd
import datetime
import itertools
import matplotlib.pyplot as plt

def cartesian_product_basic(left, right):
    return (
       left.assign(key=1).merge(right.assign(key=1), on='key').drop('key', 1))


today=datetime.date.today()-datetime.timedelta(days=1)
date=today-datetime.timedelta(days=1)
data=pd.read_csv(f'../../dxy-data/nice-dxy-data/province-pivot-day-summary-{today}.csv')
move=pd.read_csv(f'../../migration_2010.csv')

move=move[move['provinceName1']=='湖北省']
move=move[['export','provinceName2']]
move.rename(columns={'provinceName2': 'provinceName'}, inplace=True)
data=pd.merge(data,move,on='provinceName',how='inner')
plt.loglog(data['export'],data[f'{date}'],'o')

plt.show()
