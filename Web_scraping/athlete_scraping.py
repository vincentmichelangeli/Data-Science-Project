from selenium import webdriver
from selenium.webdriver.common.by import By



driver = webdriver.Chrome()

data = []

def get_table(gender, events, n_pages):
    data = []
    for e in events:
        for i in range(1,n_pages):
            driver.get(f"https://worldathletics.org/world-rankings/{e}/{gender}?regionType=world&page={i}&rankDate=2024-05-05&limitByCountry=0")
            table = driver.find_element(By.TAG_NAME, value = 'body')
            table = table.find_element(By.CLASS_NAME , value='outer-container')
            table = table.find_element(By.CLASS_NAME, value='site-container')
            table = table.find_element(By.CLASS_NAME , value='records-table')
            table = table.find_element(By.TAG_NAME , value='tbody')
            buttons = table.find_elements(By.TAG_NAME, value="tr")

            # Iterate over each button element
            for button in buttons:
                # Find all <td> elements within each button
                athlete_url = "https://worldathletics.org" + button.get_attribute('data-athlete-url')
                tds = button.find_elements(By.TAG_NAME,value='td')

                # Get data from each <td>
                single_data = [td.text for td in tds[1:4]]
                single_data.append(athlete_url)
                # Find the URL (assuming it's contained in an <a> tag within the first <td>)
                data.append(single_data)
    return set(data)