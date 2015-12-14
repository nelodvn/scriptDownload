# -*- coding: latin-1 -*-

import requests
import urllib2
import os
from BeautifulSoup import BeautifulSoup
from time import sleep 

def getURL(page):
    start_link = page.find("a href")
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1: end_quote]
    return url, end_quote

def download(url, pageCount):
	file_name = url.split('/')[-1]
	file_name = file_name.replace("%20", " ")
	u = urllib2.urlopen(url)

	if not os.path.exists('/tmp/lelivros'):
		os.makedirs('/tmp/lelivros')
	if not os.path.exists('/tmp/lelivros/page' + pageCount):
		os.makedirs('/tmp/lelivros/page' + pageCount)

	f = open('/tmp/lelivros/' + 'page' + pageCount + '/' + file_name, 'wb')
	meta = u.info()
	file_size = int(meta.getheaders("Content-Length")[0])
	#print "Downloading: %s Bytes: %s" % (file_name, file_size)
	print "         dOWNLOADING :: %s :: bYTES ::" % (file_name),

	file_size_dl = 0
	block_sz = 8192
	while True:
	    buffer = u.read(block_sz)
	    if not buffer:
	        break
	    file_size_dl += len(buffer)
	    f.write(buffer)
	    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
	    status = status + chr(8)*(len(status)+1)
	    print status,

	f.close()
	return status

cont = 1
print "     iNFO :: Os livros serão salvos na pasta /tmp/lelivros"
while True:
	url = "http://lelivros.website/book/page/" + str(cont) + "/"
	print('     iNFO :: Pagnia atual: ' + str(cont))
	response = requests.get(url)
	# parse html
	page = str(BeautifulSoup(response.content))
	urlAnterior = ''
	while True:
	    url, n = getURL(page)
	    page = page[n:]
	    if url: 
	    	if "http://lelivros.website/book" in url: 
	    		if url != urlAnterior:
	    			#print url
		    		responseDownload = requests.get(url)
		    		pageDownload = str(BeautifulSoup(responseDownload.content))
		    		while True:
		    			urlDownload, n = getURL(pageDownload)
		    			pageDownload = pageDownload[n:]
		    			if urlDownload:
		    				if ".mobi" in urlDownload:
		    					print(download(urlDownload, str(cont)))
		    			else:
		    				break
	    	urlAnterior = url
	    else:
	        break
	cont = cont + 1