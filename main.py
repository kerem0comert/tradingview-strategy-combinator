from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from itertools import product
from dataclasses import dataclass

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

@dataclass
class Row: 
    comb: tuple
    result: float
        

max_row = None

while 1:
    fileName = f'{input("File name: ")}.txt'
    with open(fileName, 'a') as file:
        elemCount = int(input("Enter the count of inputs: "))
        for i in range(1, elemCount + 1):
            xpath = f'//*[@id="overlap-manager-root"]/div/div/div[1]/div/div[3]/div/div[{i * 2}]/div/span/span[1]/input'
            inputsList.append(driver.find_element_by_xpath(xpath))
            
        for elem in inputsList:
            value = int(elem.get_attribute('value'))
            thresholdDiff = int((value) * THRESHOLD_PERCENTAGE)
            valuesList.append([i for i in range(value - thresholdDiff, value + thresholdDiff)])
            
        combinations = list(product(*valuesList))
        for comb in combinations:
            results = {}
            for idx, val in enumerate(comb):
                inputsList[idx].send_keys(Keys.CONTROL + "a")
                inputsList[idx].send_keys(Keys.DELETE)
                inputsList[idx].send_keys(val)
            
            sleep(0.4)
            net_profit = (driver.find_element_by_class_name('additional_percent_value')).text.split(" ")[0]
            result_line = f"{comb} : {net_profit}"
            print(result_line)
            file.write(f"{result_line}\n")
            
            if max_row is None or net_profit > max_row.result:
                max_row = Row(comb, net_profit)
            
        print(max_row.__dict__)
        file.write(str(max_row.__dict__))
        file.close()
    
