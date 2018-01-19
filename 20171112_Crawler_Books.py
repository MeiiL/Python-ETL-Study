from bs4 import BeautifulSoup
import requests
import re
import json

product = []  
section_list = []

outdoor_URL = requests.get("http://www.books.com.tw/web/outdoors")
a = BeautifulSoup(outdoor_URL.text, "html5lib")
outdoor_urls = [x.get('href') for x in a.select('.sub > li > span > a') if x.get('href').startswith('http')]
for url in outdoor_urls:
    section_list.append(re.findall('(http://www.books.com.tw/web/.+/outdoors/.+)\?', url)[0].strip())


for m in range(1, len(section_list)):
    for i in range(1, 20):
        try:
            URL = section_list[m] + "/?o=5&page=%s" % i
            resp = requests.get(URL)
            s = BeautifulSoup(resp.text, "html5lib")  

            product_num = s.select(".price")
            for j in range(len(product_num)):
                product_list = s.select_one(".cntli_001").select("li > h4")[j].text.strip()
                price_list = s.select_one(".cntli_001").select("li > span.price")[j].text.strip()

                product.append({
                    'product': product_list,
                    'price': price_list
                })
            print("[INFO] Crawling pages %s, status is %s" % (URL, resp.status_code))
        except:
            continue

with open('./works/books_sports.json', 'w', encoding='utf-8') as f:
    json.dump(product, f, indent=2, sort_keys=True, ensure_ascii=False)
