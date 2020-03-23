### Pushes the .csv file to GitHub

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime

URL_pre = "https://github.com/login"
URL_post = "https://github.com/QasimWani/Track-COVID/upload/master"

def init():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    br = webdriver.Chrome(executable_path=r"C:/Users/PATH_TO_CHROMEDRIVER/chromedriver_win32_v80/chromedriver.exe",options=chrome_options)
    br.get(URL_pre)
    time.sleep(3)
    return br

def main():
    br = init()
    br.find_element_by_id("login_field").send_keys("EMAIL")
    br.find_element_by_id("password").send_keys("PASSWORD")
    button = br.find_element_by_class_name("btn.btn-primary.btn-block")
    button.click()

    br.get(URL_post)
    time.sleep(3)

    file_dir = "C:/Users/qasim/Desktop/Exigence/COVID-19/CoronaBluetooth/Diagnostics/Confirmed_case.csv"
    br.find_element_by_id("upload-manifest-files-input").send_keys(file_dir)

    time.sleep(3)
    TIME = str(datetime.now())
    TIME = ':'.join(TIME.split(":")[:-1])

    br.find_element_by_id("commit-summary-input").send_keys("auto data update : " + TIME)

    br.find_element_by_class_name("btn.btn-primary.js-blob-submit").click()

    time.sleep(10)
    br.close()

    print("GitHub Integration SUCCESS. @ Time = ", TIME)

if __name__ == "__main__":
    main()
    
