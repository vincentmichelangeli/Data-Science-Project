import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np
from sklearn.metrics import silhouette_score
import re
import matplotlib.pyplot as plt
import os


datetime_columns = ['1500 Metres', '10 Kilometres Road', '5000 Metres','Half Marathon', '10,000 Metres', 'Marathon']

def time_to_seconds(t):
    if pd.isnull(t):
        return np.nan
    t = t.split()[2]
    t = re.split('[:.]', t)
    time = float(t[0])*3600 + float(t[1]) * 60 + float(t[2])
    if len(t) == 4:
        time += float(t[3]) /1e6
    return time

def impute_missing_performances(Gender):
    df = pd.read_csv(f'Data/Preprocessed_tables/{Gender}_performances.csv')

    df = df.drop(columns=['Year'])
    # Drop the Name column for clustering
    names = df.pop('Name')

    for col in df.columns:
        df[col] = df[col].apply(time_to_seconds)

    # Impute missing values using KNN
    imputer = KNNImputer(n_neighbors=3)
    df_imputed = imputer.fit_transform(df)
    df_imputed = pd.DataFrame(df_imputed, columns=df.columns)

    df['Name'] = names
    df_imputed['Name'] = names
    return df_imputed,df

def generate_best_performance(df,df_imputed):
    df = df.groupby('Name').min()

    best_performance = df_imputed.groupby('Name').min()


    # Combine the DataFrames by keeping the maximum values for each column
    best_performance = best_performance.combine(df, np.fmax)

    # Reset the index to have 'Name' as a column again
    best_performance.reset_index(inplace=True)

    names = best_performance.pop('Name')
    return best_performance,names

def clustering_pca(best_performance,names):
    # Standardize the data
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(best_performance)

    silhouette = []
    # Perform KMeans clustering
    for i in range(2,7):
        kmeans = KMeans(n_clusters=i, random_state=42)
        clusters = kmeans.fit_predict(df_scaled)
        silhouette.append(silhouette_score(df_scaled, clusters))

    k = np.argmax(silhouette) + 2
    kmeans = KMeans(n_clusters=k, random_state=42)
    clusters = kmeans.fit_predict(best_performance)

    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(df_scaled)

    # Add the PCA result back to the DataFrame
    best_performance['PCA1'] = pca_result[:, 0]
    best_performance['PCA2'] = pca_result[:, 1]

    # Add the cluster labels back to the original DataFrame
    best_performance['Cluster'] = clusters
    best_performance['Name'] = names
    return best_performance


def make_plot(best_performance,Gender):
    plt.figure(figsize=(10, 7))

    # Define a color map for clusters
    colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']

    for cluster in best_performance['Cluster'].unique():
        cluster_data = best_performance[best_performance['Cluster'] == cluster]
        plt.scatter(cluster_data['PCA1'], cluster_data['PCA2'], label=f'Cluster {cluster}', c=colors[cluster % len(colors)], alpha=0.6, edgecolors='w', s=50)

    if Gender == 'Men':
        points_to_label = ['Eliud KIPCHOGE','Kelvin KIPTUM', 'Jakob INGEBRIGTSEN', 'Kenenisa BEKELE', 'Mehdi FRÈRE', 'Jimmy GRESSIER', 'Joshua CHEPTEGEI']
    else:
        points_to_label = ['Letesenbet GIDEY','Sifan HASSAN','Tigst ASSEFA','Faith KIPYEGON']
    for point in points_to_label:
        label_data = best_performance[best_performance['Name'] == point]
        cluster = best_performance[best_performance['Name'] == point]['Cluster'].values[0]
        plt.scatter(label_data['PCA1'], label_data['PCA2'], c=colors[cluster % len(colors)], edgecolor='black', s=100, linewidth=1.5)
        plt.text(label_data['PCA1'].values[0], label_data['PCA2'].values[0], point.split()[1], fontsize=10, ha='right', weight = 'bold')

    clusters_to_label = [1]
    num_points_to_label = 5

    for cluster in clusters_to_label:
        cluster_data = best_performance[best_performance['Cluster'] == cluster]
        sampled_points = cluster_data.sample(n=num_points_to_label, random_state=42)
        for __, row in sampled_points.iterrows():
            plt.scatter(row['PCA1'], row['PCA2'], c=colors[cluster % len(colors)], edgecolor='black', s=100, linewidth=1.5)  # Outline the point
            plt.text(row['PCA1'], row['PCA2'], row['Name'].split()[-1], fontsize=10, ha='right', weight = 'bold')


    plt.title('PCA of Clustered Data')
    plt.title('PCA of Clustered Data')
    plt.xlabel('PCA1')
    plt.ylabel('PCA2')
    plt.legend()
    plt.grid(True)
    plt.show()

    output_dir = 'Data/Figures'
    os.makedirs(output_dir, exist_ok=True)

    # Save the figure
    output_path = os.path.join(output_dir, f'{Gender}_Athletes_clustering.png')
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.savefig()
