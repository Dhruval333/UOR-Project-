import requests as ureq
from bs4 import BeautifulSoup
import os
import re
# Feature =r'C:\Users\Admin\Documents\WORK\Feature_story\Feature.html'
url = 'https://www.uregina.ca/external/communications/feature-stories/current/2019/01-07.html'
r = ureq.get(url)
soup = BeautifulSoup(r.content,'lxml')
body = soup.find('div',id='dspace')
# read file
f = open("Feature.html","r")
temp = f.readlines()
temp = [line % {'ads_block': body} for line in temp]
f = open("Feature.html","w")
f.writelines(temp)
f.close()
# print("completed")