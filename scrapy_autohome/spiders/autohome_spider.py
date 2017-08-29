# -*- coding: utf-8 -*-
import re
import scrapy
import urllib.parse
from scrapy_autohome.all_car_id import All_Car_Id
from scrapy_autohome.items import ScrapyAutohomeItem


class AutohomeSpider(scrapy.Spider):
    name = "autohome_spider"
    allowed_domains = ["autohome.com"]
    start_urls = ['http://autohome.com/']
    # 评论的个数
    count = 0

    # 循环页码，就在这个函数中实现。
    def start_requests(self):
        reqs = []  # 每个车型页面的request

        # 获取所有车辆的ID
        all_car_id = All_Car_Id()
        car_id_list = all_car_id.car_id_list
        # 两层遍历，分别遍历车型和页数
        for i in car_id_list:  # i代表从车型的遍历
            for j in range(1,101): # j代表评论页数，range(1,3)表示1到2页
                req = scrapy.Request("http://k.autohome.com.cn/"+str(i)+"/index_"+str(j)+".html#dataList")
                reqs.append(req)
        return reqs

    def parse(self, response):
        # 记录个数
        AutohomeSpider.count += 1
        #print(AutohomeSpider.count)

        # 获取所有评论div //*[@id="maodian"]/div/div/div[2]/div[4]
        divs = response.xpath('//*[@id="maodian"]/div/div/div[2]/div[@class="mouthcon"]')



        for div in divs:
            # 记录个数
            AutohomeSpider.count += 1
            print("----------------------------------")
            print("第：",AutohomeSpider.count,"个评论。")

            item = ScrapyAutohomeItem()
            # 车ID //*[@id="maodian"]/div/div/div[2]/div[4]/div/div[1]/div[2]/dl[1]/dd/a[1]
            item['CAR_ID'] = div.xpath('div/div[1]/div[2]/dl[1]/dd/a[1]/@href')[0].extract().replace('/','')
            # 车名字
            item['CAR_NAME'] = div.xpath('div/div[1]/div[2]/dl[1]/dd/a[1]/text()')[0].extract()

            # 用户ID  //*[@id="maodian"]/div/div/div[2]/div[4]/div/div[1]/div[1]/div/div[1]/div[2]/p/a
            USER_ID1 = div.xpath('div/div[1]/div[1]/div/div[1]/div[2]/p/a/@href')[0].extract()
            item['USER_ID'] = re.findall('\d{1,15}',USER_ID1)[0]
            item['USER_NAME'] = div.xpath('div/div[1]/div[1]/div/div[1]/div[2]/p/a/text()')[0].extract().strip()

            # 购买地点 //*[@id="maodian"]/div/div/div[2]/div[4]/   div/div[1]/div[2]/dl[2]/dd
            PURCHASE_PLACE = div.xpath('div/div[1]/div[2]/dl[2]/dd')[0]
            item['PURCHASE_PLACE'] =PURCHASE_PLACE.xpath('string(.)').extract()[0].strip()


            # 因为列表属性相同且数量不确定，所要加入判断
            dls =div.xpath('div/div[1]/div[2]/dl')
            # 正常的有7个
            if dls.__len__() == 7:
                # 购买时间 //*[@id="maodian"]/div/div/div[2]/div[4]/ div/div[1]/div[2]/dl[4]/dd
                item['PURCHASE_TIME'] = div.xpath('div/div[1]/div[2]/dl[4]/dd/text()')[0].extract().strip()
                # 裸车购买价 //*[@id="maodian"]/div/div/div[2]/div[4]/ div/div[1]/div[2]/dl[5]/dd
                CAR_PRICE = div.xpath('div/div[1]/div[2]/dl[5]/dd')[0]
                item['CAR_PRICE'] = CAR_PRICE.xpath('string(.)').extract()[0].strip().replace('\xa0','')
                # 购车目的 //*[@id="maodian"]/div/div/div[2]/div[4]/ div/div[1]/div[2]/dl[7]/dd
                PURCHASE_PURPOSE = div.xpath('div/div[1]/div[2]/dl[7]/dd')[0]
                item['PURCHASE_PURPOSE'] = PURCHASE_PURPOSE.xpath('string(.)').extract()[0].strip().replace('\r\n','').replace('                                ',';')
            #不正常的有6个，分为两种情况：缺经销商和缺油耗。
            elif dls.__len__() == 6:
                p = div.xpath('div/div[1]/div[2]/dl[5]/dt/p')
                # 如果有p标签 ，说明有油耗，没有经销商
                if p:
                    # 购买时间 //*[@id="maodian"]/div/div/div[2]/div[4]/ div/div[1]/div[2]/dl[4]/dd
                    item['PURCHASE_TIME'] = div.xpath('div/div[1]/div[2]/dl[3]/dd/text()')[0].extract().strip()
                    # 裸车购买价 //*[@id="maodian"]/div/div/div[2]/div[4]/ div/div[1]/div[2]/dl[5]/dd
                    CAR_PRICE = div.xpath('div/div[1]/div[2]/dl[4]/dd')[0]
                    item['CAR_PRICE'] = CAR_PRICE.xpath('string(.)').extract()[0].strip().replace('\xa0', '')
                    # 购车目的 //*[@id="maodian"]/div/div/div[2]/div[4]/ div/div[1]/div[2]/dl[7]/dd
                    PURCHASE_PURPOSE = div.xpath('div/div[1]/div[2]/dl[6]/dd')[0]
                    item['PURCHASE_PURPOSE'] = PURCHASE_PURPOSE.xpath('string(.)').extract()[0].strip().replace('\r\n','').replace('                                ', ';')
                # 如果没有p说明 没有油耗，有经销商
                else:
                    # 购买时间 //*[@id="maodian"]/div/div/div[2]/div[4]/ div/div[1]/div[2]/dl[4]/dd
                    item['PURCHASE_TIME'] = div.xpath('div/div[1]/div[2]/dl[4]/dd/text()')[0].extract().strip()
                    # 裸车购买价 //*[@id="maodian"]/div/div/div[2]/div[4]/ div/div[1]/div[2]/dl[5]/dd
                    CAR_PRICE = div.xpath('div/div[1]/div[2]/dl[5]/dd')[0]
                    item['CAR_PRICE'] = CAR_PRICE.xpath('string(.)').extract()[0].strip().replace('\xa0', '')
                    # 购车目的 //*[@id="maodian"]/div/div/div[2]/div[4]/ div/div[1]/div[2]/dl[7]/dd
                    PURCHASE_PURPOSE = div.xpath('div/div[1]/div[2]/dl[6]/dd')[0]
                    item['PURCHASE_PURPOSE'] = PURCHASE_PURPOSE.xpath('string(.)').extract()[0].strip().replace('\r\n','').replace('                                ', ';')



            # 评分- 空间 //*[@id="maodian"]/div/div/div[2]/div[4]/ div/div[1]/div[2]/div[1]/dl/dd/span[2]
            item['SCORE_SPACE'] = div.xpath('div/div[1]/div[2]/div[1]/dl/dd/span[2]/text()')[0].extract()
            # 评分- 动力 //*[@id="maodian"]/div/div/div[2]/div[4]/ div/div[1]/div[2]/div[2]/dl/dd/span[2]
            item['SCORE_POWER'] = div.xpath('div/div[1]/div[2]/div[2]/dl/dd/span[2]/text()')[0].extract()
            # 评分- 操控
            item['SCORE_CONTROL'] = div.xpath('div/div[1]/div[2]/div[3]/dl/dd/span[2]/text()')[0].extract()
            # 评分- 油耗
            item['SCORE_FUEL_CONSUMPTION'] = div.xpath('div/div[1]/div[2]/div[4]/dl/dd/span[2]/text()')[0].extract()
            # 评分- 舒适性
            item['SCORE_COMFORT'] = div.xpath('div/div[1]/div[2]/div[5]/dl/dd/span[2]/text()')[0].extract()
            # 评分- 外观
            item['SCORE_EXTERIOR'] = div.xpath('div/div[1]/div[2]/div[6]/dl/dd/span[2]/text()')[0].extract()
            # 评分- 内饰
            item['SCORE_INTERIOR'] = div.xpath('div/div[1]/div[2]/div[7]/dl/dd/span[2]/text()')[0].extract()
            # 评分- 性价比 //*[@id="maodian"]/div/div/div[2]/div[4]/ div/div[1]/div[2]/div[8]/dl/dd/span[2]
            item['SCORE_COST_EFFECTIVE'] = div.xpath('div/div[1]/div[2]/div[8]/dl/dd/span[2]/text()')[0].extract()



            # 有多少人支持这条口碑  #//*[@id="maodian"]/div/div/div[2]/div[6]/  div/div[2]/div[1]/div[3]/div[2]/span[3]/label
            item['COMMENT_SUPPORT_QUANTITY'] = div.xpath('div/div[2]/div[1]/div[3]/div[2]/span[3]/label/text()')[0].extract()
            # 有多少人看过这条口碑  #//*[@id="maodian"]/div/div/div[2]/div[6]/  div/div[2]/div[1]/div[3]/div[2]/span[4]/a
            item['COMMENT_SEEN_QUANTITY'] = div.xpath('div/div[2]/div[1]/div[3]/div[2]/span[4]/a/text()')[0].extract()


            # 评论的url //*[@id="maodian"]/div/div/div[2]/div[4]/ div/div[1]/div[1]/div/div[2]/div[2]
            url_id_pre = div.xpath('div/div[1]/div[1]/div/div[2]/div[2]/@id')[0].extract()# 结果为 DivRelatedTopics_1565672
            # 截取id
            url_id = re.findall('\d{1,20}', url_id_pre)[0]
            # 存入评论url
            item['COMMENT_URL'] ="http://k.autohome.com.cn/FrontAPI/GetFeelingByEvalId?evalId=" + url_id
            COMMENT_URL = item['COMMENT_URL']

            #  用回调函数获取 评论内容
            yield scrapy.Request(url=COMMENT_URL,meta={'item': item},callback=self.parse_recommand,dont_filter=True)


    def parse_recommand(self,response):
        # 此函数用于解析评论json

        #　获取该页面的代码　
        text = response.body
        # 解码为gb312（通过response.headers知道）
        text1 = str(text, encoding="gb2312",errors='ignore').replace("\\u0027", "'").replace("\\u003e", ">").replace("\\u003c", "<")
        # 调用函数 替换<span>
        text2 = AutohomeSpider.get_complete_text_autohome(text1)
        # 获取中文评论
        text3 = re.findall(r'@HS_BASE64@.*@HS_ZY@',text2)[0].replace('@HS_BASE64@-->',"").replace("<!--@HS_ZY@","")

        # 使用传入的item
        item = response.meta['item']
        item["COMMENT_CONTENT"] = text3
        yield item


    # 该函数用于替换<span>
    def get_complete_text_autohome(text):

        text = text.replace(r"\u0027", "'").replace(r"\u003e", ">").replace(r"\u003c", "<")
        js = re.search("<!--@HS_ZY@--><script>([\s\S]+)\(document\);</script>", text)
        #print("find : %s" % js.group())
        if not js:
            print("  if not js:")
            return text
        try:
            char_list = AutohomeSpider.get_char(js.group(1))
            print("try111")

        except Exception as e:
            print(e)
            print("except222")
            return text

        def char_replace(m):
            index = int(m.group(1))
            char = char_list[index]
            return char

        text = re.sub("<span\s*class=[\'\"]hs_kw(\d+)_[^\'\"]+[\'\"]></span>", char_replace, text)
        # print(text)
        return text


    # 这个函数用于 获取js中的变换规则
    def get_char(js):
        all_var = {}
        # 判断混淆 无参数 返回常量 函数
        if_else_no_args_return_constant_function_functions = []
        """
        function zX_() {
                function _z() {
                    return '09';
                };
                if (_z() == '09,') {
                    return 'zX_';
                } else {
                    return _z();
                }
            }
        """
        constant_function_regex4 = re.compile("""
            function\s+\w+\(\)\s*\{\s*
                function\s+\w+\(\)\s*\{\s*
                    return\s+[\'\"][^\'\"]+[\'\"];\s*
                \};\s*
                if\s*\(\w+\(\)\s*==\s*[\'\"][^\'\"]+[\'\"]\)\s*\{\s*
                    return\s*[\'\"][^\'\"]+[\'\"];\s*
                \}\s*else\s*\{\s*
                    return\s*\w+\(\);\s*
                \}\s*
            \}
            """,
                                              re.X)
        l = constant_function_regex4.findall(js)
        # print("l 38",l)
        for i in l:
            function_name = re.search("""
            function\s+(\w+)\(\)\s*\{\s*
                function\s+\w+\(\)\s*\{\s*
                    return\s+[\'\"]([^\'\"]+)[\'\"];\s*
                \};\s*
                if\s*\(\w+\(\)\s*==\s*[\'\"]([^\'\"]+)[\'\"]\)\s*\{\s*
                    return\s*[\'\"]([^\'\"]+)[\'\"];\s*
                \}\s*else\s*\{\s*
                    return\s*\w+\(\);\s*
                \}\s*
            \}
            """, i,
                                      re.X)
            if_else_no_args_return_constant_function_functions.append(function_name.groups())
            js = js.replace(i, "")
            # 替换全文
            a, b, c, d = function_name.groups()
            all_var["%s()" % a] = d if b == c else b

        # 判断混淆 无参数 返回函数 常量
        if_else_no_args_return_function_constant_functions = []
        """
        function wu_() {
                function _w() {
                    return 'wu_';
                };
                if (_w() == 'wu__') {
                    return _w();
                } else {
                    return '5%';
                }
            }
        """
        constant_function_regex5 = re.compile("""
            function\s+\w+\(\)\s*\{\s*
                function\s+\w+\(\)\s*\{\s*
                    return\s+[\'\"][^\'\"]+[\'\"];\s*
                \};\s*
                if\s*\(\w+\(\)\s*==\s*[\'\"][^\'\"]+[\'\"]\)\s*\{\s*
                    return\s*\w+\(\);\s*
                \}\s*else\s*\{\s*
                    return\s*[\'\"][^\'\"]+[\'\"];\s*
                \}\s*
            \}
            """,
                                              re.X)
        l = constant_function_regex5.findall(js)
        # print("l 87",l)
        for i in l:
            function_name = re.search("""
            function\s+(\w+)\(\)\s*\{\s*
                function\s+\w+\(\)\s*\{\s*
                    return\s+[\'\"]([^\'\"]+)[\'\"];\s*
                \};\s*
                if\s*\(\w+\(\)\s*==\s*[\'\"]([^\'\"]+)[\'\"]\)\s*\{\s*
                    return\s*\w+\(\);\s*
                \}\s*else\s*\{\s*
                    return\s*[\'\"]([^\'\"]+)[\'\"];\s*
                \}\s*
            \}
            """, i,
                                      re.X)
            if_else_no_args_return_function_constant_functions.append(function_name.groups())
            js = js.replace(i, "")
            # 替换全文
            a, b, c, d = function_name.groups()
            all_var["%s()" % a] = b if b == c else d

        # var 参数等于返回值函数
        var_args_equal_value_functions = []
        """
        var ZA_ = function(ZA__) {
                'return ZA_';
                return ZA__;
            };
        """
        constant_function_regex1 = re.compile(
            "var\s+[^=]+=\s*function\(\w+\)\{\s*[\'\"]return\s*\w+\s*[\'\"];\s*return\s+\w+;\s*\};")
        l = constant_function_regex1.findall(js)
        # print("l 119",l)
        for i in l:
            function_name = re.search("var\s+([^=]+)", i).group(1)
            var_args_equal_value_functions.append(function_name)
            js = js.replace(i, "")
            # 替换全文
            a = function_name
            js = re.sub("%s\(([^\)]+)\)" % a, r"\1", js)

        # var 无参数 返回常量 函数
        var_no_args_return_constant_functions = []
        """
        var Qh_ = function() {
                'return Qh_';
                return ';';
            };
        """
        constant_function_regex2 = re.compile("""
                var\s+[^=]+=\s*function\(\)\{\s*
                    [\'\"]return\s*\w+\s*[\'\"];\s*
                    return\s+[\'\"][^\'\"]+[\'\"];\s*
                    \};
                """,
                                              re.X)
        l = constant_function_regex2.findall(js)
        # print("l 144",l)
        for i in l:
            function_name = re.search("""
                var\s+([^=]+)=\s*function\(\)\{\s*
                    [\'\"]return\s*\w+\s*[\'\"];\s*
                    return\s+[\'\"]([^\'\"]+)[\'\"];\s*
                    \};
                """,
                                      i,
                                      re.X)
            var_no_args_return_constant_functions.append(function_name.groups())
            js = js.replace(i, "")
            # 替换全文
            a, b = function_name.groups()
            all_var["%s()" % a] = b

        # 无参数 返回常量 函数
        no_args_return_constant_functions = []
        """
        function ZP_() {
                'return ZP_';
                return 'E';
            }
        """
        constant_function_regex3 = re.compile("""
                function\s*\w+\(\)\s*\{\s*
                    [\'\"]return\s*[^\'\"]+[\'\"];\s*
                    return\s*[\'\"][^\'\"]+[\'\"];\s*
                \}\s*
            """,
                                              re.X)
        l = constant_function_regex3.findall(js)
        # print("l 176",l)
        for i in l:
            function_name = re.search("""
                function\s*(\w+)\(\)\s*\{\s*
                    [\'\"]return\s*[^\'\"]+[\'\"];\s*
                    return\s*[\'\"]([^\'\"]+)[\'\"];\s*
                \}\s*
            """,
                                      i,
                                      re.X)
            no_args_return_constant_functions.append(function_name.groups())
            js = js.replace(i, "")
            # 替换全文
            a, b = function_name.groups()
            all_var["%s()" % a] = b

        # 无参数 返回常量 函数 中间无混淆代码
        no_args_return_constant_sample_functions = []
        """
        function do_() {
                return '';
            }
        """
        constant_function_regex3 = re.compile("""
                function\s*\w+\(\)\s*\{\s*
                    return\s*[\'\"][^\'\"]*[\'\"];\s*
                \}\s*
            """,
                                              re.X)
        l = constant_function_regex3.findall(js)
        # print("l 206",l)
        for i in l:
            function_name = re.search("""
                function\s*(\w+)\(\)\s*\{\s*
                    return\s*[\'\"]([^\'\"]*)[\'\"];\s*
                \}\s*
            """,
                                      i,
                                      re.X)
            no_args_return_constant_sample_functions.append(function_name.groups())
            js = js.replace(i, "")
            # 替换全文
            a, b = function_name.groups()
            all_var["%s()" % a] = b

        # 字符串拼接时使无参常量函数
        """
        (function() {
                    'return sZ_';
                    return '1'
                })()
        """
        constant_function_regex6 = re.compile("""
                \(function\(\)\s*\{\s*
                    [\'\"]return[^\'\"]+[\'\"];\s*
                    return\s*[\'\"][^\'\"]*[\'\"];?
                \}\)\(\)
            """,
                                              re.X)
        l = constant_function_regex6.findall(js)
        # print("l 236",l)
        for i in l:
            function_name = re.search("""
                \(function\(\)\s*\{\s*
                    [\'\"]return[^\'\"]+[\'\"];\s*
                    return\s*([\'\"][^\'\"]*[\'\"]);?
                \}\)\(\)
            """,
                                      i,
                                      re.X)
            js = js.replace(i, function_name.group(1))

        # 字符串拼接时使用返回参数的函数
        """
        (function(iU__) {
                    'return iU_';
                    return iU__;
                })('9F')
        """
        constant_function_regex6 = re.compile("""
                \(function\(\w+\)\s*\{\s*
                    [\'\"]return[^\'\"]+[\'\"];\s*
                    return\s*\w+;
                \}\)\([\'\"][^\'\"]*[\'\"]\)
            """,
                                              re.X)

        l = constant_function_regex6.findall(js)
        # print("l 264",l)
        for i in l:
            function_name = re.search("""
                \(function\(\w+\)\s*\{\s*
                    [\'\"]return[^\'\"]+[\'\"];\s*
                    return\s*\w+;
                \}\)\(([\'\"][^\'\"]*[\'\"])\)
            """,
                                      i,
                                      re.X)
            js = js.replace(i, function_name.group(1))
        #print("275", js)
        # 获取所有变量
        var_regex = "var\s+(\w+)=(.*?);\s"
        var_find = re.findall(var_regex, js)
        #print("var_find", var_find)
        for var_name, var_value in var_find:
            var_value = var_value.strip("\'\"").strip()
            # print(var_name,"---",var_value)
            if "(" in var_value:
                var_value = ";"
            all_var[var_name] = var_value
        #print("all var", all_var)
        # 注释掉 此正则可能会把关键js语句删除掉
        # js = re.sub(var_regex, "", js)

        for var_name, var_value in all_var.items():
            js = js.replace(var_name, var_value)
        #print("----282", js)
        js = re.sub("[\s+']", "", js)
        #print("----284", js)
        string_m = re.search("(%\w\w(?:%\w\w)+)", js)
        # string = urllib.parse.unquote(string_m.group(1)).encode("utf-8").decode("utf8")
        #print("string_m", string_m.groups())
        string = urllib.parse.unquote(string_m.group(1)).encode("utf-8").decode("utf8")
        #print(string)
        index_m = re.search("([\d,]+(;[\d,]+)+)", js[string_m.end():])
        #print(index_m.group())
        string_list = list(string)
        #print("str", len(string_list))
        # print("string_list",string_list)
        index_list = index_m.group(1).split(";")
        # print("index_list",index_list)
        _word_list = []
        # print(type(_word_list))
        # print(_word_list)
        i = 1
        exflag = 0;
        # deal exception

        # print("--max ",type(int(max(index_list))))
        max_index = 0;
        for word_index_list in index_list:
            _word = ""
            if "," in word_index_list:
                word_index_list = word_index_list.split(",")
                word_index_list = [int(x) for x in word_index_list]
            else:
                word_index_list = [int(word_index_list)]
            for word_index in word_index_list:
                # print(word_index)
                if (word_index > max_index):
                    max_index = word_index
                try:
                    string_list[word_index]
                except Exception as e:
                    exflag = 1;
        print(max_index)
        print("exflag", exflag)
        less = max_index - len(string_list)
        print(less)
        for word_index_list in index_list:
            _word = ""
            if "," in word_index_list:
                word_index_list = word_index_list.split(",")
                # print("word_index_list",word_index_list)
                word_index_list = [int(x) for x in word_index_list]
                # print("word_index_list", word_index_list)
            else:
                word_index_list = [int(word_index_list)]
            j = 1;
            for word_index in word_index_list:
                # print("for",j)
                j += 1
                # print("word_index",word_index)
                # print("string_list[word_index]",string_list[word_index])
                try:
                    _word += string_list[word_index - 1 - less]
                except Exception as e:
                    print(e)

            # print(_word)
            _word_list.append(_word)
            # print("----------")
            # print(i)
            # print(_word_list)

            i += 1

        return _word_list