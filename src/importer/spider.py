#!/usr/bin/python
# -*- coding: utf-8 -*-
from importer.utility import PriorityQueue,Parser
import urllib2
import urllib
import sys
import os
import re
import hashlib
 
class Spider(object):
    musthave = ''
    beginurl = ''
    pages = ''
    downFolder = ''
    priQueue = PriorityQueue()
    downlist = PriorityQueue() 
    
    def __init__(self, beginurl, reg, priorcontent, pages, downloadFolder):
        self.reg = reg
        self.beginurl = beginurl
        self.pages = pages
        self.downFolder = downloadFolder
        self.priorcontent = priorcontent
        if not os.path.isdir( downloadFolder ):
            os.mkdir( downloadFolder )
        self.priQueue = PriorityQueue()
        self.downlist = PriorityQueue() 
        
    def md5(self, content):
        m=hashlib.md5()
        m.update(content)
        return m.hexdigest()
    
    def updatePriQueue(self, priQueue, url ):
        "input new web page to be crawled into priQueue"
        extraPrior = url.endswith('.html') and 2 or 0 #url with 'html' has higher priority 
        extraURL = self.priorcontent in url and 5 or 0 #
        item = priQueue.getitem(url)
        if item :
            newitem = ( item[0]+1+extraPrior+extraURL, item[1] )
            priQueue.remove(item)
            priQueue.push( newitem )
        else :
            priQueue.push( (1+extraPrior+extraURL,url) )
 
    def getMainUrl(self, url):
        "obtain the host address for URL"
        ix = url.find('/',len('http://') )
        if ix > 0 :
            return url[:ix]
        else :
            return url
 
    def analyseHtml(self, url, html):
        "analyze the html to find new URL to be crawled"
        p = Parser()
        try :
            p.feed(html)
            p.close()
        except:
            print ""
        mainurl = self.getMainUrl(url)
                
        for k, v in p.anchors.items():
            for u in v :
                if (not u.startswith('http://')) :  #handle the relative URL, transfer href ='test/1.html' to href='http://xxx/test/1.html'
                    u = mainurl + u      
                if not self.downlist.count(u) and re.match(self.reg, u) : #if url is not downloaded and match the required regular expression
                    print 'add new url: ' + u 
                    self.updatePriQueue( self.priQueue, u )
        
    def downloadUrl(self, id, url):
        "download the web page related to the specified URL and analyze the web page"
        headers = {
                   'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        }
        postdata=urllib.urlencode({
            'emailAddress':'pipifuyj@gmail.com',
            'password':'fuyanjie868686',
            'signIn':'1'
        })
        req = urllib2.Request(
            url = url,
            headers = headers,
            data = postdata
        )
        downFileName = self.downFolder+'/%d.html' %(id)
        print 'crawling: ', url, 
        try:
            fp = urllib2.urlopen(req)
        except:
            print '[ failed ]'
            return False
        else :
            print '[ success ]'
            self.downlist.push( url )  #add the downloaded url into downlist
            html = fp.read()
            self.saveHTML(url,html,downFileName)
            fp.close()
            print 'analyzing: ', url
            self.analyseHtml(url,html)
            return True
        
    def saveHTML(self,url,html,path=''):
        if path != '':
            print 'downloading',url,'as', path ,
            op = open(path,"wb")
            op.write( html )
            op.close()
    
    def usage(self):
        print >> sys.stderr,'this is a test for function'  

    def run(self):
        "spider running function, fetch the url from priority queue and crawl the web page, and then add new url into priority queque"
        self.priQueue.push( (1,self.beginurl) )
        i = 0
        fp = open('url.txt','w')   
        while not self.priQueue.empty() and i < self.pages :
            k, url = self.priQueue.pop()
            if self.downloadUrl(i+1, url):
                i += 1
                fp.write(url+' '+self.md5(url)+'\n')
                fp.flush()
        fp.close()
        print '\nDownload',i,'pages, Totally.'
            
def main():
    "main function used to do test for class spider "
    #initialization
    beginurl = 'http://www.fatwallet.com/forums/hot-deals/985386/?start=200'  #the begin url
    reg = '^http://www.fatwallet.com/forums/hot-deals/[0-9a-zA-Z?#=/]{1,}$'
    pages = 10000   #number of web pages to be crawled
    downloadFolder = './spiderDown' #web pages stored location
    priorcontent = '?start=0'
    
    #start crawling
    fatwallet = Spider( beginurl, reg, priorcontent, pages, downloadFolder)
    fatwallet.run()
 
if __name__ == '__main__':
    main()