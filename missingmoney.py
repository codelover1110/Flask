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
import threading
import time
import string, random
# crawl_object = dict()

# user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) ' \
#              'Chrome/80.0.3987.132 Safari/537.36'

# options = webdriver.ChromeOptions()
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--ignore-certificate-errors')
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument(f'user-agent={user_agent}')
# options.headless = True

# search_result_url = 'https://missingmoney.com/en/Property/Search?searchName={}&page={}'


# def sophisticated(data):
#     real_data = data.split("\\r\\n")[1]
#     if "<br />" in real_data:
        
#         real_data = real_data.replace("<br />"," ")
#     if "<span class=\\\'glyphicon glyphicon-arrow-up\\\'></span>" in real_data:#
        
#         real_data = real_data.replace("<span class=\\\'glyphicon glyphicon-arrow-up\\\'></span>"," ")
#     if "<span class=\\\'glyphicon glyphicon-arrow-down\\\'></span>" in real_data:
        
#         real_data = real_data.replace("<span class=\\\'glyphicon glyphicon-arrow-down\\\'></span>"," ")
    
    
#     x = re.search("\w",real_data)
#     character_index = x.start()
#     #print(real_data[character_index:])
#     return real_data[character_index:]
# def get_data(url,proxy_url):
#   claims_data = list()
#   #http_downloader = urllib.request.build_opener(urllib.request.HTTPHandler)
#   proxy_handler = urllib.request.ProxyHandler({
#             'http': proxy_url,
#             'https': proxy_url,
#         })

#   proxy_downloader = urllib.request.build_opener(proxy_handler)
#   proxy_downloader.addheaders = \
#             [('User-Agent',
#                 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'),
#                 ('Content-Type', 'application/json; charset=utf-8')]

#   with proxy_downloader.open(url, timeout=50) as response:
#       the_page = response.read()

#   text = str(the_page)
#   row_count = len(text.split("<tr>"))
#   index = 0
#   for row in text.split("<tr>"):
#       tmp_dict = {}
#       try:
#           if len(row.split("<td")) > 5:
#                   index +=1
#                   if index == 1: 
#                       continue
#                   tmp_dict["Name"] = sophisticated(row.split("<td")[2])
#                   tmp_dict["Held In"] = sophisticated(row.split("<td")[3])
#                   tmp_dict["Last Address"] = sophisticated(row.split("<td")[4])
#                   tmp_dict["Reported By"] = sophisticated(row.split("<td")[5])
#                   tmp_dict["Amount"] = sophisticated(row.split("<td")[6])
#                   claims_data.append(tmp_dict)
        
#       except:
#           continue
#   return claims_data

# def crawl_missingmoney(name): 
#   property_ids = list()
#   proxy_urls = list()
#   file_name = name + "_data.csv"
#   with open("proxy.txt","r") as file:
#       random_num = random.randint(1,1000)
#       proxyurls = file.readlines()
#       proxy_url = proxyurls[random_num]
#       print('proxy_url', proxy_url)
#         #print('proxy_url', proxy_url)
#   proxy_http = "http://" + proxy_url
#   webdriver.DesiredCapabilities.CHROME['proxy']={
#       "httpProxy":proxy_http,
#       "ftpProxy":proxy_http,
#       "sslProxy":proxy_http,
    
#       "proxyType":"MANUAL",
#     }
#   print ("**************")
#   driver = webdriver.Chrome(options=options)
#   #driver.set_page_load_timeout(10)
#   for i in range(1, 11):
#       start_time = time.time()
#       print ("22222222222222222222----", i, "\t\t", str(time.time() - start_time))
#       url = search_result_url.format(urllib.parse.quote(name),i)

