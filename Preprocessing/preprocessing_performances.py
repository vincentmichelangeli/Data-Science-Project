import pandas as pd
import ast
import re
from datetime import timedelta

# Function to convert a time string to a timedelta object
def parse_time_to_timedelta(time_str):
    # Split the time string by delimiters ':' and '.'
    parts = re.split('[:.]', time_str)
    parts = [int(re.sub(r'\D', '', part)) for part in parts]  # Convert all parts to integers
    if len(parts) == 2:  # Minutes and Seconds
        return timedelta(minutes=parts[0], seconds=parts[1])
    elif len(parts) == 3 and time_str.count(':') == 2:  # Hours, Minutes, Seconds
        return timedelta(hours=parts[0], minutes=parts[1], seconds=parts[2])
    elif len(parts) == 3:  # Minutes, Seconds, Hundredths of a second
        return timedelta(minutes=parts[0], seconds=parts[1], milliseconds=parts[2]*10)
    return None

# Function to identify and extract time from a string using regex
def extract_time(parts):
    combined_string = ' '.join(parts)
    time_pattern = re.compile(r'\b(\d{1,2}:\d{2}(?::\d{2})?(?:\.\d{1,2})?)\b')
    match = time_pattern.search(combined_string)
    if match:
        return parse_time_to_timedelta(match.group(0))
    return None

# Function to parse the races string and extract the required data
def process_races(row):
    races = ast.literal_eval(row['Races'])
    records = []
    for race in races:
        race_name = race[0]
        if race_name in ['1500 Metres', '10 Kilometres Road', '5000 Metres','Half Marathon', '10,000 Metres', 'Marathon']:
            for performance in race[2:]:
                parts = performance.split()
                year = parts[0]
                time_delta = extract_time(parts)
                if time_delta:  # Ensure there is a valid time delta before appending
                    records.append([row['Name'], race_name, year, time_delta])
    return records

# Example DataFrame (adjust to your actual data loading)
data = {
    'Name': ['John Doe', 'Jane Smith'],
    'Races': [
        "[['1500 Metres', 'Year Performance Venue Date', '2021 3:54.7 Moi International Sports Centre, Kasarani, Nairobi (KEN) 12 MAR 2021']]",
        "[['10 Kilometres Road', 'Year Performance Venue Date', '2022 27:35 Brasov (ROU) 25 SEP 2022', '2024 27:01 Valencia (ESP) 14 JAN 2024']]"
    ]
}

df = pd.DataFrame(data)

new_records = []
df.apply(lambda row: new_records.extend(process_races(row)), axis=1)

result_df = pd.DataFrame(new_records, columns=['Name', 'Race', 'Year', 'Time'])
print(result_df)
