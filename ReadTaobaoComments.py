import urllib2
import re
import time
import requests
from bs4 import BeautifulSoup
import json
import logging.handlers

# Log File sort by time
tm = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
log_file = '%s.log' % tm

# Log File handler
handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
fmt = '%(message)s'
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

logger = logging.getLogger('Comments')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

url = 'https://s.taobao.com/search?initiative_id=tbindexz_20170824&ie=utf8&spm=a21bo.50862.201856-taobao-item.2&sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q=606%E8%BD%B4%E6%89%BF&suggest=0_2&_input_charset=utf-8&wq=606&suggest_query=606&source=suggest&sort=sale-desc'
pre_content = requests.get(url)
soup = BeautifulSoup(pre_content.text, 'lxml')
node = soup.find_all('script')[7].string

e = re.compile(r'"allNids":\[(.*?)]')
f = re.compile(r'"(\d+)"')
g = re.compile(r'href="//rate.taobao.com/(.*?)"')
# print pre_content.text
product_id = re.findall(e, node)[0]
product_list = re.findall(f, product_id)
print product_list
for i in product_list:
    product_url = 'https://item.taobao.com/item.htm?id=%s' % i
    content = requests.get(product_url)
    if re.findall(g, content.text):
        rate_url = re.findall(g, content.text)[0]
        rate_url = 'https://rate.taobao.com/%s' % rate_url
        print rate_url
    else:
        print product_url
