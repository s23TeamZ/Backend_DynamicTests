import os
import logging
import time
import json
from pyvirtualdisplay import Display
from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from browsermobproxy import Server

logging.getLogger().setLevel(logging.INFO)

# BASE_URL = 'http://www.example.com/'
BASE_URL = 'https://d3ward.github.io/toolz/adblock.html'
BASE_URL = 'https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-2.1.4/browsermob-proxy-2.1.4-bin.zip'


def chrome_example():
    display = Display(visible=1, size=(1280, 720))
    display.start()
    logging.info('Initialized virtual display..')

    # server = Server("~/browsermob-proxy-2.1.4/bin/browsermob-proxy")
    # server = Server("browsermob-proxy-2.1.4/bin/browsermob-proxy")
    # server.start()
    # proxy = server.create_proxy()

    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--no-sandbox')
    chrome_options.add_extension('./ublock_origin_1_48_0_0.crx')
    chrome_options.add_argument("window-size=1280,720")
    # chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))

    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': os.path.join(os.getcwd(), 'downloads_folder'),
        'download.prompt_for_download': False,
    })
    logging.info('Prepared chrome options..')
    # browser1 = webdriver.Chrome(options=chrome_options)
    # logging.info('Initialized chrome browser 1..')
    # browser1.get(BASE_URL)
    # with open(os.path.join("downloads_folder","no_ad_block.html"), "w", encoding='utf-8') as f:
    #     f.write(browser1.page_source)
    # browser1.close()

    # caps = DesiredCapabilities.CHROME
    # caps['goog:loggingPrefs'] = {'performance': 'ALL'}
    browser = webdriver.Chrome(options=chrome_options)#, desired_capabilities=caps)
    logging.info('Initialized chrome browser..')

    browser.get('chrome://extensions/')
    time.sleep(4)
    browser.get(BASE_URL)
    # with open(os.path.join("downloads_folder","ad_block.html"), "w", encoding='utf-8') as f:
    #     f.write(browser.page_source)

    # perf = browser.get_log('performance')
    # with open(os.path.join("downloads_folder","o_nw.json"), "w", encoding='utf-8') as f:
    #     json.dump(perf, f, indent=4)

    # proxy.new_har("myhar")
    # with open(os.path.join("downloads_folder",'myhar.har'), 'w') as har_file:
    #     json.dump(proxy.har, har_file)
    logging.info('Accessed %s ..', BASE_URL)

    logging.info('Page title: %s', browser.title)
    p = input()
    browser.quit()
    display.stop()


if __name__ == '__main__':
    chrome_example()
    # firefox_example()
    # phantomjs_example()