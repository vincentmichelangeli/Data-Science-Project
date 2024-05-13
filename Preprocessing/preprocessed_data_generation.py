import pandas as pd
from preprocessing_performances import process_races
from preprocessing_athletes import process_athletes

df_men = pd.read_csv('Data\Scraped_data\Men_Athletes.csv')
df_men = process_athletes(df_men)
df_men.to_csv('Data\Preprocessed_data\Men_athletes.csv')

df_women = pd.read_csv('Data\Scraped_data\Women_Athletes.csv')
df_women = process_athletes(df_women)
df_women.to_csv('Data\Preprocessed_data\Women_athletes.csv')

df_men_perf = pd.read_csv('Data\Scraped_data\Men_performances.csv')
new_records = []
df_men_perf.apply(lambda row: new_records.extend(process_races(row)), axis=1)
df_men_perf = pd.DataFrame(new_records, columns=['Name', 'Race', 'Year', 'Time'])
pd.to_datetime(df_men_perf['Year'])
df_men_perf.to_csv('Data\Preprocessed_data\Men_performances.csv')

df_women_perf = pd.read_csv('Data\Scraped_data\Women_performances.csv')
new_records = []
df_women_perf.apply(lambda row: new_records.extend(process_races(row)), axis=1)
df_women_perf = pd.DataFrame(new_records, columns=['Name', 'Race', 'Year', 'Time'])
pd.to_datetime(df_women_perf['Year'])
df_women_perf.to_csv('Data\Preprocessed_data\Women_performances.csv')

