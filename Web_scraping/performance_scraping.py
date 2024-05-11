from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

driver = webdriver.Chrome()


def get_times(gender):
    path = f'Data/Scraped_data/{gender}_Athletes.csv'
    data = []
    df = pd.read_csv(path, header=True)
    for _,i in df.iterrows():
        url = i['Link']
        name = i['Name']
        driver.get(url)

        times = driver.find_element(By.TAG_NAME, value='body')
        times = times.find_element(By.CLASS_NAME, value = 'profileStatistics_fullStats__2G6op')
        times = times.find_element(By.CLASS_NAME, value='profileStatistics_fullStatsInner__33eTg')
        button = times.find_element(By.CLASS_NAME, value='profileStatistics_tabs__1cAYd')
        button = button.find_element(By.TAG_NAME, value='ul')
        button = button.find_elements(By.TAG_NAME, value= 'li')[4]
        button = button.find_element(By.TAG_NAME, value= 'div')
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        button.click()
        times = times.find_elements(By.CLASS_NAME, value='profileStatistics_statsTable__xU9PN')
        times = [time.text.split('\n') for time in times]
        data.append([name, times])
    data.to_csv('Data/Scraped_data/Men_competitions.csv', index=False)


data = []
url = 'https://worldathletics.org/athletes/ethiopia/sisay-lemma-14547527'
name = 'Lemma'
driver.get(url)

times = driver.find_element(By.TAG_NAME, value='body')
times = times.find_element(By.CLASS_NAME, value = 'profileStatistics_fullStats__2G6op')
times = times.find_element(By.CLASS_NAME, value='profileStatistics_fullStatsInner__33eTg')
button = times.find_element(By.CLASS_NAME, value='profileStatistics_tabs__1cAYd')
button = button.find_element(By.TAG_NAME, value='ul')
button = button.find_elements(By.TAG_NAME, value= 'li')[4]
button = button.find_element(By.TAG_NAME, value= 'div')
driver.execute_script("arguments[0].scrollIntoView(true);", button)
button.click()
times = times.find_elements(By.CLASS_NAME, value='profileStatistics_statsTable__xU9PN')
times = [time.text.split('\n') for time in times]
data.append([name, times])

