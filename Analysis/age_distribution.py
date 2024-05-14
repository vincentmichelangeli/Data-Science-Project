import os
import pandas as pd
import matplotlib.pyplot as plt
from clustering import time_to_seconds
import numpy as np

races = ['1500 Metres', '5000 Metres', '10 Kilometres Road', '10,000 Metres','Half Marathon', 'Marathon']
output_dir = 'Data/Figures'
os.makedirs(output_dir, exist_ok=True)

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
    # Save the figure
    plt.xlabel('Age')
    plt.ylabel('Number of athletes that competed')
    output_path = os.path.join(output_dir, f'{Gender}_Athletes_distribution.png')
    plt.savefig(output_path, bbox_inches='tight', dpi=300)


def calculate_time_differences(df, columns):
    """Calculate the differences for successive years for a given column"""
    diffs = {col: [] for col in columns}
    races_duration = {'1500 Metres' : 210, 
                    '5000 Metres' : 780,
                    '10 Kilometres Road' : 29*60,
                    '10,000 Metres' : 29*60,
                    'Half Marathon' : 61*60,
                    'Marathon' : 126*60}
    previous_values = {col: None for col in columns}
    
    for __, row in df.iterrows():
        for col in columns:
            if previous_values[col] is not None:
                diffs[col].append((- row[col] + previous_values[col])/races_duration[col])
            else:
                diffs[col].append(np.nan)
            previous_values[col] = row[col]
    
    for col in columns:
        df[col] = diffs[col]
    
    return df

def calculate_rolling_best_time(df, columns):
    """Calculate the differences for successive years for a given column"""
    best = {col: [] for col in columns}
    
    previous_values = {col: None for col in columns}
    
    for __, row in df.iterrows():
        for col in columns:
            if row[col] == 0:
                row[col] = np.nan
            if previous_values[col] is not None:
                previous_values[col] = np.fmin(row[col],previous_values[col])
                best[col].append(previous_values[col])
                
            else:
                previous_values[col] = np.fmin(row[col],np.nan)
                best[col].append(previous_values[col])
                
    for col in columns:
        df[col] = best[col]
    
    return df

def plot_progression(Gender):
    perf_by_age = create_age_performance_table(Gender)

    perf_by_age.sort_values(by=['Name', 'Year'], inplace=True)

    # Calculate the time differences between successive years for each athlete
    for col in races:
        perf_by_age[col] = perf_by_age[col].apply(time_to_seconds)
    races.append('Name')
    progress_by_age = perf_by_age[races].groupby('Name').apply(lambda x: calculate_rolling_best_time(x, races[:-1])).reset_index(level=0, drop=True)
    print(perf_by_age)
    progress_by_age = progress_by_age[races].groupby('Name').apply(lambda x: calculate_time_differences(x, races[:-1])).reset_index(level=0, drop=True)
    progress_by_age['Age'] = perf_by_age['Age']
    progress_by_age = progress_by_age.drop(columns='Name')

    progress_by_age = progress_by_age.groupby('Age').mean()
    progress_by_age = progress_by_age[progress_by_age.index<35]
    progress_by_age = progress_by_age[progress_by_age.index>20]

    plt.figure(figsize=(10,7))
    for col in races[:-1]:
        plt.plot(progress_by_age[col], label = col)
    plt.legend()
    plt.xlabel('Age')
    plt.ylabel('Relative time gained')

    # Save the figure
    output_path = os.path.join(output_dir, f'{Gender}_Athletes_progression.png')
    plt.savefig(output_path, bbox_inches='tight', dpi=300)


