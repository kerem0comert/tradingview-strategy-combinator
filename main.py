from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from itertools import product

"""
'//*[@id="overlap-manager-root"]/div/div/div[1]/div/div[3]/div/div[2]/div/span/span[1]/input'
'//*[@id="overlap-manager-root"]/div/div/div[1]/div/div[3]/div/div[4]/div/span/span[1]/input'
'//*[@id="overlap-manager-root"]/div/div/div[1]/div/div[3]/div/div[6]/div/span/span[1]/input'
"""
THRESHOLD_PERCENTAGE = 0.2

driver = webdriver.Chrome()
driver.get("https://www.tradingview.com/chart/")

inputsList = []
valuesList = []
while 1:
    elemCount = int(input("Enter the count of inputs: "))
    for i in range(1, elemCount + 1):
        xpath = f'//*[@id="overlap-manager-root"]/div/div/div[1]/div/div[3]/div/div[{i * 2}]/div/span/span[1]/input'
        inputsList.append(driver.find_element_by_xpath(xpath))
        
    for elem in inputsList:
        value = int(elem.get_attribute('value'))
        thresholdDiff = int(value * THRESHOLD_PERCENTAGE)
        valuesList.append([i for i in range(value - thresholdDiff, value + thresholdDiff)])
        
    combinations = list(product(*valuesList))
    for comb in combinations:
        for idx, val in enumerate(comb):
            inputsList[idx].send_keys(Keys.CONTROL + "a")
            inputsList[idx].send_keys(Keys.DELETE)
            inputsList[idx].send_keys(val)
        
        sleep(0.5)
        net_profit = driver.find_element_by_class_name('additional_percent_value')
        print(f"{comb} : {net_profit.text}")
