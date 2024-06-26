from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import pandas as pd

driver = webdriver.Chrome()


def get_times(gender):

    """gender = string 
    Returns the finished dataframe
    Works as of the 14/05/2024, might be deprecated in the future"""

    path = f'Data/Scraped_data/{gender}_Athletes.csv'
    data = []
    df = pd.read_csv(path)
    for _,i in df.iterrows():
        url = i['Link']
        name = i['Name']
        try:
            driver.get(url)
            ##finding the relevant button
            
            times = driver.find_element(By.TAG_NAME, value='body')
            times = times.find_element(By.CLASS_NAME, value = 'profileStatistics_fullStats__2G6op')
            times = times.find_element(By.CLASS_NAME, value='profileStatistics_fullStatsInner__33eTg')
            button = times.find_element(By.CLASS_NAME, value='profileStatistics_tabs__1cAYd')
            button = button.find_element(By.TAG_NAME, value='ul')
            button = button.find_elements(By.TAG_NAME, value= 'li')[4]
            button = button.find_element(By.TAG_NAME, value= 'div')

            ## CLicking on the button

            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            button.click()
            times = times.find_elements(By.CLASS_NAME, value='profileStatistics_statsTable__xU9PN')
            times = [time.text.split('\n') for time in times]
            ### Adding the data the list in the rawest form possible

            data.append([name, times])
        except Exception:
            print("Error occured, skipping to next iteration")
            continue
    data = pd.DataFrame(data, columns= ['Name' , 'Races'])
    data.to_csv(f'Data/Scraped_tables/{gender}_performances.csv', index=False)


#tests
if __name__ == "__main__":
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

