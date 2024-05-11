from athlete_scraping import get_table
import pandas as pd

events = ["marathon","road-running","10000m","5000m","1500m"]

women_table = get_table("women",events,5)
women_df = pd.DataFrame(women_table,columns = ["Name", "Date of Birth", "Nationality", "Link"])
women_df.to_csv('Data/Scraped_data/Women_Athletes.csv', index=False)

men_table = get_table("men",events,5)
men_df = pd.DataFrame(women_table,columns = ["Name", "Date of Birth", "Nationality", "Link"])
men_df.to_csv('Data/Scraped_data/Men_Athletes.csv', index=False)