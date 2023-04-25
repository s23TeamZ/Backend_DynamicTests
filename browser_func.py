import os
import logging
import time
import json
from pyvirtualdisplay import Display
from selenium import webdriver
import uuid
import re
import requests
from threading import Thread
from multiprocessing.pool import ThreadPool

# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from browsermobproxy import Server

# logging.getLogger().setLevel(logging.INFO)

# BASE_URL = 'http://www.example.com/'
# BASE_URL = 'https://d3ward.github.io/toolz/adblock.html'
# BASE_URL = 'https://raw.githubusercontent.com/itsfoss/text-files/master/sherlock.txt'
# BASE_URL = 'http://ipv4.download.thinkbroadband.com/50MB.zip'

main_dwn_folder = "downloads_folder"
HEADERS = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}


def chrome_run(BASE_URL: str, dwn_folder):
    
    dwn_folder_path = os.path.join(main_dwn_folder,dwn_folder)
    os.mkdir(dwn_folder_path)
    display = Display(visible=0, size=(1280, 720))
    display.start()
    print('Initialized virtual display..')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("window-size=1280,720")

    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': os.path.join(os.getcwd(), dwn_folder_path),
        'download.prompt_for_download': False,
    })
    print('Prepared chrome options..')
    logs = ['','']
    def func_no_block():
        try:
    browser1 = webdriver.Chrome(options=chrome_options)
    print('Initialized chrome browser 1 ...')
    browser1.get(BASE_URL)
    with open(os.path.join(dwn_folder_path,"no_ad_block.html"), "w", encoding='utf-8') as f:
        f.write(browser1.page_source)
    browser1.close()
        except Exception as e:
            logs[0] = e
    def func_block():
        try:
            chrome_options1 = chrome_options
            chrome_options1.add_extension('./ublock_origin_1_48_0_0.crx')
            browser = webdriver.Chrome(options=chrome_options)
    print('Initialized chrome browser 2 ...')

    browser.get('chrome://extensions/')
    time.sleep(4)
    browser.get(BASE_URL)
    with open(os.path.join(dwn_folder_path,"ad_block.html"), "w", encoding='utf-8') as f:
        f.write(browser.page_source)
            browser.quit()
        except Exception as e:
            logs[1] = e
    # tl = []
    # tl.append(Thread(target=func_block))
    # tl.append(Thread(target=func_no_block))
    # for _t in tl:
    #     _t.start()
    # for _t in tl:
    #     _t.join()
    func_no_block()
    func_block()
    print('Accessed ..', BASE_URL)

    
    display.stop()
    change_p = 0
    try:
        file_diff = os.popen(f"wdiff -s3 {os.path.join(dwn_folder_path,'ad_block.html')} {os.path.join(dwn_folder_path,'no_ad_block.html')} | tail -n 2").read()
        change_p = float(re.findall(r" ([\d\.]+)% changed", file_diff[-25:])[0])
    except:
        pass
    return [True if(logs[0]=='' and logs[1]=='') else False, change_p, logs] 

def check_for_downloads(url):
    file_name = ''
    ret_val = [False, '', 0, '']
    print("[+] Checking for downloads")
    try:
        r = requests.get(url,stream=True, headers=HEADERS)
    except Exception as e:
        return [False, 'NULL', 0, str(e)]
    ret_val[2] = r.headers.get('content-length',0)
    ret_val[1] = r.headers.get('content-type','').lower()
    ret_val[0] = True if(not ('html' in ret_val[1] or 'text' in ret_val[1])) else False
    return ret_val


    print("\ndone!")

def main_browser_func(BASE_URL: str):
    dwn_data = check_for_downloads(url = BASE_URL)
    return_val = {"score": 0 if(dwn_data[0]) else 100*0.25*0.6}
    change_p = 0
    phish_p = 0
    chrome_data = []
    if(not dwn_data[0]):
        dwn_folder = f"{uuid.uuid4().hex[:10].upper()}"
        print(f"Folder Name : {dwn_folder}")
        chrome_data = chrome_run(BASE_URL = BASE_URL, dwn_folder=dwn_folder)
        change_p = chrome_data[1]

    return_val['score'] = return_val['score'] + 0.1*0.6*max(100-(change_p*15),0) + 0.1*0.6*max(100-phish_p,0)
    return_val['dwn_data'] = dwn_data
    return_val['chrome_data'] = chrome_data
    return return_val

# if __name__ == '__main__':
#     chrome_run('https://google.com')


