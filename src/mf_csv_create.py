#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re
from HTMLParser import HTMLParser
import codecs
import sys
import unicodedata

class out_link_parser(HTMLParser):
    def __init__(self):
        self.reset()
        self.NEWATTRS = []
        self.DATALIST = []
        self.CSVLIST = []
        self.active_flag = ""
        self.record = ""

    def handle_starttag(self, tag, attrs):
        if tag == "i":
            self.record = False
        if tag == "tr":
            attrs_length = len(attrs)
            if attrs_length != 0:
                if "js-cf-edit-container target-active transaction_list" in attrs[0]:
                    self.active_flag = "active"

        if tag == "td":
            self.NEWATTRS.append(attrs)
            attrs_length = len(attrs)
            if attrs_length != 0:
                if "date" in attrs[0] or "date form-switch-td" in attrs[0]:
                    if self.active_flag == "active":
                        self.record = "date"
                if "content" in attrs[0] or "content form-switch-td" in attrs[0]:
                    if self.active_flag == "active" and "" not in attrs:
                        self.record = "content"
                if "amount number plus-color" in attrs[0] or "amount minus-color number" in attrs[0] or "amount form-switch-td plus-color number" in attrs[0] or "amount form-switch-td minus-color number" in attrs[0]:
                    if self.active_flag == "active":
                        self.record = "price"
                if "lctg" in attrs[0]:
                    if self.active_flag == "active":
                        self.record = "ltag"
                if "mctg" in attrs[0]:
                    if self.active_flag == "active":
                        self.record = "mtag"

    def handle_endtag(self, tag):
        if tag == 'i':
            self.record = False
        if tag == 'tr':
            self.active_flag = ""
        if tag == 'td':
            self.record = False

    def handle_data(self, data):
        if data != "\n":
            if self.record == "date":
                str_data = re.sub('^[ \n\r\t]+|[ \n\r\t]+$', '', data).encode('utf-8') + ','
                self.DATALIST.append(str_data)
            elif self.record == "content":
                str_data = re.sub('^[ \n\r\t]+|[ \n\r\t]+$', '', data).encode('utf-8').replace(",",".") + ','
                self.DATALIST.append(str_data)
            elif self.record == "price":
                str_data = re.sub('^[ \n\r\t]+|[ \n\r\t]+$', '', data).encode('utf-8').replace(",","") + ','
                self.DATALIST.append(str_data)
            elif self.record == "ltag":
                str_data = re.sub('^[ \n\r\t]+|[ \n\r\t]+$', '', data).encode('utf-8') + ','
                self.DATALIST.append(str_data)
            elif self.record == "mtag":
                str_data = re.sub('^[ \n\r\t]+|[ \n\r\t]+$', '', data).encode('utf-8') + '\n'
                self.DATALIST.append(str_data)
                self.CSVLIST.append(self.DATALIST)
                self.DATALIST = []


    def clean(self):
        self.reset()
        self.NEWATTRS = []
        self.DATALIST = []
        self.record = ""


input_argvs = sys.argv
print input_argvs[1]
print input_argvs[2]

url = open(input_argvs[1], "r")
csvfile = codecs.open(input_argvs[2], "w", "shift-jis")
html = url.read()
parser = out_link_parser()
parser.feed(html.decode('utf-8'))

for i in parser.CSVLIST:
    for csvi in i:
        u_seci = unicode(csvi,"utf-8").replace(u"\u2014", u"\u2015")
        u_seci = u_seci.replace(u"\u309a", "")
        u_seci = u_seci.replace(u"\u9ad9", u"\u9ad8")
        csvfile.write(u_seci)


csvfile.close()
url.close()
parser.clean()