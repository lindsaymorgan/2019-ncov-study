import pandas as pd
from scipy.optimize import curve_fit
import numpy as np
from collections import Counter
import scipy as sp
import datetime
import requests
import time

def telegram_bot_sendtext(bot_message):
    bot_token = '618426064:AAEPwV7G8fmf88r53RcFQ_aJm53AfvOj86Y'
    bot_chatID = '140278675'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()



today = datetime.date.today()-datetime.timedelta(days=1)
country_data=pd.read_csv(f'/mnt/data/Lindsay/2019-ncov/program/dxy-data/nice-dxy-data/country-day-summary-{today}.csv')
data=pd.read_csv(f'/mnt/data/Lindsay/2019-ncov/program/dxy-data/nice-dxy-data/city-day-summary-{today}.csv')

data=data.sort_values(by=['provinceName', 'cityName','updateTime'])
data['updateTime']=pd.to_datetime(data['updateTime'])

city_list=list(Counter(data['cityName']))
city=list()
k_list=list()
b_list=list()

color=['r','y','g','b','m','c','lawngreen','sandybrown','darkviolet','hotpink']
def rmse(y_test, y):
    return sp.sqrt(sp.mean((y_test - y) ** 2))

for x in city_list:
    # i=result['city'][x]
    value = np.log10(data[data['cityName'] == x]['city_confirmedCount'])
    value.index = [(k - datetime.datetime(2020, 1, 23)).days for k in data[data['cityName'] == x]['updateTime']]
    value=value.rolling(3).mean()
    if len(value[15:])<6:
        continue
    # name = p.get_pinyin(f"{i}", "").capitalize()
    try:
        # popt, pcov = curve_fit(lambda t,k, b: k * t+b, list(range(len(value)))[-4:],value[-4:])
        popt, pcov = curve_fit(lambda t, k, b: k * t + b, value.index[-4:], value[-4:])
        city.append(x)
        k_list.append(popt[0])
        b_list.append(popt[1])

    except:
        continue

result=pd.DataFrame()
result['city']=city
result['k']=k_list
result['b']=b_list
result.sort_values(by='k',inplace=True,ascending=False)
result.to_csv(f'/mnt/data/Lindsay/2019-ncov/program/everyday-run/result/slope-log-mean-{today}.csv',index=0)
test = telegram_bot_sendtext(f'calculate finish {time.strftime("%Y-%m-%d %H:%M:%S")} ')

