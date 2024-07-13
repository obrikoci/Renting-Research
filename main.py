from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfiyRGd82SxeTP7HKKDexOhOYnII-MkeemjDrteaWIYwMTCDA/viewform?usp=sf_link"
ZILLOW_URL = "https://appbrewery.github.io/Zillow-Clone/"

# -------------------------------------GETTING HOLD OF ADDRESS, PRICE AND LINK------------------------------------------

response = requests.get(ZILLOW_URL)
zillow_website = response.text

soup = BeautifulSoup(zillow_website, "html.parser")

all_links_tags = soup.select(".ListItem-c11n-8-84-3-StyledListCardWrapper a")
links = []
for tag in all_links_tags:
    link = tag.get("href")
    if link not in links:
        links.append(link)

all_prices_tags = soup.select(".ListItem-c11n-8-84-3-StyledListCardWrapper .PropertyCardWrapper__StyledPriceLine")
prices = []
for tag in all_prices_tags:
    price_text = tag.text
    if "+" in price_text:
        price = price_text.split("+")[0]
    else:
        price = price_text.split("/")[0]
    prices.append(price)

all_address_tags = soup.select(".ListItem-c11n-8-84-3-StyledListCardWrapper address")
addresses = []
for tag in all_address_tags:
    address = tag.text.strip()
    if "|" in address:
        address = address.replace(" |","")
    addresses.append(address)

# --------------------------------COMPLETING THE FORM AND CREATING THE SPREADSHEET--------------------------------------
chrome_opts = webdriver.ChromeOptions()
chrome_opts.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_opts)
driver.get(FORM_URL)

for n in range(len(links)):
    sleep(2)
    address_field = driver.find_element(By.XPATH,"/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")
    price_field = driver.find_element(By.XPATH,"/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input")
    link_field = driver.find_element(By.XPATH,"/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input")
    submit_button = driver.find_element(By.XPATH,"/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span/span")

    address_field.send_keys(addresses[n])
    sleep(1.5)
    price_field.send_keys(prices[n])
    sleep(1.5)
    link_field.send_keys(links[n])
    sleep(1.5)
    submit_button.click()

    sleep(2)
    submit_another_response = driver.find_element(By.LINK_TEXT, "Submit another response")
    submit_another_response.click()

# After going to Google Forms manually (bcs we need to be signed in for this part) and clicking "Link To Sheets"
sheets_link = "https://docs.google.com/spreadsheets/d/1rLgwP2Bw18u7RfYH5dVNOdGjtW9o2gMllANd3yg96BA/edit?resourcekey=&gid=2111879424#gid=2111879424"
print(f"Link to the Sheets with all the details added: \n{sheets_link}")


