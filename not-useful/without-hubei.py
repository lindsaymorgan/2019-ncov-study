import pandas as pd
import powerlaw
import matplotlib.pyplot as plt
import numpy as np

raw_data=pd.read_csv('province-day-summary-2020-02-11.csv')
raw_data['updateTime'] = pd.to_datetime(raw_data['updateTime'])

data=raw_data[raw_data['provinceName']=='湖北省']
summary=data.groupby(['updateTime']).agg(np.sum)
inc=summary['province_confirmedCount']-summary['province_confirmedCount'].shift(1)
print(summary)
print(inc)
