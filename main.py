import urllib2
import re
from bs4 import BeautifulSoup

html_path_lst = ["https://s.2.taobao.com/list/list.htm?spm=2007.1000337.6.2.57041f73tt69mQ&st_edtime=1&start=100&q=%C0%D6%B8%DF&ist=0"]
page_id = 1
node_list = []

def item_id_str2int(str):
    pattern = re.compile(r'\d+')
    result = pattern.findall(str)
    for str_id in result:
        if int(str_id) > 9999 and int(str_id) < 100000:
            return int(str_id)
    return 0

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
        


list_head = LIST_NODE_HEAD()


for html_path in html_path_lst:
    response = urllib2.urlopen(html_path)
    html = response.read()
    soup = BeautifulSoup(html)
    item_lst = soup.find_all(class_='item-info')
    for item_html in item_lst:
        item_id = item_id_str2int(item_html.h4.a.string)
        if item_id > 0:
            item = ITEM(item_id, float(item_html.div.find_next_sibling(class_='item-price price-block').span.em.string))
            list_head.insert_node(item)
        #print item[2].h4.a.string #item name
        #print item[2].div.find_next_sibling(class_='item-price price-block').span.em.string #item price


list_head.print_all()

#print soup.prettify()
#print soup.p
#print soup.div()

#item = soup.find_all(class_='item-info')
#print item[2].h4.a.string #item name
#print item[2].div.find_next_sibling(class_='item-price price-block').span.em.string #item price

