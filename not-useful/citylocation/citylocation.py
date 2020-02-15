import json
import pandas as pd
import csv
from xpinyin import Pinyin

p = Pinyin()
with open(u'chinaCity.json',encoding='utf-8') as f:
    data = json.load(f)
with open('chinacitylocation.csv','w',newline='') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(['cityName-ch','cityName','lat','lon'])

    for i in data:
        if i['name'][-1]=='市':
            name = p.get_pinyin(f"{i['name'][:-1]}", "").capitalize()
            f_csv.writerow([i['name'][:-1],str(name),i['lat'],i['log']])
        else:
            for d in i['children']:
                name = p.get_pinyin(f"{d['name']}", "").capitalize()
                f_csv.writerow([d['name'],str(name), d['lat'], d['log']])


