from selenium import webdriver
import requests
from bs4 import BeautifulSoup


driver_path = '/utils/chrome_driver/chromedriver.exe'
driver = webdriver.Chrome()


driver.get('https://worldathletics.org/world-rankings/road-running/women?regionType=world&page=1&rankDate=2024-05-05&limitByCountry=0')

table = driver.find_element_by_class_name('records-table')
buttons = table.find_element_by_tag_name("tr")

data = []

# Iterate over each button element
for button in buttons:
    # Find all <td> elements within each button
    athlete_url = button.get_attribute('data-athlete-url')
    tds = button.find_element_by_tag_name('td')

    # Get data from each <td>
    single_data = [td.text for td in tds]
    single_data.append(athlete_url)
    # Find the URL (assuming it's contained in an <a> tag within the first <td>)
    data.append(single_data)
