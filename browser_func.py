import os
import logging
import time
import json
from pyvirtualdisplay import Display
from selenium import webdriver
import uuid

# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from browsermobproxy import Server

# logging.getLogger().setLevel(logging.INFO)

# BASE_URL = 'http://www.example.com/'
# BASE_URL = 'https://d3ward.github.io/toolz/adblock.html'
# BASE_URL = 'https://raw.githubusercontent.com/itsfoss/text-files/master/sherlock.txt'
# BASE_URL = 'http://ipv4.download.thinkbroadband.com/50MB.zip'

main_dwn_folder = "downloads_folder"

def chrome_run(BASE_URL: str):
    dwn_folder = f"{uuid.uuid4().hex[:10].upper()}"
    print(f"Folder Name : {dwn_folder}")
    dwn_folder_path = os.path.join(main_dwn_folder,dwn_folder)
    os.mkdir(dwn_folder_path)
    display = Display(visible=0, size=(1280, 720))
    display.start()
    print('Initialized virtual display..')

    # server = Server("~/browsermob-proxy-2.1.4/bin/browsermob-proxy")
    # server = Server("browsermob-proxy-2.1.4/bin/browsermob-proxy")
    # server.start()
    # proxy = server.create_proxy()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("window-size=1280,720")
    # chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))

    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': os.path.join(os.getcwd(), dwn_folder_path),
        'download.prompt_for_download': False,
    })
    print('Prepared chrome options..')
    browser1 = webdriver.Chrome(options=chrome_options)
    print('Initialized chrome browser 1 ...')
    browser1.get(BASE_URL)
    with open(os.path.join(dwn_folder_path,"no_ad_block.html"), "w", encoding='utf-8') as f:
        f.write(browser1.page_source)
    browser1.close()

    chrome_options.add_extension('./ublock_origin_1_48_0_0.crx')

    # caps = DesiredCapabilities.CHROME
    # caps['goog:loggingPrefs'] = {'performance': 'ALL'}
    browser = webdriver.Chrome(options=chrome_options)#, desired_capabilities=caps)
    print('Initialized chrome browser 2 ...')

    browser.get('chrome://extensions/')
    time.sleep(4)
    browser.get(BASE_URL)
    with open(os.path.join(dwn_folder_path,"ad_block.html"), "w", encoding='utf-8') as f:
        f.write(browser.page_source)

    # perf = browser.get_log('performance')
    # with open(os.path.join(dwn_folder_path,"o_nw.json"), "w", encoding='utf-8') as f:
    #     json.dump(perf, f, indent=4)

    # proxy.new_har("myhar")
    # with open(os.path.join(dwn_folder_path,'myhar.har'), 'w') as har_file:
    #     json.dump(proxy.har, har_file)
    print('Accessed %s ..', BASE_URL)
    wait_for_downloads()

    print('Page title: %s', browser.title)
    # p = input()
    browser.quit()
    display.stop()
    return dwn_folder_path

def wait_for_downloads():
    file_name = ''
    print("Waiting for downloads", end = '')
    while any([filename.endswith(".crdownload") for filename in 
               os.listdir("downloads_folder")]):
        print("...", end = '')
        time.sleep(2)

    print("\ndone!")

def main_browser_func(BASE_URL: str):
    dwn_folder_path = chrome_run(BASE_URL= BASE_URL)
    return_val = {}
    return_val['File_Diff'] = os.popen(f"wdiff -s3 {os.path.join(dwn_folder_path,'no_ad_block.html')} {os.path.join(dwn_folder_path,'ad_block.html')} | tail -n 2").read()
    files_l = os.listdir(dwn_folder_path) 
    if(len(files_l)>2):
        return_val['File_Down_bool'] = True
        files_l.remove('no_ad_block.html')
        files_l.remove('ad_block.html')
        return_val['Files_Dwn'] = files_l
    return return_val

if __name__ == '__main__':
    chrome_run('https://google.com')


