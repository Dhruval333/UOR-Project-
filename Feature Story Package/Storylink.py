import requests as ureq
from bs4 import BeautifulSoup
import os
import pprint
import re

baseurl = "https://www.uregina.ca/external/communications/feature-stories/current/2021/"

def imgdown(folder):
    try:
        os.mkdir(os.path.join(os.getcwd(),folder))
    except:
        pass
    os.chdir(os.path.join(os.getcwd(),folder))
    r = ureq.get('https://www.uregina.ca/external/communications/feature-stories/current/2021/index.html')
    soup = BeautifulSoup(r.content,'lxml')

    storylinks = []

    for title in soup.find_all('td', class_='title'):
        for link in title.find_all('a', href=True):
                storylinks.append(baseurl + link['href'])
            
    # print(storylinks)

    # link = 'https://www.uregina.ca/external/communications/feature-stories/current/2019/12-23.html'
    # story = []
    for link in storylinks:
        r = ureq.get(link)
        soup = BeautifulSoup(r.content,'lxml')
        lin= soup.find('div',class_='globalCol_1_1')
        link = lin.findAll('img')
        for link in lin.findAll('img',src=True):
            story = baseurl + link['src']
            name = link['src']
            if story == 'https://www.uregina.ca/external/communications/feature-stories/current/2019/https://cascade.uregina.ca:8443/render/file.act?path=feature-stories/current/2019/images/theFalls-3.png':
                continue
            with open(name.replace('images','').replace('/','').replace('//','') + '','wb') as f:
                im = ureq.get(story)
                f.write(im.content)
                print('Writing:',name)

            # print(story)
            # story.append(baseurl + link['src'])
        
        # print(story)
    # print(story)
            # data = {
            # name = soup.find('h1').text,
        # stoylinks.append(data)
    
imgdown('images')