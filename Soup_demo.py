import json
import requests as ureq
from bs4 import BeautifulSoup
import pandas as pd
import pprint

baseurl = "https://www.uregina.ca/external/communications/feature-stories/current/2019/"


r = ureq.get('https://www.uregina.ca/external/communications/feature-stories/current/2019/index.html')
soup = BeautifulSoup(r.content,'lxml')

storylinks = []

for title in soup.find_all('td', class_='title'):
    for link in title.find_all('a', href=True):
        storylinks.append(baseurl + link['href'])
        
# print(storylinks)

# testlink = 'https://www.uregina.ca/external/communications/feature-stories/current/2019/12-23.html'
# with open('test.json','w') as f:
datalist = []
for link in storylinks:
        r = ureq.get(link)
        soup = BeautifulSoup(r.content,'lxml')
        name = soup.find('h1').text   
        try:
            author = soup.find('span', class_='author').text
        except:
            author = 'no author'
        date = soup.find('span', class_='date').text
        description = soup.find('div', class_='cutline').text
        container = soup.find('div','p', class_='globalCol_1_1')
        content = container.findAll('p')[5].text
        try:
            content2 = container.findAll('p')[6].text
        except:
            content2 = " "
        data = {
            'Name': name,
            'Author': author,
            'Date': date,
            'Description': description,
            'Data': content+content2
        }
    
        print(data)
        datalist.append(data)
        print('Saving:', data['Name'])

df = pd.DataFrame(datalist)
print(df)
# df.to_json(r'C:\Users\Admin\Documents\WORK\project2_env\p2\textbooks.json',orient='columns')
# with open("textbooks.json", "w") as writeJSON:
#    json.dump(datalist, writeJSON, ensure_ascii=False)

# pprint.pprint(data)
def has_src(tag):
    return tag.has_attr('src')