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
    """ t :string element from a column where the races are stored
    Output : float that represtent the matching number of seconds"""

    if pd.isnull(t):
        return np.nan
    t = t.split()[-1]
    t = re.split('[:.]', t)
    time = float(t[0])*3600 + float(t[1]) * 60 + float(t[2])
    if len(t) == 4:
        time += float(t[3]) /1e6
    return time

def impute_missing_performances(Gender):


    """ Gender : 'Men' | 'Women' : string represeting the table used
    Ouput : df,df_imputed : both the df with imputed values and the original one"""


    #Load the df
    df = pd.read_csv(f'Data/Preprocessed_tables/{Gender}_performances.csv')
    df = df.drop(columns=['Year'])
    names = df.pop('Name')

    #Convert times
    for col in df.columns:
        df[col] = df[col].apply(time_to_seconds)

    # Impute missing values
    imputer = KNNImputer(n_neighbors=3)
    df_imputed = imputer.fit_transform(df)
    df_imputed = pd.DataFrame(df_imputed, columns=df.columns)

    df['Name'] = names
    df_imputed['Name'] = names
    return df_imputed,df

def generate_best_performance(df,df_imputed):

    """ Inputs are the ouputs of the previous function
    Outputs : dataframe containing athletes pbs and the corresponding list of names"""

    df = df.groupby('Name').min()
    best_performance = df_imputed.groupby('Name').min()

    best_performance = best_performance.combine(df, np.fmax)

    # Reset the index to have 'Name' as a column again
    best_performance.reset_index(inplace=True)

    names = best_performance.pop('Name')
    return best_performance,names

def clustering_pca(best_performance,names):

    """ Input are the outputs of the previous functions
    Output : Dataframe with the best performances and the PCA of the athletes"""


    # Standardize the data
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(best_performance)

    silhouette = []

    #KMeans clustering cross validation

    for i in range(2,7):
        kmeans = KMeans(n_clusters=i, random_state=42)
        clusters = kmeans.fit_predict(df_scaled)
        silhouette.append(silhouette_score(df_scaled, clusters))

    k = np.argmax(silhouette) + 2
    kmeans = KMeans(n_clusters=k, random_state=42)
    clusters = kmeans.fit_predict(best_performance)

    # PCA
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(df_scaled)

    # Add the PCA
    best_performance['PCA1'] = pca_result[:, 0]
    best_performance['PCA2'] = pca_result[:, 1]

    # Add the cluster labels
    best_performance['Cluster'] = clusters
    best_performance['Name'] = names
    return best_performance


def make_plot(best_performance,Gender):

    """Makes the plot with the dataframe obtained before and the gender : string (Men or Women)"""
    plt.figure(figsize=(10, 7))

    # Define a color map for clusters
    colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']

    for cluster in best_performance['Cluster'].unique():
        cluster_data = best_performance[best_performance['Cluster'] == cluster]
        plt.scatter(cluster_data['PCA1'], cluster_data['PCA2'], label=f'Cluster {cluster}', c=colors[cluster % len(colors)], alpha=0.6, edgecolors='w', s=50)

    if Gender == 'Men':
        points_to_label = ['Eliud KIPCHOGE','Kelvin KIPTUM', 'Jakob INGEBRIGTSEN', 'Kenenisa BEKELE', 'Jimmy GRESSIER', 'Joshua CHEPTEGEI']
    else:
        points_to_label = ['Letesenbet GIDEY','Sifan HASSAN','Tigst ASSEFA','Faith KIPYEGON']
    for point in points_to_label:
        label_data = best_performance[best_performance['Name'] == point]
        cluster = best_performance[best_performance['Name'] == point]['Cluster'].values[0]
        plt.scatter(label_data['PCA1'], label_data['PCA2'], c=colors[cluster % len(colors)], edgecolor='black', s=100, linewidth=1.5)
        plt.text(label_data['PCA1'].values[0], label_data['PCA2'].values[0], point.split()[1], fontsize=10, ha='right', weight = 'bold')

    clusters_to_label = [1]
    num_points_to_label = 3

    for cluster in clusters_to_label:
        cluster_data = best_performance[best_performance['Cluster'] == cluster]
        sampled_points = cluster_data.sample(n=num_points_to_label, random_state=15)
        for __, row in sampled_points.iterrows():
            plt.scatter(row['PCA1'], row['PCA2'], c=colors[cluster % len(colors)], edgecolor='black', s=100, linewidth=1.5) 
            plt.text(row['PCA1'], row['PCA2'], row['Name'].split()[-1], fontsize=10, ha='right', weight = 'bold')


    plt.title('Visualisation of the clusters')
    plt.legend()
    if Gender == 'Women':
        plt.xlim(-6, 6)  
        plt.ylim(-5, 5)
    plt.grid(True)

    
    output_dir = 'Data/Figures'
    os.makedirs(output_dir, exist_ok=True)

    # Save the figure
    output_path = os.path.join(output_dir, f'{Gender}_Athletes_clustering.png')
    plt.savefig(output_path, bbox_inches='tight', dpi=300)


def final_clustering(Gender):
    """Gender : 'Men'| 'Women' function generates everything"""
    imputed_df,df = impute_missing_performances(Gender)
    best_performance, names = generate_best_performance(df,imputed_df)
    best_performance = clustering_pca(best_performance,names)
    make_plot(best_performance, Gender)
