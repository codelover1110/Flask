import urllib
from bs4 import BeautifulSoup
import json
import re
from urllib.request import Request
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

import time
import string, random
#crawl_object = dict()
#options = Options()
#options.incognito = True
#options.headless = True
#driver = webdriver.Chrome("./chromedriver", chrome_options=options)
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/80.0.3987.132 Safari/537.36'
#proxy_http_pool = 
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--ignore-certificate-errors')
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f'user-agent={user_agent}')
options.headless = True

#search_result_url = 'https://missingmoney.com/en/Property/Search?searchName={}&page={}'
search_result_url = 'https://missingmoney.com/en/Property/Search?searchName={}'



def sophisticated(data):
    #print("aaa")
    
    real_data = data.split("\\r\\n")[1]
    if "<br />" in real_data:
        
        real_data = real_data.replace("<br />"," ")
    if "<span class=\\\'glyphicon glyphicon-arrow-up\\\'></span>" in real_data:#
        
        real_data = real_data.replace("<span class=\\\'glyphicon glyphicon-arrow-up\\\'></span>"," ")
    if "<span class=\\\'glyphicon glyphicon-arrow-down\\\'></span>" in real_data:
        
        real_data = real_data.replace("<span class=\\\'glyphicon glyphicon-arrow-down\\\'></span>"," ")
    
    
    x = re.search("\w",real_data)
    character_index = x.start()
    #print(real_data[character_index:])
    return real_data[character_index:]
def get_data(url,proxy_url):
    claims_data = list()
    #http_downloader = urllib.request.build_opener(urllib.request.HTTPHandler)
    proxy_handler = urllib.request.ProxyHandler({
            'http': proxy_url,
            'https': proxy_url,
        })

    proxy_downloader = urllib.request.build_opener(proxy_handler)
    proxy_downloader.addheaders = \
            [('User-Agent',
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'),
                ('Content-Type', 'application/json; charset=utf-8')]

    with proxy_downloader.open(url, timeout=50) as response:
        the_page = response.read()

    text = str(the_page)
    row_count = len(text.split("<tr>"))
    index = 0
    for row in text.split("<tr>"):
        tmp_dict = {}
        try:
            if len(row.split("<td")) > 5:
                    index +=1
                    if index == 1: 
                        continue
                    tmp_dict["Name"] = sophisticated(row.split("<td")[2])
                    tmp_dict["Held In"] = sophisticated(row.split("<td")[3])
                    tmp_dict["Last Address"] = sophisticated(row.split("<td")[4])
                    tmp_dict["Reported By"] = sophisticated(row.split("<td")[5])
                    tmp_dict["Amount"] = sophisticated(row.split("<td")[6])
                    claims_data.append(tmp_dict)
        
        except:
            continue
    return claims_data

def crawl_missingmoney(name,index=None):
    property_ids = list()
    proxy_urls = list()
    file_name = name + "_" + str(index)+ "_data.csv"
    #claims_data = list()
    with open("proxy.txt","r") as file:
        random_num = random.randint(1,1000)
        #print(random_num)
        proxyurls = file.readlines()
        proxy_url = proxyurls[random_num]
        print('proxy_url', proxy_url)
        #print('proxy_url', proxy_url)
    proxy_http = "http://" + proxy_url
    webdriver.DesiredCapabilities.CHROME['proxy']={
        "httpProxy":proxy_http,
        "ftpProxy":proxy_http,
        "sslProxy":proxy_http,
    
        "proxyType":"MANUAL",
    }
    driver = webdriver.Chrome(options=options)
    # for i in range(1, 11):
    #url = search_result_url.format(urllib.parse.quote(name),1)
    url = search_result_url.format(urllib.parse.quote(name))
    print (url)

    driver.get(url)

    buttons = driver.find_elements_by_class_name('btn-primary')
    page_btns = driver.find_elements_by_class_name('pagination')

    print (page_btns)
    if len(page_btns) != 0:
        st = page_btns[0].text
        stt = st.split("\n")
        print ("page_btn_text:", st)
        print ("split:", stt)
        if len(stt) > 1:
            print ("page_count:", len(stt) - 1)
        if len(stt) == 1:
            print ("page_count:", 1)            
    else:
        print ("no result!")
        # claims_data = get_data(url,proxy_url)
        # # print(len(buttons))
        # # print(buttons)
        # print("######################",len(claims_data))
        # required_button = []
        # for button in buttons:
        #   # print(button.get_attribute('id'))
        #   if button.get_attribute('id').find('btnClaim') != -1:
        #       required_button.append(button.get_attribute('id'))
        # print("@@@@@@@@@@@@@@@@@@@@@@",len(required_button))
        # cnt = 0
        # for button_id in required_button:
        #   driver.get(url)
        #   cur_button = driver.find_element_by_id(button_id)
        #   cur_button.click()
        #   try:
        #       data = driver.find_element_by_xpath('//*[@id="redirectForm"]/table/tbody/tr[1]/td[2]')
        #   except:
        #       continue
                
        #   property_ids.append(data.text)
        #   if cnt <= len(claims_data) - 1:
        #       claims_data[cnt]["Property ID"] = data.text

        #   cnt += 1

        #   # if cnt > 4:
        #   #   break
        
        # #crawl_object[name] = claims_data
        # for claims in claims_data:
        #   file_exists = os.path.isfile(file_name)
        #   with open(file_name,"a",newline = "") as file:
        #       fieldnames = ["Name","Held In","Last Address","Reported By","Amount","Property ID"]
        #       writer = csv.DictWriter(file,fieldnames = fieldnames)
        #       if not file_exists:
        #           writer.writeheader()
        #       writer.writerow(claims)

if __name__ == "__main__":
    #crawl_missingmoney('ryan druckenmiller')       # 1
    #crawl_missingmoney('david')                    # 10
    crawl_missingmoney('willson piter')             # 0
    #crawl_missingmoney('ryan dru')                  # 5