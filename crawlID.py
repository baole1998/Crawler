from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chromedriver = '/Users/lebao/PycharmProjects/project1/chromeDriver/chromedriver'

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chromedriver)
driver.get('https://masothue.com/')
elem1 = driver.find_element_by_name('q')
elem1.send_keys('001096013150' + Keys.RETURN)
time.sleep(2)
elem2 = driver.find_element_by_xpath('//*[@id="main"]/section[1]/div/table/tbody/tr[3]/td[2]/span')
name = elem2.text

time.sleep(2)
driver.get('https://baohiemxahoi.gov.vn/tracuu/Pages/tra-cuu-ho-gia-dinh.aspx')
elem3 = driver.find_element_by_xpath('//*[@id="ctl00_ctl39_g_caca5e50_572a_42fe_963e_83cbf9d90375"]/div[2]/div[2]/div/div[2]/div/div[1]/div[1]/div/div/div/button/span[1]')
arena = elem3.click()
time.sleep(2)
elem4 = driver.find_element_by_xpath('//*[@id="ctl00_ctl39_g_caca5e50_572a_42fe_963e_83cbf9d90375"]/div[2]/div[2]/div/div[2]/div/div[1]/div[1]/div/div/div/div/ul/li[63]/a')
city = elem4.click()
time.sleep(2)

fieldHoten = driver.find_element_by_id('HoTen')
try:
    fieldHoten.send_keys(name)
except Exception as e:
    print(e)
    driver.close()
time.sleep(2)

cmnd = driver.find_element_by_id('CMND')
cmnd.send_keys('001096013150')

