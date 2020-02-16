from requests_html import HTMLSession
import random
import sys
import json
import time
from pandas.io.json import json_normalize
import numpy as np
import pandas as pd
import re
import requests
import datetime

def telegram_bot_sendtext(bot_message):
    bot_token = '618426064:AAEPwV7G8fmf88r53RcFQ_aJm53AfvOj86Y'
    bot_chatID = '140278675'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

session = HTMLSession()

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]
# 页面数据 + 目标字符串


def get_html_page():

    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    today = datetime.date.today()

    headers = {"User-Agent": random.choice(USER_AGENTS)}
    dxyurl = 'https://3g.dxy.cn/newh5/view/pneumonia'
    response = session.get(dxyurl)
    # 01.完整页面
    page = response.html.html
    # print(page)
    # 02.目标内容
    start = page.find("window.getAreaStat = [")
    # print(start)
    temp = page[start + 22:]
    end = temp.find("]}catch(e){}")
    temp = temp[0:end]
    items = temp.split("]},")
    # 03.最后一个元素，特殊处理（尾部没有“，”号）
    last = items[-1]
    items.pop()
    newitems = []
    for item in items:
        item = item + "]}"
        newitems.append(item)
        # print(item)
    newitems.append(last)
    # 04. 省市数据分布
    city=pd.DataFrame()
    province=pd.DataFrame()
    area=pd.DataFrame()
    for item in newitems:
        # 输出原始数据
        with open(f'dxy_rawdata_{today}.txt', "a+") as f:
            print(item, file=f)

        data = json.loads(item)
        if data['provinceName'] not in ['北京市','上海市','重庆市','天津市']:
            #市级数据
            frame_city=json_normalize(data['cities'])
            # frame_city.drop('locationId', inplace=True, axis=1)
            frame_city['provinceName']=data['provinceName']
            city=city.append(frame_city, ignore_index=True)
        else:
            # 市级数据
            frame_city = json_normalize(data['cities'])
            # frame_city.drop('locationId', inplace=True, axis=1)
            frame_city['provinceName'] = data['provinceName']
            area = area.append(frame_city, ignore_index=True)
        del data['cities']
        #省级数据
        frame_province=json_normalize(data)
        frame_province = frame_province.drop(columns=['provinceShortName','comment','locationId'])
        province=province.append(frame_province, ignore_index=True)
        if data['provinceName'] in ['北京市', '上海市', '重庆市', '天津市']:
            frame_province['cityName']=data['provinceName']
            city = city.append(frame_province, ignore_index=True)



    city.drop(['locationId','deadCount'], inplace=True, axis=1)
    province.drop(['deadCount'], inplace=True, axis=1)


    city['updateTime']= today
    province['updateTime'] = today
    area['updateTime'] = today

    for index, row in city.iterrows():
        if len(row['cityName']) > 2 and row['cityName'][-1] in ['县', '市', '盟']:
            city.at[index, 'cityName'] = row['cityName'][:-1]
        elif len(row['cityName']) > 2 and row['cityName'][-1] == '州' and row['cityName'][-3:] != '自治州':
            city.at[index, 'cityName'] = row['cityName'][:-1]
        elif row['cityName'][-3:] == '管委会':
            city.at[index, 'cityName'] = row['cityName'][:-3]
        elif row['cityName'][-2:] == '地区':
            city.at[index, 'cityName'] = row['cityName'][:-2]
        elif row['cityName'][-1] in ['区', '旗']:
            city.at[index, 'cityName'] = np.nan

        if row['cityName'][0] in ['待', '未', '外', '第'] or '兵团' in row['cityName']:
            city.at[index, 'cityName'] = np.nan

        # 处理括号
        if '（' in row['cityName']:
            s = re.sub(u'[（]', '(', row['cityName'])
            s = re.sub(u'[）]', ')', s)
            city.at[index, 'cityName'] = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", s)
    city = city.dropna(how='any')
    city = city.rename(
        columns={'confirmedCount': 'city_confirmedCount', 'curedCount': 'city_curedCount',
                 'suspectedCount': 'city_suspectedCount'})
    province = province.rename(
        columns={'confirmedCount': 'province_confirmedCount', 'curedCount': 'province_curedCount',
                 'suspectedCount': 'province_suspectedCount'})


    city.to_csv(f'city-day-{today}.csv',index=0)
    province.to_csv(f'province-day-{today}.csv', index=0)
    area.to_csv(f'area-day-{today}.csv', index=0)

    city_sum=pd.read_csv(f'/mnt/data/Lindsay/2019-ncov/program/dxy-data/nice-dxy-data/city-day-summary-{yesterday}.csv')
    city_sum=pd.concat([city_sum,city],ignore_index=True)
    city_sum.to_csv(f'/mnt/data/Lindsay/2019-ncov/program/dxy-data/nice-dxy-data/city-day-summary-{today}.csv', index=0)

    province_sum = pd.read_csv(f'/mnt/data/Lindsay/2019-ncov/program/dxy-data/nice-dxy-data/province-day-summary-{yesterday}.csv')
    province_sum = pd.concat([province_sum, province], ignore_index=True)
    province_sum.to_csv(f'/mnt/data/Lindsay/2019-ncov/program/dxy-data/nice-dxy-data/province-day-summary-{today}.csv', index=0)

    country = province.sum()
    country['updateTime']=time.strftime("%Y-%m-%d")
    country=country.drop(['provinceName'])
    country.columns = ['country_confirmedCount', 'country_curedCount', 'country_suspectedCount','updateTime']
    country = pd.DataFrame(country).transpose()

    country_sum = pd.read_csv(f'/mnt/data/Lindsay/2019-ncov/program/dxy-data/nice-dxy-data/country-day-summary-{yesterday}.csv')
    country_sum = pd.concat([country_sum, country], ignore_index=True)
    country_sum.to_csv(f'/mnt/data/Lindsay/2019-ncov/program/dxy-data/nice-dxy-data/country-day-summary-{today}.csv', index=0)
    # print(country)

    test = telegram_bot_sendtext(f'get dxy data finish {time.strftime("%Y-%m-%d %H:%M:%S")} {city["cityName"]}')





# 主函数
if __name__ == '__main__':
    get_html_page()
