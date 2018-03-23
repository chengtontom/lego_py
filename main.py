#coding=utf-8

import urllib2
import re
import sys
import types

from bs4 import BeautifulSoup

max_page_id = 20
html_parse = "&q=%C0%D6%B8%DF&ist=0"

search_keyword = "乐高"
traditional_search_keyword = "樂高"
hk_exchange = 0.81
low_price = 500
high_price = 15000

def get_chn_2_asc_str(search_keyword):
    key_asc = map(ord, search_keyword)
    asc_str = ""
    for c in key_asc:
        asc_str += "%" + str(hex(c))[2:]
    return asc_str
     
def get_spm_id(search_keyword):
    asc_str = get_chn_2_asc_str(search_keyword)
    html_path = "https://s.2.taobao.com/list/list.htm?q=%s&search_type=item&_input_charset=utf8 " % (asc_str)

    response = urllib2.urlopen(html_path)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    item = soup.find_all(attrs={"name": "spm-id"})
    if item[0]['content']:
        return item[0]['content']
    return ""

def item_id_str2int(str):
    pattern = re.compile(r'\d+')
    result = pattern.findall(str)
    for str_id in result:
        if int(str_id) > 999 and int(str_id) < 100000:
            return int(str_id)
    return 0
        
def get_str_float_value(str):
    pattern = re.compile(r'\-*\d+(?:\.\d+)?')
    result = pattern.findall(str)
    value = float(result[0])
    return value
        
def get_str_int_value(str):
    pattern = re.compile(r'\d+')
    result = pattern.findall(str)
    return int(result[0])

def print_wait_dot():
    sys.stdout.write(".")
    sys.stdout.flush()
    
class ITEM:
    'item'
    def __init__(self, id, price, sell_cnt = 1):
        self.id = id
        self.price = price 
        self.sell_cnt = sell_cnt 
    
class LIST_NODE:
    'list node'
    def __init__(self,id):
        self.id = id
        self.sell_cnt = 0
        self.price = []
    def is_same_id(self, id):
        if self.id == id :
            return True
    def insert_price(self, price):
        self.price.append(price);
    def print_all(self):
        print "id = %d" % (self.id)
        print "sell_cnt = %d" % (self.sell_cnt)
        for p in self.price :
            print "p = %d" % (p)
    def get_price_avg(self) :
        sum = 0
        number = len(self.price)
        for p in self.price :
            sum += p
        if(number) : 
            return float(float(sum)/number)
        return 0
    def get_price_mid(self) :
        sum = 0
        number = len(self.price)
        if (number % 2) == 1 :
            return self.price[number/2]
        else :
            return (self.price[number/2-1] + self.price[number/2])/2

