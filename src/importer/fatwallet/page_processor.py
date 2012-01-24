#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import urllib2,cookielib
import re
import string
from db.database import Connection
from include.BeautifulSoup import BeautifulSoup

class PageProcessor():
    
    def __init__(self,html):
        self.html=html
        self.soup = BeautifulSoup(self.html)
    
    def isFirstPage(self):
        if self.soup.find('div',{'class':'userMsg', 'id':'firstPostText'})!=None:
            return True
        else:
            return False
        
    def getTitle(self):
        if self.isFirstPage()==True:
            title = self.soup.find('div',{'class':'post_title'}).findAll(lambda tag:tag.name=='a',text=True)
            title = ''.join(title)
            title = title.replace('google_ad_region_start=title', '')
            title = title.replace('google_ad_region_end=title', '')
            title = title.replace('Archived From: Hot Deals', '')
            title = title.replace('&amp', '')
            title = title.replace('\n','')
            return title.strip()
        else:
            print >> sys.stderr, 'it is not the first page'
    
    def getRating(self):
        pass
    
    def getReplyNum(self):
        pass
    
    def getViewNum(self):
        pass
    
    def getPostTime(self):
        if self.isFirstPage():
            time = self.soup.find('div',{'class':'post_date'}).findAll(lambda tag:tag.name!='b',text=True)
            time = ''.join(time)
            time = time.replace('posted:', '')
            time = time.replace('updated:', '')
            time = time.replace('\n','')
            return time.strip()
        else:
            print >> sys.stderr, 'it is not the first page' 
    
    def getDescription(self):
        if self.isFirstPage():
            content = self.soup.find('div',{'class':'userMsg', 'id':'firstPostText'}).findAll(lambda tag:tag.name=='table',text=True)
            return (''.join(content[1:-1])).strip()
        else:
            print >> sys.stderr, 'it is not the first page' 
                
    def getCategory(self):
        pass
    
    def getFeedback(self):
        pass
    
    def getUser(self):
        if self.isFirstPage():
            username = self.soup.find('li',{'class':'user_name'}).findAll(lambda tag:tag.name!='span',text=True)
            return (''.join(username)).strip()
        else:
            print >> sys.stderr, 'it is not the first page'   
    
def output(row):
    test = PageProcessor(row.text_html)
    print '=========================='
    print 'URL',row.url
    print 'TITLE:',test.getTitle()
    print 'USER:',test.getUser()
    print 'DESC:',test.getDescription()
    print 'TIME:',test.getPostTime()   

def save(row, db):
    pp = PageProcessor(row.text_html)
    db.query('update fatwallet set title=%s, user=%s, desc=%s, posted_time=%s where id=%s',pp.getTitle(), pp.getUser(), pp.getDescription(), pp.getPostTime(), row.id)

def main():
    host = 'localhost'
    database = 'resys'
    user = 'root'
    password = ''
    db = Connection(host,database,user,password)
    for row in db.query('select * from fatwallet'):
        if row.url.find('?start=0')!=-1 or re.match('^http://www.fatwallet.com/forums/hot-deals/[0-9]+/$',row.url)!=None:
            output(row)
            save(row,db)

    #===========================================================================
    # print re.findall('<div class="post_title"><div style=".*"><h1 style=".*"><a href=".*"><!--.*-->(.*)<!--.*--></a></h1>.*</div></div>',html,re.S)
    # soup = BeautifulSoup(html)
    # print soup.prettify()
    # title = soup.find('div',{'class':'userMsg', 'id':'firstPostText'}).findAll(lambda tag:tag.name=='tr',text=True)
    # print title
    # print ''.join(title[1:-1])
    #===========================================================================
  
if __name__ == '__main__':
    main()   

