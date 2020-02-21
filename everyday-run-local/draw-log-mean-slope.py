import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import datetime
import requests
import time


def telegram_bot_sendtext(bot_message):
    bot_token = '618426064:AAEPwV7G8fmf88r53RcFQ_aJm53AfvOj86Y'
    bot_chatID = '140278675'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()



plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签

today = datetime.date.today()-datetime.timedelta(days=1)
country_data=pd.read_csv(f'country-day-summary-{today}.csv')
data=pd.read_csv(f'city-day-summary-{today}.csv')

data=data.sort_values(by=['provinceName', 'cityName','updateTime'])
result=pd.read_csv(f'./result/slope-log-mean-{today}.csv')
result=result.sort_values(by=['k'], ascending=False).reset_index(drop=True)
#, label=f'fit-{name}-{round(popt[0],2)}'
color=['r','y','g','b','m','c','lawngreen','sandybrown','darkviolet','hotpink']

#right fig
for x in range(10):
    i=result['city'][x]
    if i not in ['黔南','通辽']:
        k=result['k'][x]
        b=result['b'][x]

        value = np.log10(data[data['cityName'] == i]['city_confirmedCount'])
        value=value.rolling(3).mean()

        y2 = [k* i+b for i in list(range(len(value)+2))[-6:]]
        plt.plot(range(len(value)), value, marker='o', label=f'{i}',color=color[x])
        plt.plot(list(range(len(value)+2))[-6:], y2, '--',color=color[x])


# formatter = FuncFormatter(formatnum)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.xlabel('日期')
date=list()
m=datetime.datetime(2020,1,24)
while m.date()-datetime.timedelta(days=1)<=today:
    m=m+datetime.timedelta(days = 2)
    date.append( m.strftime("%m-%d"))
plt.xticks( [i*2 for i in range(1,len(date))], date ,rotation=45)

ytick=[1,3,6,10,30,60,100,300,600,1000,3000,6000,10000,30000]
plt.yticks( np.log10(ytick),ytick)
plt.ylabel('确诊人数规模-对数坐标')

plt.savefig(f'./result/city-log-mean-slope-top10-{today}.jpg',bbox_inches='tight')
plt.close()


#left fig
result=result[:10]
city_name = list(result['city'])[1:4]+list(result['city'])[5:]
with open(f'./result/text-{today}.txt', 'a+') as f:
    print('slope_top10',', '.join(list(result["city"])[:10]), file=f)
city_name.reverse()
data = list(result['k'])[1:4]+list(result['k'])[5:]
data.reverse()

plt.barh(range(len(data)), data,color='#ff4c00')
plt.yticks(range(len(city_name)),city_name,fontsize='13')
plt.xticks()


plt.title('城市确诊人数指数增长率前八名', loc='center', fontsize='20',
          fontweight='bold')
plt.savefig(f'./result/log-mean-slope-top10-cityplot-{today}.jpg', bbox_inches='tight')

test = telegram_bot_sendtext(f'{list(result["city"])[:10]}')

# plt.show()

