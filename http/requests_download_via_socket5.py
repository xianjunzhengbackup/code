
# coding: utf-8

# In[1]:

#url is a download address
#python requests_download_via_socket5.py url


# In[8]:

import sys
import requests
import re
import os
import time


# In[2]:

#url = str(sys.argv[1])
#url='http://www.chnaus.com/forum.php?mod=viewthread&tid=198569
fp=open('south_download.list','rb')


# In[3]:

headers={'Content-Type':'application','User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3'}


# In[4]:

proxies = {'http': "socks5://127.0.0.1:9050"}


# In[6]:

def download_file(url,headers,proxies):
    req=requests.get(url=url,headers=headers,proxies=proxies)
    content=req.content
    pattern=re.compile(r'\d{6}')
    result=pattern.search(url)
    if result:
        fn=result.group()
        with open(fn,'wb') as fp:
            fp.write(content)
            print(url+' was fininsh!\n')
            os.system('sed -i 1d south_download.list')


# In[7]:

counter =0
for link in fp.readlines():
    counter = counter + 1
    download_file(link.decode('utf-8'),headers=headers,proxies=proxies)
    time.sleep(1)
    if counter == 20:
        os.system('service tor restart') 
        print("Tor is restarting now.....")
        time.sleep(20)
        counter =0


# In[ ]:



