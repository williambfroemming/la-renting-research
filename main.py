from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import requests
import lxml

GOOGLE_FORM_LINK = YOUR GOOGLE FORM LINK
ZILLOW_LINK = YOUR ZILLOW LINK
CHROME_DRIVER_PATH = YOUR CHROME DRIVER PATH
HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

# Gets all data from Zillow and
response = requests.get(ZILLOW_LINK, headers=HEADER)
webpage = response.text
soup = BeautifulSoup(webpage, "lxml")

# Final all addresses of the listings
addresses = soup.find_all(class_="list-card-addr")
address_list = [address.getText() for address in addresses]
print(address_list)

# Find all links
links = soup.find_all(class_="list-card-link")
link_list = [link.get("href") for link in links]
print(link_list)

# Find all prices
prices = soup.find_all(class_="list-card-price")
price_list = [price.getText() for price in prices]
print(price_list)

# Use Selenium to open the google form and input all the data scraped from Zillow
chrome_driver_path = CHROME_DRIVER_PATH
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get(GOOGLE_FORM_LINK)
sleep(3)
for i in range(len(address_list)):
    address_input = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_input.send_keys(address_list[i])

    price_input = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input.send_keys(price_list[i])

    link_input = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input.send_keys(link_list[i])

    submit = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')
    submit.click()
    sleep(.5)
    new_submission = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    new_submission.click()
    sleep(.5)

