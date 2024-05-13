import pandas as pd

def process_athletes(df):
    df['Date of Birth'] = pd.to_datetime(df['Date of Birth'])
    df['Year of Birth'] = df['Date of Birth'].dt.year
    new_df = df[['Name', 'Nationality', 'Year of Birth']]
    return new_df