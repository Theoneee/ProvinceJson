import json
import requests
from bs4 import BeautifulSoup
import time

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'

headers = {'User-Agent': USER_AGENT}

BASE_URL = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/'
INDEX = 'index.html'

SAVE_PATH = "C:\\Users\\Administrator\\Desktop\\all_province.json"

# 省
PROVINCE = 1
# 市
CITY = 2
# 区县
COUNTY = 3
# 乡镇
TOWN = 4
# 居委会
VILLAGE = 5

def get_list_data(url, type):
    config = get_type_config(type,url)
    soup = get_url_soup(config['url'])
    list = []
    for tags in soup.select(config['key']):
        items = tags.findAll(config['tag'])
        if len(items) == 0:
            continue
        else:
            if type == PROVINCE:
                for item in items:
                    name = item.get_text()
                    url = item.get('href')
                    print(name)
                    list.append({name: get_list_data(url, config['next'])})
            else:
                # code = items[0].get_text()
                name = items[config['index']].get_text()
                url = items[0].get('href')
                print(config['space'] + name )
                if url:
                    datas = get_list_data(url,config['next'])
                    if len(datas) >0:
                        list.append({name:datas})
                    else:
                        list.append(name)
                else:
                    list.append(name)
    return list

def get_type_config(type,url):
    URL = BASE_URL + url
    tag = 'a'
    index = 1
    space = ""
    next = PROVINCE
    key = ""
    if type == PROVINCE:
        next = CITY
        key = "provincetr"
    elif type == CITY:
        next = COUNTY
        key = "citytr"
        space = "=="
    elif type == COUNTY:
        next = TOWN
        key = "countytr"
        space = "===="
    elif type == TOWN:
        URL = BASE_URL + url[3:5]+"/" + url
        next = VILLAGE
        key = "towntr"
        space = "======"
    elif type == VILLAGE:
        URL = BASE_URL +url[3:5]+"/01/"+ url
        key = "villagetr"
        index =  2
        tag = 'td'
        space = "========"
    return {"url":URL,"next":next,"key":"."+key,"tag":tag,"index":index,"space":space}

def get_url_soup(url):
    r = requests.get(url, headers=headers)
    r.encoding = 'gb2312'
    return BeautifulSoup(r.text, "html.parser")

print("==============================")
print("开始爬取数据")
start = time.perf_counter()
json_list = get_list_data(INDEX,PROVINCE)
print("爬取数据完成")
print("==============================")
print("开始写入JSON")
jsonArr = json.dumps(json_list, ensure_ascii=False)
with open(SAVE_PATH,'a',encoding='utf-8')as fp:
    json.dump(json_list,fp,ensure_ascii=False)
end = time.perf_counter()
print("写入完成")
print('总耗时: %s 秒' % (end - start))
print("==============================")


