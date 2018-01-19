
from bs4 import BeautifulSoup
import requests
import re
import json
import math

product = []  # make sure to put [dic] out side of for loop
section_list = []

outdoor_URL = requests.get(
    "http://www.u-mall.com.tw/LList?nm=%e9%81%8b%e5%8b%95%e5%81%a5%e8%ba%ab%e5%99%a8%e6%9d%90&StoreID=33297&CategoryID=33385")
a = BeautifulSoup(outdoor_URL.text, "html5lib")

cate_id = re.findall(
    '''\{"CATE_ID": "(.{4,6})", "CATE_NAME": ".{2,20}", "CATE_TYPE": ''',
    a.text)
cate_name = re.findall(
    '''\{"CATE_ID": ".{4,6}", "CATE_NAME": "(.{2,20})", "CATE_TYPE": ''',
    a.text)

for m in range(0, len(cate_id)):
    URL_session = "http://www.u-mall.com.tw/SList?nm=" + cate_name[m] + "&StoreID=33297&CategoryID=" + cate_id[m] + "&"
    resp_session = requests.get(URL_session)

    page_num = int(re.findall('var ProductPageTotalCount = (\d{1,6});', resp_session.text)[0]) / 40
    page_num = math.ceil(page_num)

    for i in range(0, page_num):
        try:
            URL = URL_session + "&ProductPage=%s&RecordsPerPage=40" % i
            resp = requests.get(URL)
            product_num = re.findall("""<div class\="Gd\-name">'\+ DoubleToSingle\('(.{0,200})'\) \+'""", resp.text)

            for j in range(0, (len(product_num))):
                product_list = \
                re.findall("""<div class\="Gd\-name">'\+ DoubleToSingle\('(.{0,200})'\) \+'""", resp.text)[j]

                if re.findall("""Sys_showPRCValue\('(.{0,1})', '.{0,10}', '.{0,10}'\)  \+'<""", s.text)[j] == "Y":
                    price_list = \
                    re.findall("""Sys_showPRCValue\('.{0,1}', '(.{0,10})', '.{0,10}'\)  \+'<""", resp.text)[j]
                else:
                    price_list = \
                    re.findall("""Sys_showPRCValue\('.{0,1}', '.{0,10}', '(.{0,10})'\)  \+'<""", resp.text)[j]

                product.append({
                    'product': product_list,
                    'price': price_list
                })
        except:
            continue

with open('./shenshen_sports3.json', 'w', encoding='utf-8') as f:
    json.dump(product, f, indent=2, sort_keys=True, ensure_ascii=False)