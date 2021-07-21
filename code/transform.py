import json
from xpinyin import Pinyin
from pypinyin import lazy_pinyin

class Transform():

    def format_json(self):
        with open('C:\\Users\\Administrator\\Desktop\\all_province.txt', 'r', encoding='utf8')as f:
            # 所有省列表
            data = json.load(f)
            response = {}
            # 一个省的数据 provinces
            for provinces in data:
                for province, cities_list in provinces.items():
                    # 省
                    print(province)
                    # 所有市的数据 cities_list
                    res_city = {}
                    # 一个市的数据 cities
                    for cities in cities_list:
                        for city, counties_list in cities.items():
                            # 市
                            print("==" + city)
                            # 所有区县列表
                            res_county = {}
                            # 一个区县的数据 counties
                            for counties in counties_list:
                                for county, towns_list in counties.items():
                                    # 区县
                                    print("====" + county)
                                    # 所有乡镇的数据 towns_list
                                    res_town_list = []
                                    res_town = {}
                                    for towns in towns_list:
                                        # 一个乡镇的数据 towns  所有村庄数据 villages_list
                                        for town, villages_list in towns.items():
                                            # 乡镇
                                            print("======" + town)
                                            if villages_list:
                                                res_town.__setitem__(town,villages_list)
                                            else:
                                                res_town_list.append(town)
                                    if len(res_town_list) >0:
                                        res_county.__setitem__(county,res_town_list)
                                    else:
                                        res_county.__setitem__(county,res_town)
                            res_city.__setitem__(city,res_county)
                    response.__setitem__(province,res_city)
            with open('C:\\Users\\Administrator\\Desktop\\all_province_front.json', 'a', encoding='utf-8')as fp:
                json.dump(response, fp, ensure_ascii=False)


    def format_back_json(self):
        with open('C:\\Users\\Administrator\\Desktop\\all_province_front.json', 'r', encoding='utf8')as f:
            # 所有省列表
            data = f.read()
            # txt文件包含BOM字符，去掉BOM字符
            if data.startswith(u'\ufeff'):
                data = data.encode('utf8')[3:].decode('utf8')
            json_data = json.loads(data)
            index = 1
            province_list = []
            response = {}
            pin = Pinyin()
            # 循环得到所有的省份
            for k,v in json_data.items():
                province_list.append({"code":str(index),"address":k})
                index+=1
            res_province = {}
            res_A_G = []
            res_H_N = []
            res_O_T = []
            res_U_Z = []
            for province in province_list:
                name = province['address']
                # 取首字母拼音转成大写
                if "重庆" in name:
                    py = "c"
                else:
                    py = pin.get_pinyin(name)[0:1]

                py =py.upper()
                if py in 'ABCDEFG':
                    res_A_G.append(province)
                elif py in 'HIJKLMN':
                    res_H_N.append(province)
                elif py in 'OPQRST':
                    res_O_T.append(province)
                else:
                    res_U_Z.append(province)
            res_province.__setitem__("A-G",res_A_G)
            res_province.__setitem__("H-N",res_H_N)
            res_province.__setitem__("O-T",res_O_T)
            res_province.__setitem__("U-Z",res_U_Z)

            response.__setitem__("86",res_province)
            for province in province_list:
                address = province['address']
                city_list = json_data[address]
                res_city = {}
                for city,county_list in city_list.items():
                    index += 1
                    city_id = index
                    # 市
                    res_city.__setitem__(str(city_id),city)
                    res_county = {}
                    for county, town_list in county_list.items():
                        index += 1
                        county_id = index
                        # 区县
                        res_county.__setitem__(str(county_id),county)
                        res_town= {}
                        try:
                            for town, village_list in town_list.items():
                                # 县
                                index += 1
                                res_town.__setitem__(str(index),town)
                        except Exception:
                            for town in town_list:
                                index += 1
                                res_town.__setitem__(str(index),town)
                        response.__setitem__(str(county_id),res_town)
                    response.__setitem__(str(city_id),res_county)
                response.__setitem__(province['code'],res_city)
            print(response)
            with open('C:\\Users\\Administrator\\Desktop\\all_province_back.json', 'a', encoding='utf-8')as fp:
                json.dump(response, fp, ensure_ascii=False)

    def sort_pinyin(self,hanzi_list):
        hanzi_list_pinyin = []
        hanzi_list_pinyin_alias_dict = {}
        for single_str in hanzi_list:
            py_r = lazy_pinyin(single_str)
            # print("整理下")
            single_str_py = ''
            for py_list in py_r:
                single_str_py = single_str_py + py_list
            hanzi_list_pinyin.append(single_str_py)
            hanzi_list_pinyin_alias_dict[single_str_py] = single_str
        hanzi_list_pinyin.sort()
        sorted_hanzi_list = []
        for single_str_py in hanzi_list_pinyin:
            sorted_hanzi_list.append(hanzi_list_pinyin_alias_dict[single_str_py])
        return sorted_hanzi_list

# Transform().format_json()
Transform().format_back_json()
