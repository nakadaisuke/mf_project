#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'daisuke'
import re
import csv
from HTMLParser import HTMLParser

url = open("/Users/daisuke/Documents/python/lowhtml/201511.html")
csvfile = open("/Users/daisuke/Documents/python/lowhtml/201511.csv", "ab")

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
                str_data = re.sub('^[ \n\r\t]+|[ \n\r\t]+$', '', data).encode('utf-8')
                self.DATALIST.append(str_data)
                print str_data
            elif self.record == "content":
                str_data = re.sub('^[ \n\r\t]+|[ \n\r\t]+$', '', data).encode('utf-8')
                self.DATALIST.append(str_data)
                print str_data
            elif self.record == "price":
                str_data = re.sub('^[ \n\r\t]+|[ \n\r\t]+$', '', data).encode('utf-8')
                self.DATALIST.append(str_data)
                print str_data
            elif self.record == "ltag":
                str_data = re.sub('^[ \n\r\t]+|[ \n\r\t]+$', '', data).encode('utf-8')
                self.DATALIST.append(str_data)
                print str_data
            elif self.record == "mtag":
                str_data = re.sub('^[ \n\r\t]+|[ \n\r\t]+$', '', data).encode('utf-8')
                self.DATALIST.append(str_data)
                print str_data
                self.CSVLIST.append(self.DATALIST)
                self.DATALIST = []

    def clean(self):
        self.reset()
        self.NEWATTRS = []
        self.DATALIST = []
        self.record = ""

html = url.read()
parser = out_link_parser()

parser.feed(html.decode('utf-8'))

dataWriter = csv.writer(csvfile)
dataWriter.writerows(parser.CSVLIST)

csvfile.close()
url.close()
parser.clean()