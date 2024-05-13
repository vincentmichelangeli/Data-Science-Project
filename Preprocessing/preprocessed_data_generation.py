import pandas as pd
from preprocessing_performances import process_races
from preprocessing_athletes import process_athletes
from preprocessing_performances import full_data_process

df_men = pd.read_csv('Data\Scraped_tables\Men_Athletes.csv')
df_men = process_athletes(df_men)
df_men.to_csv('Data\Preprocessed_tables\Men_athletes.csv')

df_women = pd.read_csv('Data\Scraped_data\Women_Athletes.csv')
df_women = process_athletes(df_women)
df_women.to_csv('Data\Preprocessed_tables\Women_athletes.csv')

full_data_process('Women')
full_data_process('Men')