#       driver.get(url)
#       print ("\t33333333333333333333----", i, "\t", str(time.time() - start_time))
#       buttons = driver.find_elements_by_class_name('btn-primary')
#       claims_data = get_data(url,proxy_url)
#       print ("\t44444444444444444444----", i, "\t", str(time.time() - start_time))
#       # print(len(buttons))
#       # print(buttons)
#       #print("######################",len(claims_data))
#       required_button = []
#       for button in buttons:
#           # print(button.get_attribute('id'))
#           if button.get_attribute('id').find('btnClaim') != -1:
#               required_button.append(button.get_attribute('id'))
#       #print("@@@@@@@@@@@@@@@@@@@@@@",len(required_button))
#       cnt = 0
#       for button_id in required_button:
#           driver.get(url)
#           cur_button = driver.find_element_by_id(button_id)
#           cur_button.click()
#           try:
#               data = driver.find_element_by_xpath('//*[@id="redirectForm"]/table/tbody/tr[1]/td[2]')
#           except:
#               continue

#           property_ids.append(data.text)
#           claims_data[cnt]["Property ID"] = data.text
#           cnt += 1

#       print ("\t55555555555555555555----", i, "\t", str(time.time() - start_time))

            # if cnt > 4:
            #   break
        
#       crawl_object[name] = claims_data
#       for claims in claims_data:
#           file_exists = os.path.isfile(file_name)
#           with open(file_name,"a",newline = "") as file:
#               fieldnames = ["Name","Held In","Last Address","Reported By","Amount","Property ID"]
#               writer = csv.DictWriter(file,fieldnames = fieldnames)
#               if not file_exists:
#                   writer.writeheader()
#               writer.writerow(claims)

# ***************************************************************************************************************

try:
   import queue
except ImportError:
   import Queue as queue

from dataclasses import dataclass
@dataclass 
class JDefine:
    # crawl thread states
    CRAWL_STATE_NOTHING_DOING        = 1
    CRAWL_STATE_NOW_DOING            = 2
    CRAWL_STATE_DONE_ERROR_NONE      = 3
    CRAWL_STATE_DONE_ERROR_TIME_OVER = 4
    CRAWL_STATE_DONE_ERROR_OTHER     = 5

    # url search states
    PAGE_PROC_NOT_DONE              = 11
    PAGE_PROC_NOW_DOING             = 12
    PAGE_PROC_DONE_OK               = 13
    PAGE_PROC_DONE_ERROR            = 14
    NO_SEARCH_RESULT                = 15

    GET_PROXY_LIST_DONE             = 21 
    GET_PROXY_LIST_ERROR            = 22

    THREAD_TIME_LIMIT               = 40  # stop thread if Crawl time is over than 20 seconds
    CLIENT_NO_SEARCH_TIME_OUT       = 60 # after 300 seconds without any search, delete CrawlThreadManager

