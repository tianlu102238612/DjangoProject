"""
Created on Wed Jul  8 19:58:04 2020

@author: tianlu
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Chrome

import time,json,random,requests,re
import pandas

driver = webdriver.Chrome(ChromeDriverManager().install())

user = "1078801674@qq.com"
password = "e07880e674"
gzlist=['牛娃成长记']

def weChat_login():
    post = {}
    options = Options()
    options.add_argument('-headless')

    
    driver.get('https://mp.weixin.qq.com/')
    
    
    driver.find_element_by_xpath('//*[@id="header"]/div[2]/div/div/div[2]/a').click()
    driver.find_element_by_xpath('//*[@id="header"]/div[2]/div/div/div[1]/form/div[1]/div[1]/div/span/input').clear()
    driver.find_element_by_xpath('//*[@id="header"]/div[2]/div/div/div[1]/form/div[1]/div[1]/div/span/input').send_keys(user)
    driver.find_element_by_xpath('//*[@id="header"]/div[2]/div/div/div[1]/form/div[1]/div[2]/div/span/input').clear()
    driver.find_element_by_xpath('//*[@id="header"]/div[2]/div/div/div[1]/form/div[1]/div[2]/div/span/input').send_keys(password)
    
    
    #remeber password
    driver.find_element_by_xpath('//*[@id="header"]/div[2]/div/div/div[1]/form/div[3]/label').click()
    print("记住账号")
    
    #login
    driver.find_element_by_xpath('//*[@id="header"]/div[2]/div/div/div[1]/form/div[4]/a').click()
    
    #暂停扫码登陆
    time.sleep(10)
    print("登录成功")
    
    #重新载入公众号登录页，登录之后会显示公众号后台首页，从这个返回内容中获取cookies信息
    driver.get('https://mp.weixin.qq.com/')
    #获取cookies
    cookie_items = driver.get_cookies()
    #获取到的cookies是列表形式，将cookies转成json形式并存入本地名为cookie的文本中
    for cookie_item in cookie_items:
        post[cookie_item['name']] = cookie_item['value']
    cookie_str = json.dumps(post)
    with open('cookie.txt', 'w+', encoding='utf-8') as f:
        f.write(cookie_str)
    print("cookies信息已保存到本地")
    
    
def get_content(query):
    #query为要爬取的公众号名称
    #公众号主页
    url = 'https://mp.weixin.qq.com'
    #设置headers
    header = {
        "HOST": "mp.weixin.qq.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
        }
    #读取上一步获取到的cookies
    with open('cookie.txt', 'r', encoding='utf-8') as f:
        cookie = f.read()
    cookies = json.loads(cookie)
    print(cookies)
    #登录之后的微信公众号首页url变化为：https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=1849751598，从这里获取token信息
    response = requests.get(url=url, cookies=cookies)
    print(response)
    token = re.findall(r'token=(\d+)', str(response.url))[0]
    print(token)
    #搜索微信公众号的接口地址
    search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
    #搜索微信公众号接口需要传入的参数，有三个变量：微信公众号token、随机数random、搜索的微信公众号名字
    query_id = {
        'action': 'search_biz',
        'token' : token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'query': query,
        'begin': '0',
        'count': '5'
        }
    #打开搜索微信公众号接口地址，需要传入相关参数信息如：cookies、params、headers
    search_response = requests.get(search_url, cookies=cookies, headers=header, params=query_id)
    #取搜索结果中的第一个公众号
    lists = search_response.json().get('list')[0]
    #获取这个公众号的fakeid，后面爬取公众号文章需要此字段
    fakeid = lists.get('fakeid')
    #微信公众号文章接口地址
    appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
    #搜索文章需要传入几个参数：登录的公众号token、要爬取文章的公众号fakeid、随机数random
    query_id_data = {
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'action': 'list_ex',
        'begin': '0',#不同页，此参数变化，变化规则为每页加5
        'count': '5',
        'query': '',
        'fakeid': fakeid,
        'type': '9'
        }
    #打开搜索的微信公众号文章列表页
    appmsg_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
    #获取文章总数
    max_num = appmsg_response.json().get('app_msg_cnt')
    print(max_num)
    #每页至少有5条，获取文章总的页数，爬取时需要分页爬
    num = int(int(max_num) / 5)
    #起始页begin参数，往后每页加5
    begin = 0
    while num + 1 > 0 :
        query_id_data = {
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'action': 'list_ex',
            'begin': '{}'.format(str(begin)),
            'count': '5',
            'query': '',
            'fakeid': fakeid,
            'type': '9'
            }
        print('正在翻页：--------------',begin)
        #获取每一页文章的标题和链接地址，并写入本地文本中
        query_fakeid_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
        fakeid_list = query_fakeid_response.json().get('app_msg_list')
        
        df = pandas.DataFrame(columns=('Title','Link'))
        
        for item in fakeid_list:
            title = item.get('title')
            link = item.get('link')
            df = df.append({'Title':title,'Link':link},ignore_index=True)
          
            fileName=query+'.csv'
            
        num -= 1
        begin = int(begin)
        begin+=5
        time.sleep(2)
        df.to_csv(fileName,mode='a',index=False)

if __name__=='__main__':
    try:
        #登录微信公众号，获取登录之后的cookies信息，并保存到本地文本中
        weChat_login()
        #登录之后，通过微信公众号后台提供的微信公众号文章接口爬取文章
        for query in gzlist:
            #爬取微信公众号文章，并存在本地文本中
            print("开始爬取公众号："+query)
            get_content(query)
            print("爬取完成")
    except Exception as e:
        print(str(e))
    
    

