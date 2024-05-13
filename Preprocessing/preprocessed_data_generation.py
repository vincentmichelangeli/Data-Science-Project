import pandas as pd
from preprocessing_performances import process_races


df_men_perf = pd.read_csv('Data\Scraped_data\Men_performances.csv')
new_records = []
df_men_perf.apply(lambda row: new_records.extend(process_races(row)), axis=1)
df_men_perf = pd.DataFrame(new_records, columns=['Name', 'Race', 'Year', 'Time'])
df_men_perf.to_csv('Data\Preprocessed_data\Men_performances.csv')
