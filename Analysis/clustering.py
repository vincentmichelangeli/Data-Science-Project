import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np



df = pd.read_csv('Data/Preprocessed_tables/Men_performances.csv')

df = df.drop(columns=['Year'])
# Drop the Name column for clustering
names = df.pop('Name')


def time_to_seconds(t):
    if pd.isnull(t):
        return np.nan
    return t.hour * 3600 + t.minute * 60 + t.second + t.microsecond / 1e6

for col in df.columns:
    df[col] = df[col].apply(time_to_seconds)

# Impute missing values using KNN
imputer = KNNImputer(n_neighbors=3)
df_imputed = imputer.fit_transform(df)
df_imputed = pd.DataFrame(df_imputed, columns=df.columns)

# Standardize the data
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_imputed)

# Perform KMeans clustering
kmeans = KMeans(n_clusters=2, random_state=42)
clusters = kmeans.fit_predict(df_scaled)

# Add the cluster labels back to the original DataFrame
df['Name'] = names
df['Cluster'] = clusters

print(df)