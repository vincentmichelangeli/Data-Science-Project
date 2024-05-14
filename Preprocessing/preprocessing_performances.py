import ast
import re
import pandas as pd
from datetime import timedelta
import pandas as pd

# Function to convert a time string to a timedelta object
def parse_time_to_timedelta(time_str):

    """ Parsing the time_str : string to get timedelta objects
    time_str follow a certain shape present in the scraped dataframe"""


    # Split the time string 
    parts = re.split('[:.]', time_str)
    parts = [int(re.sub(r'\D', '', part)) for part in parts]

    if len(parts) == 2:  # Minutes and Seconds
        return timedelta(minutes=parts[0], seconds=parts[1])
    elif len(parts) == 3 and time_str.count(':') == 2:  # Hours, Minutes, Seconds
        return timedelta(hours=parts[0], minutes=parts[1], seconds=parts[2])
    elif len(parts) == 3:  # Minutes, Seconds, Hundredths of a second
        return timedelta(minutes=parts[0], seconds=parts[1], milliseconds=parts[2]*10)
    return None

# Function to extract time
def extract_time(parts):
    combined_string = ' '.join(parts)
    time_pattern = re.compile(r'\b(\d{1,2}:\d{2}(?::\d{2})?(?:\.\d{1,2})?)\b')
    match = time_pattern.search(combined_string)
    if match:
        return parse_time_to_timedelta(match.group(0))
    return None

# Function to extract the required data
def process_races(row):

    """ Row is a row from the scraped dataframe, 
    returns an array with a nicer shape to handle"""


    races = ast.literal_eval(row['Races'])
    records = []
    for race in races:
        race_name = race[0]
        if race_name in ['1500 Metres', '10 Kilometres Road', '5000 Metres','Half Marathon', '10,000 Metres', 'Marathon']:
            for performance in race[2:]:
                parts = performance.split()
                year = parts[0]
                time_delta = parse_time_to_timedelta(parts[1])
                if time_delta:  
                    records.append([row['Name'], race_name, year, time_delta])

    return records


def full_data_process(Gender):


    """ Using all the function above for the table corresponding to 
    Gender : 'Men'|'Women' table"""


    records = []
    df_perf = pd.read_csv(f'Data\Scraped_tables\{Gender}_performances.csv')
    df_perf.apply(lambda row: records.extend(process_races(row)), axis=1)
    records = pd.DataFrame(records, columns=['Name', 'Race', 'Year', 'Time'])
    pd.to_datetime(records['Year'])
    records = records.pivot_table(index=['Name', 'Year'], columns='Race', values='Time', aggfunc='first')
    records.to_csv(f'Data\Preprocessed_tables\{Gender}_performances.csv')

