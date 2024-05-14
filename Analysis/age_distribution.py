import pandas as pd
import matplotlib.pyplot as plt
from clustering import time_to_seconds
import numpy as np

races = ['1500 Metres', '5000 Metres', '10 Kilometres Road', '10,000 Metres','Half Marathon', 'Marathon']

def create_age_performance_table(Gender):
    df_performance = pd.read_csv(f'Data/Preprocessed_tables/{Gender}_performances.csv')
    df_athletes = pd.read_csv(f'Data/Preprocessed_tables/{Gender}_athletes.csv')

    # Merge the performance data with the birth year data
    performances_by_age = pd.merge(df_performance, df_athletes, on='Name')
    performances_by_age['Year'] = performances_by_age['Year'].astype(float)
    performances_by_age['Year of Birth'] = performances_by_age['Year of Birth'].astype(float)

    # Calculate the age of the athletes at the time of each performance
    performances_by_age['Age'] = performances_by_age['Year'] - performances_by_age['Year of Birth']

    # Count the number of performances for each age
    return performances_by_age


def plot_distribution(Gender):
    perf_by_age = create_age_performance_table(Gender)
    perf_by_age = perf_by_age.groupby('Age').apply(lambda x: x.count())[races]
    perf_by_age = perf_by_age[perf_by_age.index>14]
    plt.figure(figsize=(10,7))
    for col in races:
        plt.plot(perf_by_age[col], label = col)
    plt.legend()
    plt.show()


def calculate_time_differences(df, columns):
    """Calculate the differences for successive years for a given column"""
    diffs = []
    previous_value = None
    
    for value in df[columns]:
        if previous_value is not None:
            diffs.append(value - previous_value)
        else:
            diffs.append(np.nan)
        previous_value = value
    
    return diffs

def plot_progression(Gender):
    perf_by_age = create_age_performance_table(Gender)

    perf_by_age.sort_values(by=['Name', 'Year'], inplace=True)

    # Calculate the time differences between successive years for each athlete
    progress_by_age = perf_by_age['Age']
    progress_by_year = perf_by_age['Year']
    for col in races:
        perf_by_age[col] = perf_by_age[col].apply(time_to_seconds)
        perf_by_age[col + '_diff'] = perf_by_age.groupby('Name')[col].diff()
        progress_by_age[col + '_diff'] = perf_by_age[col + '_diff']
        progress_by_year[col + '_diff'] = perf_by_age[col + '_diff']
    print(progress_by_age)

    progress_by_age = progress_by_age.groupby('Age').mean()
    progress_by_year = progress_by_year.groupby('Year').mean()
    plt.figure(figsize=(10,7))
    for col in races:
        plt.plot(progress_by_age[col + '_diff'], label = col)
    plt.legend()
    plt.show()



plot_distribution('Men')
plot_progression('Men')