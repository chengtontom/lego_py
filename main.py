#coding=utf-8

import urllib2
import re
import sys
from bs4 import BeautifulSoup

html_path_lst = ["https://s.2.taobao.com/list/list.htm?spm=2007.1000337.6.2.57041f73tt69mQ&st_edtime=1&start=100&q=%C0%D6%B8%DF&ist=0"]
max_page_id = 20
node_list = []
html_parse = "&q=%C0%D6%B8%DF&ist=0"

search_keyword = "乐高"


class ITEM:
    'item'
    def __init__(self, id, price):
        self.id = id
        self.price = price 
    
class LIST_NODE:
    'list node'
    def __init__(self,id):
        self.id = id
        self.price = []
    def is_same_id(self, id):
        if self.id == id :
            return True
    def insert_price(self, price):
        self.price.append(price);
    def print_all(self):
        print "id = %d" % (self.id)
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
    def __init__(self):
        self.list = []
    def insert_node(self, item):
        for node in self.list:
            if(node.is_same_id(item.id)):
                node.insert_price(item.price)
                return
        new_node = LIST_NODE(item.id)
        new_node.insert_price(item.price)
        self.list.append(new_node)
    def print_all(self):
        for node in self.list:
            node.print_all()
    def sort_by_price_number(self) :    
        self.list.sort(lambda n1 , n2 : - cmp ( len(n1.price) , len(n2.price) ))
        for node in self.list :
            node.price.sort(lambda p1 , p2 : - cmp ( p1 , p2))
    def print_info(self):
        print "id\tcounts\thigh-price\tlow-price\tavg-price\tmid-price"
        for node in self.list :
            print "%d\t%d\t%.1f\t\t%.1f\t\t%.1f\t\t%.1f" % (node.id, len(node.price), node.price[0], node.price[-1], node.get_price_avg(), node.get_price_mid()) 
    def print_one_info(self, id):
        print "id\tcounts\thigh-price\tlow-price\tavg-price\tmid-price"
        for node in self.list :
            if(node.id == id):
                print "%d\t%d\t%.1f\t\t%.1f\t\t%.1f\t\t%.1f" % (node.id, len(node.price), node.price[0], node.price[-1], node.get_price_avg(), node.get_price_mid()) 
                break
    def run(self):
        for page_id in range(1,max_page_id):
            html_path = "https://s.2.taobao.com/list/list.htm?spm=%s&st_edtime=1&start=800&end=50000&page=%d&%s" % (key_spm_id, page_id, html_parse)
            response = urllib2.urlopen(html_path)
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            item_lst = soup.find_all(class_='item-info')
            for item_html in item_lst:
                item_id = item_id_str2int(item_html.h4.a.string)
                if item_id > 0:
                    item = ITEM(item_id, float(item_html.div.find_next_sibling(class_='item-price price-block').span.em.string))
                    self.insert_node(item)
        self.sort_by_price_number()
            
def get_spm_id(search_keyword):
    key_asc = map(ord, search_keyword)
    asc_str = ""
    for c in key_asc:
        asc_str += "%" + str(hex(c))[2:]
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
        if int(str_id) > 9999 and int(str_id) < 100000:
            return int(str_id)
    return 0



        #print item[2].h4.a.string #item name
        #print item[2].div.find_next_sibling(class_='item-price price-block').span.em.string #item price

def show_cmd():
    print "r : run"
    print "g : get"
    print "s : set"
    print "d : debug"
    print "q : quit"


key_spm_id = get_spm_id(search_keyword)
show_cmd()

list_head = LIST_NODE_HEAD()
while 1 :
    cmd = sys.stdin.readline()
    if(cmd[0] == 'q') :
        break
    elif(cmd[0] == 'd') :
        if((len(cmd) <4) or (int(cmd[2:]) == 0)) :
            print "d 1 : show full list"
            print "d 2 : show page range"
        elif(int(cmd[2:]) == 1) :
            list_head.print_all()
        elif(int(cmd[2:]) == 2) :
            print "page max range 1-%d" % (max_page_id)
    elif(cmd[0] == 's') :
        if((len(cmd) <4) or (int(cmd[2]) == 0)) :
            print "s 1 : set page range arg1:id"
        elif(int(cmd[2:3]) == 1) :
            max_page_id = int(cmd[4:])
    elif(cmd[0] == 'r') :
        list_head.run()
        list_head.print_info()
    elif(cmd[0] == 'g') :
        list_head.print_one_info(int(cmd[2:]))
    else :
        show_cmd()


