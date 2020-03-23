### Assumption : Confirmed_cases.csv exists in the working directory
from selenium import webdriver
import pandas as pd
import os
import re
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.keys import Keys
import time
import numpy as np
import random
from datetime import datetime
import collections

URL_logistics = "https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6"

def init(URL = "https://www.arcgis.com/apps/opsdashboard/index.html#/85320e2ea5424dfaaa75ae62e5c06e61"):
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    br = webdriver.Chrome(executable_path=r"C:/Users/qasim/Downloads/chromedriver_win32_v80/chromedriver.exe",options=chrome_options)
    br.get(URL)
    time.sleep(3)
    return br

def extract_num(string):
    string = string.split(" ")[0]
    return int(string.replace(",", ""))

def main():
    br = init(URL_logistics)
    DATA = str(br.find_element_by_tag_name("body").text).split("\n")[1:]
    logistics = {"CONFIRMED" : extract_num(DATA[1 + DATA.index("Total Confirmed")]), "DEATHS" : extract_num(DATA[1 + DATA.index("Total Deaths")]), "RECOVERED" : extract_num(DATA[1 + DATA.index("Total Recovered")])}
    TIME = str(datetime.now())
    TIME = ':'.join(TIME.split(":")[:-1])
    root = br.find_element_by_tag_name("body")
    root.screenshot("C:/Users/qasim/Desktop/Exigence/Track-COVID/Track-COVID/Visualizations/"+ TIME.split(" ")[0] +".png")
    root.screenshot("C:/Users/qasim/Desktop/Exigence/Track-COVID/Track-COVID/Visualizations/TODAY.png")

    TIME = str(datetime.now())
    TIME = ':'.join(TIME.split(":")[:-1])
    data = DATA[1+DATA.index("Confirmed Cases by Country/Region/Sovereignty"):DATA.index("Last Updated at (M/D/YYYY)")]
    case = {}
    for x in data:
        x = x.split(" ")
        country = " ".join(x[1:]).replace("*", "").strip()
        cases = int(x[0].replace(",",""))
        case[country] = cases
    case = collections.OrderedDict(sorted(case.items()))


    raw_data = {**logistics, **case}
    raw_data = collections.OrderedDict(sorted(raw_data.items()))
    df = pd.read_csv("C:/Users/qasim/Desktop/Exigence/Track-COVID/Track-COVID/Confirmed_case.csv")

    conts = list(df["Country"])
    curr_count = len(df["Country"])

    zero_fill = np.zeros(df.shape[1] - 1)

    for label in raw_data:
        if(label not in conts):
            temp = np.append(zero_fill, label)
            temp = temp[::-1]
            df.loc[curr_count] = temp
            curr_count+=1
            
    df = df.sort_values(by=['Country'], inplace=False).reset_index(drop=True)

    for i, label in enumerate(conts):
        if(label not in raw_data):
            add = df.iloc[i][-1]
            raw_data[label] = add
    raw_data = collections.OrderedDict(sorted(raw_data.items()))
    
    df_temp = pd.DataFrame.from_dict(raw_data, orient="index", columns=[TIME]).reset_index()

    
    
    del df_temp["index"]

    df_cum = [df, df_temp]

    df_cum = pd.concat(df_cum, axis=1)
    
    null_values = df_cum[df_cum[TIME].isnull()].index.tolist()

    if(len(null_values) > 0):
        priori = df_cum.columns[-2]
        df_copy = df_cum.copy()

        for x in null_values:
            value = df_copy[priori][x]
            df_cum.loc[:,TIME][x] = value

        del df_copy
    
    df_cum.to_csv("C:/Users/qasim/Desktop/Exigence/Track-COVID/Track-COVID/Confirmed_case.csv", index=False)
    
    return {"CODE" : "200", "Total Confirmed Cases" : logistics["CONFIRMED"], "TIME" : TIME}

if __name__ == "__main__":
    status = main()
    print(status)
