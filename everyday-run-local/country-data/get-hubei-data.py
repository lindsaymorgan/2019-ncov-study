import urllib.request
import json
import csv
from pandas.io.json import json_normalize
import datetime

today=datetime.date.today()-datetime.timedelta(days=1)
# today=datetime.datetime(2020,2,12)
def getdata(indate):

    headers={
    'Host': 'huiyan.baidu.com',
    'Connection': 'keep - alive',
    'User - Agent': ' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Accept': '* / *',
    'Sec - Fetch - Site': 'same - site',
    'Sec - Fetch - Mode': 'no - cors',
    'Referer': 'https: // qianxi.baidu.com /',
    'Accept - Encoding': 'gzip, deflate, br',
    'Accept - Language': 'zh - CN, zh',
    'q' : '0.9',
    'cookie':' BIDUPSID=163D270C00008EE349117DD27AC58CBE; PSTM=1562302546; BAIDUID=5E9E0BBE6DFFC5779D1B5A326398786E:FG=1; delPer=0; PSINO=7; ZD_ENTRY=empty; H_WISE_SIDS=141176_114552_141192_139405_138496_135846_141000_139148_138471_138451_139193_138878_137978_140173_131247_132552_137746_138165_107317_138883_140260_141372_139057_140202_136863_138585_139171_140078_140114_136196_131861_140591_140324_140578_133847_140793_140065_131423_141175_140311_140839_136413_136752_110085_127969_140593_140865_139886_140993_139408_128200_138312_138426_141194_139557_140684_141191_140597_139600_140964; H_PS_PSSID=1450_21096_30495; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; PHPSESSID=9lg79hs0alm3ktedls42n17gb2'
    }

    url='https://huiyan.baidu.com/migration/provincerank.jsonp?dt=province&id=420000&type=move_out&date=20200123'
    req=urllib.request.Request(url,headers=headers,method='GET')
    response=urllib.request.urlopen(req)

    data2=response.read().decode('utf-8')
    data = json.loads(data2[3:-1])
    data = json_normalize(data['data']['list'])
    data_out=data.rename(columns={'value':'move_out','province_name':'provinceName'})

    url = 'https://huiyan.baidu.com/migration/provincerank.jsonp?dt=province&id=420000&type=move_in&date=20200123'
    req = urllib.request.Request(url, headers=headers, method='GET')
    response = urllib.request.urlopen(req)

    data2 = response.read().decode('utf-8')
    data = json.loads(data2[3:-1])
    data = json_normalize(data['data']['list'])
    data = data.rename(columns={'value': 'move_in','province_name':'provinceName'})
    data=data.merge(data_out, on=('provinceName'))
    data.to_csv(f'baiduqianxi_hubei_level_20200123.csv',index=0,encoding='utf-8-sig',sep=',')


getdata(today.strftime('%Y%m%d'))