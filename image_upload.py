### Pushes the .csv file to GitHub

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import os

URL_pre = "https://github.com/login"
URL_post = "https://github.com/QasimWani/Track-COVID/upload/master/Visualizations"

def init():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    br = webdriver.Chrome(executable_path=r"C:/Users/qasim/Downloads/chromedriver_win32_v80/chromedriver.exe",options=chrome_options)
    br.get(URL_pre)
    time.sleep(3)
    return br

def find_files(PATH):
    """
    Finds all the files in a particular directory. Return only .png files.
    """
    files = []
    for r, d, f in os.walk(PATH):
        for file in f:
            if '.png' in file:
                files.append(os.path.join(r, file).replace("\\","/"))
    return files

def send_files(files, br, i,f):
    for x in files[i:f]:
        br.find_element_by_id("upload-manifest-files-input").send_keys(x)
    time.sleep(3)
    TIME = str(datetime.now())
    TIME = ':'.join(TIME.split(":")[:-1])

    br.find_element_by_id("commit-summary-input").send_keys("auto visuals update : " + TIME)

    br.find_element_by_class_name("btn.btn-primary.js-blob-submit").click()

def main():
    file_dir = "C:/Users/qasim/Desktop/Exigence/Track-COVID/Track-COVID/Visualizations"
    files = find_files(file_dir)

    br = init()
    br.find_element_by_id("login_field").send_keys("TEST@gmail.com")
    br.find_element_by_id("password").send_keys("TEST")
    button = br.find_element_by_class_name("btn.btn-primary.btn-block")
    button.click()
    br.get(URL_post)
    time.sleep(3)
    send_files(files, br, 0, 50)
    br.get(URL_post)
    send_files(files, br, 50, len(files))
    br.close()

if __name__ == "__main__":
    main()
    print("Successfully uploaded all images on GitHub")