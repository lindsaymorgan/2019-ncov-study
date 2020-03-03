import json
import time
from pandas.io.json import json_normalize
import pandas as pd

migration_pd=pd.DataFrame()
with open('migration.json', 'r',encoding='utf-8') as f:
    data = json.load(f)
    for d in data:
        frame = json_normalize(data[d])
        frame=frame.groupby(['name'],as_index=False).first()
        frame = frame.rename(
            columns={'name': 'provinceName2'})
        frame['provinceName1']=d
        migration_pd=migration_pd.append(frame,ignore_index=True)

migration_pd['choice']=
for index,row in migration_pd.iterrows():

migration_set=[set([a,b]) for a,b in zip(migration_pd['provinceName1'],migration_pd['provinceName2'])]

migration_pd.to_csv('migration_2010.csv',index=0,encoding='utf-8-sig',sep=',')