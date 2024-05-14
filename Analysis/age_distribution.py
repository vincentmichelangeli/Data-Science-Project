import pandas as pd
import matplotlib.pyplot as plt

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

print(create_age_performance_table('Men'))

def plot_distribution(Gender):
    perf_by_age = create_age_performance_table(Gender)
    perf_by_age = perf_by_age.groupby('Age').apply(lambda x: x.count())[races]
    perf_by_age = perf_by_age[perf_by_age.index>14]
    plt.figure(figsize=(10,7))
    for col in races:
        plt.plot(perf_by_age[col], label = col)
    plt.legend()
    plt.show()

plot_distribution('Men')