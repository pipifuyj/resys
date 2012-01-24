#!/usr/bin/python
# -*- coding: utf-8 -*-
from importer.spider import Spider
from db.database import Connection
import string

class FatwalletSpider(Spider):
    def __init__(self, beginurl, reg, priorcontent, pages, downloadFolder, host, database, user=None, password=None):
        super(FatwalletSpider, self).__init__(beginurl, reg, priorcontent, pages, downloadFolder)
        self.db=Connection(host,database,user,password)
        
    def saveHTML(self, url, html, path):
        md5=self.md5(html)
        raw_html=html
        text_html=''.join([c for c in html if c in string.printable])
        self.insertHTML2DB('fatwallet', url, raw_html, text_html, md5)
        super(FatwalletSpider, self).saveHTML(url,html)
    
    def insertHTML2DB(self, TABLE, URL, RAW, TEXT, MD5):
        self.db.insert(TABLE, url=URL,raw_html=RAW,text_html=TEXT, md5=MD5)

def main():
    "main function used to do test for class spider "
    #initialization
    beginurl = 'http://www.fatwallet.com/forums/hot-deals/985386/?start=0'  #the begin url
    reg = '^http://www.fatwallet.com/forums/hot-deals/[0-9a-zA-Z?#=/]{1,}$'
    pages = 100   #number of web pages to be crawled
    downloadFolder = './spiderDown' #web pages stored location
    priorcontent = '?start=0'
    host = 'localhost'
    database = 'resys'
    user = 'root'
    password = ''
    
    #start crawling
    fatwallet = FatwalletSpider(beginurl, reg, priorcontent, pages, downloadFolder, host, database, user, password)
    fatwallet.run()
 
if __name__ == '__main__':
    main()      