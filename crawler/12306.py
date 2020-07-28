# -*- coding: utf-8 -*-
"""
Created on Thu May  7 22:42:50 2020

@author: liming
"""

import re
import requests

cookies = None
login_url = r"https://kyfw.12306.cn/otn/resources/login.html"
UserLoginHead = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
  'Content-Type': 'application/x-www-form-urlencoded',
  'Referer': 'https://kyfw.12306.cn/otn/resources/login.html',
  'Upgrade-Insecure-Requests': '1',
  'Accept-Encoding': 'gzip, deflate, br',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37'
}
# res = requests.get(login_url, headers=UserLoginHead)
# cookies = res.cookies
with requests.session() as session:
    res = session.get(login_url,headers=headers)
    cookies = session.cookies

print(str(cookies))

date = "2020-06-01"
from_station = "SHH"
to_station = "TJH"

url = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=%s" \
      "&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT" % (
          date, from_station, to_station)
print(url)
response = requests.get(url, headers=headers, cookies=cookies)
print(response.text)
# stations = re.findall(r'([\u4e00-\u9fa5]\|([A-Z]+))',response.text)
# print(stations)
# station_codes = dict(stations)