class LIST_NODE_HEAD:
    'list node'
    def __init__(self, name, exchange = 1):
        self.list = []
        self.name = name
        self.exchange = exchange
    def insert_node(self, item):
        for node in self.list:
            if(node.is_same_id(item.id)):
                node.insert_price(item.price)
                node.sell_cnt += item.sell_cnt
                return
        new_node = LIST_NODE(item.id)
        new_node.insert_price(item.price)
        new_node.sell_cnt += item.sell_cnt
        self.list.append(new_node)
    def print_all(self):
        print self.name + "Info :"
        for node in self.list:
            node.print_all()
    def sort_by_price_number(self) :    
        self.list.sort(lambda n1 , n2 : - cmp ( len(n1.price) , len(n2.price) ))
        for node in self.list :
            node.price.sort(lambda p1 , p2 : - cmp ( p1 , p2))
    def sort_by_sell_number(self) :    
        self.list.sort(lambda n1 , n2 : - cmp ( n1.sell_cnt , n2.sell_cnt ))
        for node in self.list :
            node.price.sort(lambda p1 , p2 : - cmp ( p1 , p2))
    def print_info(self):
        print self.name + " Info :"
        print "id\tshop\tsell\thigh-price\tlow-price\tavg-price\tmid-price"
        for node in self.list :
            print "%d\t%d\t%d\t%.1f\t\t%.1f\t\t%.1f\t\t%.1f" % (node.id, len(node.price), node.sell_cnt, node.price[0], node.price[-1], node.get_price_avg(), node.get_price_mid()) 
    def print_one_info(self, id):
        print self.name + " Info :"
        print "id\tcounts\thigh-price\tlow-price\tavg-price\tmid-price"
        for node in self.list :
            if(node.id == id):
                print "%d\t%d\t%d\t%.1f\t\t%.1f\t\t%.1f\t\t%.1f" % (node.id, len(node.price), node.sell_cnt, node.price[0], node.price[-1], node.get_price_avg(), node.get_price_mid()) 
                break  
    def print_one_mid(self, id):
        for node in self.list :
            if(node.id == id):
                return node.get_price_mid()
    def print_one_sell(self, id):
        for node in self.list :
            if(node.id == id):
                return node.sell_cnt
        return 0        
    def xy_run(self):
        print_wait_dot()
        key_spm_id = get_spm_id(search_keyword)
        for page_id in range(1,max_page_id+1):
            print_wait_dot()
            html_path = "https://s.2.taobao.com/list/list.htm?spm=%s&st_edtime=1&start=%d&end=%d&page=%d&%s" % (key_spm_id, low_price, high_price, page_id, html_parse)
            response = urllib2.urlopen(html_path)
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            item_lst = soup.find_all(class_='item-info')
            for item_html in item_lst:
                item_id = item_id_str2int(item_html.h4.a.string)
                if item_id > 0:
                    item = ITEM(item_id, float(item_html.div.find_next_sibling(class_='item-price price-block').span.em.string))
                    self.insert_node(item)
        self.sort_by_sell_number()
    def tb_run(self):
        print_wait_dot()
        asc_str = get_chn_2_asc_str(search_keyword)
        for page_id in range(0,max_page_id):
            print_wait_dot()
            html_path = "https://s.taobao.com/search?data-key=s&data-value=%d&ajax=true&_ksTS=1521788061338_2677&callback=jsonp2678&q=%s&imgfile=&js=1&stats_click=search_radio_all:1&initiative_id=staobaoz_20180323&ie=utf8&style=list&sort=sale-desc&filter=reserve_price[%s,%d]&bcoffset=0&p4ppushleft=,44&s=44" % (page_id*44, asc_str, low_price, high_price)
            response = urllib2.urlopen(html_path)
            html = response.read()
            html_split =  html.split('{')
            for split_one_html in html_split:
                if split_one_html.find("raw_title") > 0 :
                    split_one_item = split_one_html.split(',')
                    item_get_value = False
                    item_ready = 0
                    for item_attr in split_one_item :
                        if item_attr.find('raw_title') > 0:
                            item_id = item_id_str2int(item_attr)
                            if item_id > 0 :
                                item_get_value = True
                                item_ready += 1
                        elif item_get_value and item_attr.find('view_price') > 0:
                            price = get_str_float_value(item_attr)
                            item_ready += 1
                        elif item_get_value and item_attr.find('view_sales') > 0:
                            sell_cnt = get_str_int_value(item_attr)
                            item_ready += 1
                        if item_ready == 3 :
                            item = ITEM(item_id, price, sell_cnt)
                            self.insert_node(item)
                            item_ready = 0
        self.sort_by_sell_number()
    def hk_run(self):
        asc_str = get_chn_2_asc_str(traditional_search_keyword)
        print_wait_dot()
        for page_id in range(1,max_page_id+1):
            print_wait_dot()
            html_path = "https://hk.auctions.yahoo.com/search/?acu=1&cid=0&clv=0&kw=%s&maxp=%d&minp=%d&p=%s&pg=%d&refine=con_new" % (asc_str, high_price, low_price, asc_str, page_id)
            response = urllib2.urlopen(html_path)
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            item_name_lst = soup.find_all(class_='GridItem__title___3Dnzw')
            item_price_lst = soup.find_all(class_='GridItem__price___23XQ9')
            for (item_name, item_price) in zip(item_name_lst,item_price_lst):
                item_id = item_id_str2int(item_name.string)
                if item_id > 0:
                    if item_price.string is None : 
                        print "Network error..."
                    else :
                        price = get_str_float_value(item_price.string)
                        item = ITEM(item_id, price)
                        self.insert_node(item)
        self.sort_by_sell_number()
        sys.stdout.write("\n")
    def cmp_analysis(self, cmp_lst):
        print self.name + " Info :"
        print("id\tcounts\tprice\tc-cnt\tc-p(hk)\tc-p(c)\tprofit\tprofit_pct")
        for node in self.list:
            cmp_mid = cmp_lst.print_one_mid(node.id)
            self_mid = node.get_price_mid() 
            if cmp_mid > 0:
                cmp_sell = cmp_lst.print_one_sell(node.id)
                cmp_ex_mid = cmp_mid * cmp_lst.exchange
                profit = self_mid - cmp_ex_mid
                profit_pct = float(profit/float(cmp_mid));
                print "%d\t%d\t%.1f\t%d\t%.1f\t%.1f\t%.1f\t%.3f" % (node.id, node.sell_cnt, cmp_mid, cmp_sell, self_mid, cmp_ex_mid, profit, profit_pct)
            else :
                print "%d\t%d\t%.1f\t*\t*\t*\t*\t*" % (node.id, node.sell_cnt, self_mid)