class CrawlThread(object):
    def __init__(self, url, key, param_state=None, proxy_ip=None, page_num=None):
        self.url = url                  # url address
        self.key = key                  # search key
        self.param_state = param_state
        self.state = JDefine.CRAWL_STATE_NOTHING_DOING        # thread state
        self.start_time = None          # thread processing start time
        self.chrome_opt = None          
        self.proxy = proxy_ip           # proxy_ip
        self.page_num = page_num
        self.claim_queue = queue.Queue() # dict with key: ["Name", "Held In", "Last Address", "Reported By", "Amount", "Property ID"]
        self.res = None                 # list format result
        self.working_allow = False      # allow thread to process

        self.set_chrome_option()
        self.thread = threading.Thread(target=self.crawl_thread_func)

    def set_chrome_option(self):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/80.0.3987.132 Safari/537.36'

        chrome_opt = webdriver.ChromeOptions()
        chrome_opt.add_argument('--no-sandbox')
        chrome_opt.add_argument('--disable-dev-shm-usage')
        chrome_opt.add_argument('--ignore-certificate-errors')
        chrome_opt.add_argument("--disable-blink-features=AutomationControlled")
        chrome_opt.add_argument(f'user-agent={user_agent}')
        chrome_opt.headless = True

        self.chrome_opt = chrome_opt

    def start(self):
        self.start_time = time.time()
        if not self.thread.is_alive():
            self.thread.start()
        self.state = JDefine.CRAWL_STATE_NOW_DOING

    def stop(self):
        self.thread.join()

    def restart(self, url, key, param_state, proxy, page_num):
        self.url = url
        self.key = key
        self.param_state = param_state
        self.proxy = proxy
        self.page_num
        self.result = None
        self.res = None
        self.start_time = None
        self.start()

    def get_thread_state(self):
        return self.state

    def get_page_number(self):
        return self.page_num

    def get_result(self):
        data = None
        if not self.claim_queue.empty():
            tmp = self.claim_queue.get()
            if tmp['property_id'] != "":
                data = tmp
        thread_state = self.state
        if self.state == JDefine.CRAWL_STATE_DONE_ERROR_NONE or self.state == JDefine.CRAWL_STATE_DONE_ERROR_OTHER:
            self.state = JDefine.CRAWL_STATE_NOTHING_DOING
        return self.page_num, data, thread_state

    def get_btn_ids(self, buttons, tag):
        btn_ids = []
        for button in buttons:
            if button.get_attribute('id').find(tag) != -1:
                btn_ids.append(button.get_attribute('id'))
        return btn_ids

    def sophisticated(self, data):
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

    def get_claim_data_without_property_id(self, url,proxy_url):
        claims_data = list()
        #http_downloader = urllib.request.build_opener(urllib.request.HTTPHandler)
        proxy_ip = proxy_url
        try: 
            proxy_handler = urllib.request.ProxyHandler({
                'http': proxy_ip,
                'https': proxy_ip,
            })
            proxy_downloader = urllib.request.build_opener(proxy_handler)
            proxy_downloader.addheaders = \
                    [('User-Agent',
                        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'),
                        ('Content-Type', 'application/json; charset=utf-8')]           
            with proxy_downloader.open(url, timeout=40) as response:
                the_page = response.read()
        except:
            print ("using proxy failed!==================================", self.page_num)
            return []
                
        text = str(the_page)
        row_count = len(text.split("<tr>"))
        index = 0
        for row in text.split("<tr>"):
            tmp_dict = dict.fromkeys(['name', 'held_in', 'last_addr', 'property_id','reported_by', 'amount'])
            try:
                if len(row.split("<td")) > 5:
                    index +=1
                    if index == 1:
                        continue
                    tmp_dict['name'] = self.sophisticated(row.split("<td")[2])
                    tmp_dict['held_in'] = self.sophisticated(row.split("<td")[3])
                    tmp_dict['last_addr'] = self.sophisticated(row.split("<td")[4])
                    tmp_dict['reported_by'] = self.sophisticated(row.split("<td")[5])
                    tmp_dict['amount'] = self.sophisticated(row.split("<td")[6])
                    tmp_dict['property_id'] = ""
                    #self.claim_queue.put(tmp_dict)
                    claims_data.append(tmp_dict)

            except:
                continue
           

        return claims_data

    def crawl_thread_func(self):
        print ("start_thread::::::::::::::::::::::")
        while True:
            if self.state != JDefine.CRAWL_STATE_NOW_DOING:
                time.sleep(0.1)
                continue 
            proxy_http = "http://" + self.proxy
            webdriver.DesiredCapabilities.CHROME['proxy']={
                "httpProxy":proxy_http,
                "ftpProxy":proxy_http,
                "sslProxy":proxy_http,
                "proxyType":"MANUAL",
            }

            with webdriver.Chrome(options=self.chrome_opt) as driver:
                if self.param_state == None:
                    url = self.url.format(urllib.parse.quote(self.key), self.page_num)
                else:
                    url = self.url.format(urllib.parse.quote(self.key), self.param_state, self.page_num)
                driver.get(url)
                buttons = driver.find_elements_by_class_name('btn-primary')
                # get button ids named as 'btnClaim' on current page
                required_button = self.get_btn_ids(buttons, 'btnClaim')

                claim_data = self.get_claim_data_without_property_id(url, self.proxy)

                if len(claim_data) == 0:
                    self.state = JDefine.CRAWL_STATE_DONE_ERROR_OTHER
                    continue

                #print (claim_data)
                idx = 0
                # fill the property id to claim_data
                for btn in required_button:
                    driver.get(url)
                    try:
                        cur_button = driver.find_element_by_id(btn)
                        cur_button.click()
                    except:
                        print ("button click failed!=========================", self.page_num, idx, btn, cur_button)

                    try:
                        data = driver.find_element_by_xpath('//*[@id="redirectForm"]/table/tbody/tr[1]/td[2]')
                        if idx >= len(claim_data):
                            continue
                        claim_data[idx]['property_id'] = data.text
                        print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",idx, "\t", len(claim_data), "\t", len(required_button))                        
                        self.claim_queue.put(claim_data[idx])
                    except:
                        print ("get data failed!==========================", self.page_num, idx)
                    idx += 1
                
                self.state = JDefine.CRAWL_STATE_DONE_ERROR_NONE



                
class CrawlThreadManager(object):
    def __init__(self, thread_cnt):
        self.thread_cnt = thread_cnt
        self.search_key = None
        self.url = None
        self.para_state = None
        self.page_proc_info = []                # list of dict: (page_num, state, act_cnt)
        self.page_cnt = None
        self.thread_list = []                   #list of class : CrawlThread
        self.proxy_list = None                  # list of proxy ip-> ex:192.168.11.112:3380
        self.start_time = None                  # search start time
        self.search_state = False               # True, False
        self.result_queue = queue.Queue()       # dict (page_num, data)

        self.manage_thread = threading.Thread(target=self.manage_thread_func)

    def __del__(self):
        print ("deleted!")

    def fetch_page_count(self, url, key, state=None):
        page_cnt = 0

        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/80.0.3987.132 Safari/537.36'

        chrome_opt = webdriver.ChromeOptions()
        chrome_opt.add_argument('--no-sandbox')
        chrome_opt.add_argument('--disable-dev-shm-usage')
        chrome_opt.add_argument('--ignore-certificate-errors')
        chrome_opt.add_argument("--disable-blink-features=AutomationControlled")
        chrome_opt.add_argument(f'user-agent={user_agent}')
        chrome_opt.headless = True

        proxy_url = self.get_proxy_ip()
        proxy_http = "http://" + proxy_url

        webdriver.DesiredCapabilities.CHROME['proxy']={
            "httpProxy":proxy_http,
            "ftpProxy":proxy_http,
            "sslProxy":proxy_http,
        
            "proxyType":"MANUAL",
        }
        try:
            driver = webdriver.Chrome(options=chrome_opt)
            if self.param_state == None:
                url_str = url.format(urllib.parse.quote(key), 1)
            else:
                url_str = url.format(urllib.parse.quote(key), state, 1)
            driver.get(url_str)

            page_btns = driver.find_elements_by_class_name('pagination')
            
            if len(page_btns) != 0:
                st = page_btns[0].text
                stt = st.split("\n")
                page_cnt = len(stt)-1
        except:
            print ("get page count failed!")

        return page_cnt  

    def set_param(self, url, search_key, param_state=None, proxy_list_path=None):
        self.page_proc_info.clear()
        self.result_queue.queue.clear()
        self.url = url
        self.search_key = search_key
        self.param_state = param_state        
        self.start_time = None
        if self.get_proxy_list() == False:
            return JDefine.GET_PROXY_LIST_ERROR


        self.page_cnt = 10
        # self.page_cnt = self.fetch_page_count(self.url, self.search_key, self.param_state)
        # if self.page_cnt == 0:
        #     return JDefine.NO_SEARCH_RESULT

        for page_num in range(self.page_cnt):
            item = dict.fromkeys(['page_num', 'state', 'act_cnt'])
            item['page_num'] = page_num + 1
            item['state'] = JDefine.PAGE_PROC_NOT_DONE
            item['act_cnt'] = 0

            self.page_proc_info.append(item)
        return JDefine.GET_PROXY_LIST_DONE#, len(self.proxy_list)

    def get_proxy_list(self, proxy_list_path=None):
        path = ""
        if proxy_list_path != None:
            path = proxy_list_path
        else:
            path = "proxy.txt"
        with open(path,"r") as file:
            self.proxy_list = file.readlines()    
            return True

        return False

    def get_ctm_state(self):
        return self.search_state 

    def get_queue_data(self):
        value_data = []
        if not self.result_queue.empty():
            while not self.result_queue.empty():
                item = self.result_queue.get()
                data = item['data']
                tmp = []
                for key,value in data.items():
                    tmp.append(value)
                value_data.append(tmp)
            print ("____________________________data len:", len(value_data))
            return value_data
        else:
            return []


    def start(self):
        self.start_time = time.time()
        if len(self.thread_list) == 0:
            for i in range(self.thread_cnt):
                proxy_ip, page_num = self.get_next_proxy_and_page()
                if page_num is None:
                    break
                crl_thread = CrawlThread(url=self.url, key=self.search_key, param_state=self.param_state,
                                            proxy_ip=proxy_ip, page_num=page_num)
                self.thread_list.append(crl_thread)
            for thrd in self.thread_list:
                thrd.start()

            self.manage_thread.start()

        self.search_state = True

    def end_manager(self):
        for thread in self.thread_list:
            thread.stop()

        self.manage_thread.join()
            
    def get_next_proxy_and_page(self):
        random_idx = random.randint(1,len(self.proxy_list)-1)
        proxy_ip = self.proxy_list[random_idx]
        for page_info in self.page_proc_info:
            if page_info['state'] == JDefine.PAGE_PROC_NOT_DONE:
                page_info['state'] = JDefine.PAGE_PROC_NOW_DOING
                return proxy_ip, page_info['page_num']
        return None, None

    def get_proxy_ip(self):
        random_idx = random.randint(1,len(self.proxy_list)-1)
        proxy_ip = self.proxy_list[random_idx]
        return proxy_ip

    def proc_url_result(self, page_num, data, thread_state):
        if data is not None:
            print ("--------------------------------------------------put data:", page_num)
            res = dict.fromkeys(['page_num', 'data'])
            res['page_num'] = page_num
            res['data'] = data
            self.result_queue.put(res)

        if thread_state == JDefine.CRAWL_STATE_NOTHING_DOING:
            return

        if thread_state == JDefine.CRAWL_STATE_DONE_ERROR_NONE:
            print ("DONE! Page Number: ", page_num)
            self.update_page_state(page_num, JDefine.PAGE_PROC_DONE_OK)
        
        if thread_state == JDefine.CRAWL_STATE_DONE_ERROR_OTHER:
            print ("DONE PROXY ERROR! Page Number: ", page_num)
            self.update_page_state(page_num, JDefine.PAGE_PROC_DONE_ERROR)
            pass

        if thread_state == JDefine.CRAWL_STATE_DONE_ERROR_TIME_OVER:
            pass

    def update_page_state(self, page_num, state):
        for page_info in self.page_proc_info:
            if page_info['page_num'] == page_num:
                page_info['state'] = state
                return

    def check_threads(self):     # check if all threads are not working, 
        for thread in self.thread_list:
            state = thread.get_thread_state()
            if state != JDefine.CRAWL_STATE_NOTHING_DOING:
                return False
        return True

    def manage_thread_func(self):
        no_next_page = False
        while True:
            if no_next_page == True and self.search_state == False:
                #print ("total_time:", time.time() - self.start_time)
                print ("no more page:" )
                time.sleep(2)
                continue

            for thread in self.thread_list:
                page_num, data, thread_state = thread.get_result()
                # # if proxy error then thread restart with other proxy ip
                # if thread_state == JDefine.CRAWL_STATE_DONE_ERROR_OTHER:
                #     proxy = self.get_proxy_ip()
                #     page_num = thread.get_page_number()
                #     time.sleep(3)
                #     thread.restart(self.url, self.search_key, self.param_state, proxy, page_num)
                #     print ("restart crawl thread with other proxy!===============", proxy, "\t", page_num)
                # else:
                self.proc_url_result(page_num, data, thread_state)

                if thread_state != JDefine.CRAWL_STATE_NOW_DOING:
                    proxy, next_page = self.get_next_proxy_and_page()
                    if next_page is not None:
                        thread.restart(self.url, self.search_key, self.param_state, proxy, next_page)
                    else:
                        no_next_page = True

            
            if no_next_page == True:
                tmp = False
                for thread in self.thread_list:
                    state = thread.get_thread_state()
                    if state == JDefine.CRAWL_STATE_NOW_DOING:
                        tmp = True
                        print ("tmppppppppppppppppppppppp", thread.get_page_number())
                        break

                if tmp == False:
                    self.search_state = False

            time.sleep(0.5)

        return


class CrawlSearchManager(object):
    def __init__(self):
        self.ctm_list = []          # list of dict: (client_key, ctm(CrawlThreadManager), last_act_time)
        self.ctm_check_thread = threading.Thread(target=self.ctm_check_thread_func)
        self.ctm_check_thread.start()

    def append_search(self, client_key, ctm):
        ctm_item = dict.fromkeys(['client_key', 'ctm', 'last_act_time'])
        ctm_item['client_key'] = client_key
        ctm_item['ctm'] = ctm
        ctm_item['last_act_time'] = time.time()

        self.ctm_list.append(ctm_item)
        return len(self.ctm_list)

    def get_crwal_data(self, client_key):
        # return ctm data
        for ctm_item in self.ctm_list:
            if ctm_item['client_key'] == client_key:
                data = ctm_item['ctm'].get_queue_data()
                state = ctm_item['ctm'].get_ctm_state()
                if state:
                    ctm_item['last_act_time'] = time.time()
                return True, state, data

        return False, None, None

    def get_search_count(self):
        return len(self.ctm_list)
    
    def ctm_check_thread_func(self):
        while True:
            if len(self.ctm_list) == 0:
                time.sleep(10)
                continue
            for i, ctm_item in enumerate(self.ctm_list):
                if time.time() - ctm_item['last_act_time'] > JDefine.CLIENT_NO_SEARCH_TIME_OUT: # 300 seconds
                    del self.ctm_list[i]

            time.sleep(5)



def set_url_key_state(lname,  fname, state):
    search_key = ''
    url = ''
    f_state = None
    if fname == "" and state == "":
        search_key = lname
        url = 'https://missingmoney.com/en/Property/Search?searchName={}&page={}'
        ##url.format(l)
    elif fname == "" and state != "":
        search_key = lname
        url = 'https://missingmoney.com/en/Property/Search?searchName={}&State={}&page={}'
        f_state = state
    elif fname != "" and state != "":
        search_key = lname + " " + fname
        url = 'https://missingmoney.com/en/Property/Search?searchName={}&State={}&page={}'
        f_state = state
    elif fname != "" and state == "":
        search_key = lname + " " + fname
        url = 'https://missingmoney.com/en/Property/Search?searchName={}&page={}'

    return url, search_key, state

                
if __name__ == "__main__":
    # ********************************Test for CrawlSearchManager *******************************
    if True:
        csm = CrawlSearchManager()
        max_thread_cnt = 2
        key = "David"
        url = 'https://missingmoney.com/en/Property/Search?searchName={}&page={}'
        ctm1 = CrawlThreadManager(max_thread_cnt)         

        client_key1 = str(time.time())   
        if ctm1.set_param(url, key) == JDefine.NO_SEARCH_RESULT:
            print ("no result for: ", key)
        ctm1.start()

        csm.append_search(client_key1, ctm1)
        search_cnt1 = 0

        time.sleep(20)

        #  second search----------------------------------------------
        key = "ryan dru"
        url = 'https://missingmoney.com/en/Property/Search?searchName={}&page={}'

        client_key2 = str(time.time())
        ctm2 = CrawlThreadManager(max_thread_cnt)
        if ctm2.set_param(url, key) == JDefine.NO_SEARCH_RESULT:
            print ("no result for: ", key)
        ctm2.start()

        csm.append_search(client_key2, ctm2)
        search_cnt2 = 0
        t = time.time()
        secs = 0
        while True:
            if csm.get_search_count() == 0:
                print ("no any search engine!", search_cnt1, "\t", search_cnt2)
                print ("total seconds: ", secs)
                time.sleep(1)
                continue    

            ret1, state1, data1 = csm.get_crwal_data(client_key1)
            if ret1:
                if state1 == False and len(data1) == 0:
                    if secs == 0:
                        secs = time.time() - t
                    print ("result count1 = ", search_cnt1)
                    print ("search engine_count = ", csm.get_search_count())

                else:
                    if len(data1) != 0:
                        search_cnt1 += len(data1)
                        print ("\n\n search_1 \n\n")
            else:
                print("no no no no no search engine__________111111111111111", csm.get_search_count())

            ret2, state2, data2 = csm.get_crwal_data(client_key2)
            if ret2:
                if state2 == False and len(data2) == 0:
                    print ("result count2 = ", search_cnt2)
                    print ("search engine_count = ", csm.get_search_count())
                    if secs == 0:
                        secs = time.time() - t
                else:
                    if len(data2) != 0:
                        search_cnt2 += len(data2)
                        print ("\n\n search_2 \n\n")
            else:
                print ("no no no no no search engine_________22222222222222222")

            time.sleep(1)





    # *********************************** Test for CrawThreadManager *********************************
    if False:
        ctm = CrawlThreadManager(10)
        ret = JDefine.GET_PROXY_LIST_ERROR

        if True:
            #key = "ryan druckenmiller"
            key = "Hyare"
            url = 'https://missingmoney.com/en/Property/Search?searchName={}&page={}'    
            ret = ctm.set_param(url, key)
        else:
            fname = "Anne"
            lname = "David"
            status = "alabama"

            url, key, status = set_url_key_state(lname, fname, status)
            ret = ctm.set_param(url=url, search_key=key, param_state=status)

        if ret == JDefine.GET_PROXY_LIST_ERROR:
            print("No Proxy!")
        else:
            ctm.start()
            search_cnt = 0
            while True:
                data = ctm.get_queue_data()
                if ctm.get_ctm_state() == False and len(data) == 0:
                    print ("search end!")
                    print ("result count = ", search_cnt)
                else:
                    if len(data) != 0:
                        search_cnt += len(data)
                        print ("\n\n\n")
                        print (data)
                        print ("\n\n\n")

                time.sleep(1)

        # time.sleep(10)
        # key = "David"
        # ctm.set_param(url, key)
        # ctm.start()
        # while True:
        #     if ctm.get_ctm_state() == False:
        #         print ("second search end!")
        #         break




#******************************* Test for CrawlThread  ****************************************
    if False:
        with open("proxy.txt","r") as file:
            random_num = random.randint(1,1000)
            proxyurls = file.readlines()    
            proxy_ip = proxyurls[random_num]    
        print (proxy_ip)
        page_num = 1
        t = CrawlThread(url, key, proxy_ip, page_num)
        t.start()
        while True:
            data, state = t.get_result()
            if state == JDefine.CRAWL_STATE_DONE_ERROR_NONE:
                break
            elif data is not None:
                print ("*************************************************")
                print (data)
            time.sleep(0.1)

        print ("\n\n END ")


    # x = threading.Thread(target=crawl_missingmoney, args=(key,))
    # x.start()