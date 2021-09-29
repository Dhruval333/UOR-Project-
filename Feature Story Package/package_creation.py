from urllib.request import urlopen as ureq
import requests as urq
from datetime import datetime
from bs4 import BeautifulSoup
import shutil,os
import os.path
import sys, codecs

# Change the year as per the story index required (Apply the change to both baseurl as well as r)
baseurl = "https://www.uregina.ca/external/communications/feature-stories/current/2019/"
r = ureq('https://www.uregina.ca/external/communications/feature-stories/current/2019/index.html')
soup = BeautifulSoup(r,"html5lib")

storylinks = []
store_count = {}
for title in soup.find_all('td', class_='title'):
    for link in title.find_all('a', href=True):
        storylinks.append(baseurl + link['href'])
        
# Featching data from site using soup
for link in storylinks:
    r = ureq(link)
    soup = BeautifulSoup(r,"html5lib")
    date = soup.find('span', class_='date').text
    date = datetime.strptime(date,'%B %d, %Y').strftime('%Y-%m-%d') 
    month = datetime.strptime(date,'%Y-%m-%d').strftime('%m-%B')
    year = datetime.strptime(date,'%Y-%m-%d').strftime('%Y')
    day = datetime.strptime(date,'%Y-%m-%d').strftime("%d")
    lin = soup.find('div',class_='globalCol_1_1')
    link_new = lin.findAll('img')
    body = soup.find('div',id='dspace')
    # read file

    # template for feature file:
    htmlstr =  """
    <!DOCTYPE html>
      <head>
        
        <title>University of Regina - External Relations</title>


        <link rel="stylesheet" href="combine.css" />  

      </head>

      <body>

        <div id="container">

          <div id="rhs">

            <div id="content">

              <!-- Begin Main Content Area -->    

              <div id="standardcontainer">
            <!-- Extracted Content Goes Here - Begin -->  

                 %(ads_block)s 

            <!-- Extracted Content Goes Here - End --> 
              </div>

              <!-- End Main Content Area -->

            </div>

          </div>

        </div>

      </body>
    </html>
    """

    # Creating month file
    if not os.path.exists(year):
      os.makedirs(year)
    m = os.path.join('/Users/Admin/Documents/WORK/testenv/%s/'%year,month)
    if not os.path.exists(m):
        os.makedirs(m)

    #Bypass pages encoding error
    if (month == '08-August' and day == '30' or day == '13'): 
      continue
    # if (month == '08-August' and day == '22' or day == '17'or day == '11' or day == '08' or day == '07' or day == '04'): 
    #   continue

    new_fld = ("Feature_%s" %date)
    folder = os.path.join('/Users/Admin/Documents/WORK/testenv/%s/%s/'% (year,month),new_fld)
    filename = ("Featur_%s.html" % date)
    file = os.path.join(folder,filename)
    src_file = "/Users/Admin/Documents/WORK/testenv/fol"
    
    #Creating sub folder 
    if os.path.exists(folder):
        
        store_count[str(folder)]+= 1
        new_fld = ("Feature_%s" % date)+"("+ str(store_count[str(folder)]) +")"
        filename = ("Feature_%s" % date)+"("+ str(store_count[str(folder)]) +")" + ".html"
        folder = os.path.join('/Users/Admin/Documents/WORK/testenv/%s/%s/'%(year,month),new_fld)
        file = os.path.join(folder,filename)
        src_file = "/Users/Admin/Documents/WORK/testenv/fol"
        os.makedirs(folder)

    else:
        store_count[str(folder)] = int(0)
        os.makedirs(folder)

    for f in os.listdir(src_file):
      filepath = os.path.join(src_file,f)
      shutil.copy(filepath,folder)

    
    #Image download process
    for link_new in lin.findAll('img',src=True):
      story = baseurl + link_new['src']
      name = link_new['src']
       
      #Bypass dead link and image
      if story == 'https://www.uregina.ca/external/communications/feature-stories/current/2019/https://cascade.uregina.ca:8443/render/file.act?path=feature-stories/current/2019/images/theFalls-3.png':
        continue
      if name == 'https://counter.theconversation.com/content/151769/count.gif?distributor=republish-lightbox-advanced':
        continue
      name = name.replace('../2018/','').replace('images/','').replace('/','').replace('//','').replace('../','').replace('..','')
      f = open("" + folder + '/' + name + '','wb')
      im = urq.get(story)
      f.write(im.content)
      print('Writing:',name)
      f.close()
    
    
    #Image naming
    for a in body.find_all('img',src=True):
      a['src'] = a['src'].replace('images/','').replace('../2018/','').replace('../','').replace('..','')
      a['src']  = './' + a['src']
      # a['src'] = a['src'].replace(a['src'],a)
      print (a['src'])

    f = open(file,"w", encoding='utf-8')
    f.write(htmlstr)
    f.close()
    f = open(file,"r")
    temp = f.readlines()
    temp = [line % {'ads_block': body} for line in temp]   # %(ads_block)s
    f = open(file,"w")
    f.writelines(temp)
    f.close()
    

      
  