def show_cmd():
    print "r : run(1:xy, 2:tb 3:hk)"
    print "g : get"
    print "s : set"
    print "d : debug"
    print "a : analysis"
    print "q : quit"

show_cmd()

xy_list_head = LIST_NODE_HEAD("Xianyu")
tb_list_head = LIST_NODE_HEAD("Taobao")
hk_list_head = LIST_NODE_HEAD("HK", exchange = hk_exchange)

while 1 :
    cmd = sys.stdin.readline()
    if(cmd[0] == 'q') :
        break
    elif(cmd[0] == 'd') :
        if((len(cmd) <4) or (int(cmd[2:]) == 0)) :
            print "d 1 : show full list"
            print "d 2 : show page range"
        elif(int(cmd[2:]) == 1) :
            xy_list_head.print_all()
            tb_list_head.print_all()
            hk_list_head.print_all()
        elif(int(cmd[2:]) == 2) :
            print "page max range 1-%d" % (max_page_id)
    elif(cmd[0] == 's') :
        if((len(cmd) <4) or (int(cmd[2]) == 0)) :
            print "s 1 : set page range arg1:id"
        elif(int(cmd[2:3]) == 1) :
            max_page_id = int(cmd[4:])
    elif(cmd[0] == 'r') :
        if((len(cmd) <4) or (int(cmd[2:]) == 0)) :
            tb_list_head.tb_run()
            xy_list_head.xy_run()
            hk_list_head.hk_run()
            tb_list_head.print_info()
            xy_list_head.print_info()
            hk_list_head.print_info()
        elif(int(cmd[2:]) == 1) :
            xy_list_head.xy_run()
            xy_list_head.print_info()
        elif(int(cmd[2:]) == 2) :
            tb_list_head.tb_run()
            tb_list_head.print_info()
        elif(int(cmd[2:]) == 3) :
            hk_list_head.hk_run()
            hk_list_head.print_info()
    elif(cmd[0] == 'g') :
        item_id = 0
        if (len(cmd) <4) or item_id == 0 :
            tb_list_head.print_info()
            xy_list_head.print_info()
            hk_list_head.print_info()
        else :    
            item_id = int(cmd[2:])
            xy_list_head.print_one_info(int(cmd[2:]))
            tb_list_head.print_one_info(int(cmd[2:]))
            hk_list_head.print_one_info(int(cmd[2:]))
    elif(cmd[0] == 'a') :
            xy_list_head.cmp_analysis(hk_list_head)
            tb_list_head.cmp_analysis(hk_list_head)
    else :
        show_cmd()

