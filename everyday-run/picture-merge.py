from __future__ import print_function
import os
import datetime
from PIL import Image
today=datetime.date.today()-datetime.timedelta(days=1)
files = [
    f'/mnt/data/Lindsay/2019-ncov/program/everyday-run/result/distance-cases-{today}.jpg',
    f'/mnt/data/Lindsay/2019-ncov/program/everyday-run/result/log-mean-slope-top10-cityplot-{today}.jpg',
    f'/mnt/data/Lindsay/2019-ncov/program/everyday-run/result/newlyconfirmcount-average-distance-{today}.jpg',
    f'/mnt/data/Lindsay/2019-ncov/program/everyday-run/result/city-log-mean-slope-top10-{today}.jpg']

large=[(800,800),(800,800),(800,800),(1000,1000)]
result = Image.new("RGB", (1300, 900),color = (255,255, 255))

for index, file in enumerate(files):
  path = os.path.expanduser(file)
  img = Image.open(path)
  img.thumbnail(large[index], Image.LANCZOS)
  x = index // 2 * 600
  y = index % 2 * 450
  w, h = img.size
  # print('pos {0},{1} size {2},{3}'.format(x, y, w, h))
  result.paste(img, (x, y, x + w, y + h))

result.save(os.path.expanduser(f'/mnt/data/Lindsay/2019-ncov/program/everyday-run/result/merge_summary_{today}.jpg'),dpi=(500,500))