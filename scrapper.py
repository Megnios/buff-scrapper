import requests
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
import schedule
from random import randint



class Scrapper:

    def _isvalidchar(self, caracter):

        return caracter.isdigit() or caracter == '.'


    def __init__(self):

        self._currentData = None
        self._currentID = -1
        self._totalIDs = {'45237', '763236', '835615', '927964', '928034', '927994'}


    def _find(self, data):

        dataToText = data.text
        price = ""
        i = dataToText.index('¥') + 2

        while i < len(dataToText) and self._isvalidchar(dataToText[i]):

            price += dataToText[i]
            
            i += 1
        
        return price


    def _write (self):
        
        with open("precio.txt", "a") as file:

            file.write(datetime.now().strftime("%d,%m,%y,%H"))
            file.write(',')
            file.write(self._currentID)
            file.write(',')
            file.write(self._find(self._currentData))
            file.write('\n')


    def _fetchData(self):

        driver = webdriver.Chrome()
        driver.get("https://buff.163.com/goods/{}?from=market#tab=selling".format(self._currentID))
        xpath = "//div[@class='market-list']//div[@class='l_Layout']//div[@class='detail-tab-cont']//table[@class='list_tb']"
        self._currentData = driver.find_element(By.XPATH, xpath)
        #driver.quit()


    def _loop(self):
        
        for ID in self._totalIDs:
            
            self._currentID = ID
            self._fetchData()
            self._write()
            time.sleep(randint(3, 100))
            

    def entryPoint(self):
        self._loop()
        schedule.every().hour.do(self._loop)

        while True:
            time.sleep(301)
            schedule.run_pending()




scrapper = Scrapper()
scrapper.entryPoint()


