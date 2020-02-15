import matplotlib
import random
import matplotlib.pyplot as plt
import pandas as pd
import datetime

# 中文乱码和坐标轴负号处理。
matplotlib.rc('font', family='SimHei', weight='bold')
plt.rcParams['axes.unicode_minus'] = False

yesterday = datetime.date.today() - datetime.timedelta(days=1)
result=pd.read_csv(f'./result/slope-log-mean-{yesterday}.csv')
result=result.sort_values(by=['k'], ascending=False).reset_index(drop=True)[:10]

# 城市数据。
city_name = list(result['city'])
city_name.reverse()
data = list(result['k'])
data.reverse()

plt.barh(range(len(data)), data,color='#ff4c00')
plt.yticks(range(len(city_name)),city_name,fontsize='13')
plt.xticks()


plt.title('城市确诊人数指数增长率前十名', loc='center', fontsize='20',
          fontweight='bold')
plt.savefig(f'./result/log-mean-slope-top10-cityplot-{yesterday}.jpg', bbox_inches='tight')
plt.show()