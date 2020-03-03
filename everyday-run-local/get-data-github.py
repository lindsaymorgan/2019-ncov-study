import urllib
import datetime

today=datetime.date.today()-datetime.timedelta(days=1)
# testfile = urllib.request()
urllib.request.urlretrieve("https://github.com/BlankerL/DXY-COVID-19-Data/raw/master/csv/DXYArea.csv", f"rawdata-{today}.csv")