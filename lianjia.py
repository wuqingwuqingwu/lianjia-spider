
# coding: utf-8

# In[71]:


import urllib.request,re,openpyxl
from bs4 import BeautifulSoup
import pandas as pd




def getUrl():
    urls = []
    for i in range(1,101):
        url = 'http://sh.lianjia.com/ershoufang/xuhui/d%d' % i
        urls.append(url)
    return urls

def getDetail():
    xuhui = {}
    square = []
    room = []
    floor = []
    position = []
    location = []
    road = []
    year = []
    price = []
    unit_price = []
    open_url = []
    for url in getUrl():    
        req = urllib.request.Request(url)
        res = urllib.request.urlopen(req)
        html = (res.read()).decode()
        soup = BeautifulSoup(html, 'html.parser')
        locas = soup.select('.laisuzhou span')
        tag_two = soup.select('.row2-text')
        tag_one = soup.select('.row1-text')
    
        for info_two in tag_two:
            content = info_two.text.replace('\n\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t','').replace('\n\t\t\t\t\t\t\t','').lstrip().rstrip()
            extract_loca =  ''.join(re.findall("(.+?)徐汇", content))
            matching_loca = extract_loca.replace('（）','').replace(' |', '')
            extract_road =  ''.join(re.findall("徐汇 (.+?) ", content))
            matching_road = extract_road.replace('|','')
            extract_year = '\d+年建'
            year.append(''.join(re.findall(extract_year,content)))
            location.append(matching_loca)
            road.append(matching_road)

        for info_one in tag_one:
            content = info_one.text.replace('\n\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t','').replace('\n\t\t\t\t\t\t\t','').lstrip().rstrip()
            #print(content)
            extract_room = '\d+室\d+厅'
            matching_room = ''.join(re.findall(extract_room,content))
            extract_square = '\d+.\d+平'
            matching_square = ''.join(re.findall(extract_square,content))
            extract_floor = '\S+区/\d+层'
            matching_floor = ''.join(re.findall(extract_floor,content))
            extract_position = '朝\S+'
            matching_position = ''.join(re.findall(extract_position,content))
            room.append(matching_room)
            square.append(matching_square)
            floor.append(matching_floor)
            position.append(matching_position)

        for money in soup.select('.total-price'):
            price.append(money.text + '万')
        for unit in soup.select('.minor')[:-1]:
            unit_price.append(unit.text.strip().replace('单价',''))

        for url in soup.select('.prop-title a'):
            open_url.append('http://sh.lianjia.com' + url['href'])
        
        xuhui['url'] = open_url
        xuhui['年份'] = year
        xuhui['位置'] = road
        xuhui['小区名称'] = location
        xuhui['所在楼层'] = floor
        xuhui['建筑面积'] = square
        xuhui['户型'] = room
        xuhui['朝向'] = position
        xuhui['总价'] = price 
        xuhui['单价'] = unit_price 
    return xuhui

columns = ['url', '年份', '位置', '小区名称', '所在楼层',  '建筑面积', '户型', '朝向', '单价', '总价']     
df = pd.DataFrame(getDetail(), columns = columns)
df.to_excel('链家（徐汇）.xlsx')

