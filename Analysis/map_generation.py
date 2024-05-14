import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import os


output_dir = 'Data/Figures'
os.makedirs(output_dir, exist_ok=True)

# Load your data into a pandas DataFrame
men = pd.read_csv('Data/Preprocessed_tables/Men_athletes.csv')
women = pd.read_csv('Data/Preprocessed_tables/Women_athletes.csv')
replacements = {'GER' : 'DEU', 
                'POR' : 'PRT', 
                'SUI' : 'CHE', 
                'DEN': 'DNK',
                'ALG' : 'DZA',
                'CHI' : 'CHL',
                'SAU' : 'KSA',
                'RSA':'ZAF',
                'CON' : 'COD',
                'CAM': 'CMR',
                'NED': 'NLD'}


def plot_countries():
    """Returns the saved figure for the distribution of athletes per country
    using the geopandas world map"""


    df = pd.concat([men, women], axis=0, ignore_index=True)
    df['Nationality'] = df['Nationality'].replace(replacements)


    # Count the number of occurrences of each country
    country_counts = df['Nationality'].value_counts().reset_index()
    country_counts.columns = ['Nationality', 'Count']

    # Load the world map from GeoPandas
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world = world[world.name != "Antarctica"]

    # Merge the country counts
    world = world.merge(country_counts, how='left', left_on='iso_a3', right_on='Nationality')
    world['Athletes_vs_pop'] = world['Count']/world['pop_est']*10000

    fig, ax = plt.subplots(1, 1, figsize=(15, 10))

    xmin, xmax, ymin, ymax = -150, 160, -55, 75
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    # Draw a frame around the continents
    frame = plt.Rectangle((xmin, ymin), xmax-xmin, ymax-ymin,
                        linewidth=1, edgecolor='black', facecolor='lightblue')
    ax.add_patch(frame)

    # Plot the world map 
    world.plot(column='Count', ax=ax, legend=False,
            edgecolor='black',  
            linewidth=0.5,        
            missing_kwds={"color": "lightgrey"})

    # Create background
    ax.set_facecolor('lightblue')  
    fig.patch.set_facecolor('white') 


    #Plot settings
    sm = plt.cm.ScalarMappable(Normalize(vmin=country_counts['Count'].min(), vmax=country_counts['Count'].max()))
    sm._A = []  
    cbar = fig.colorbar(sm, ax=ax, orientation='vertical', pad=0.02, shrink=0.5)
    cbar.set_label('Number of Athletes by Country', fontsize=12)
    ax.axis('off')


    # Save the figure
    output_path = os.path.join(output_dir, 'Athletes_countries.png')
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    return world



def plot_countries_vs_pop(world):
    """Takes in world as an arugment which will be returned from the function above : 
    It is simply the athletes dataframe joined on the world map
    Returns the saved figure"""
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))

    xmin, xmax, ymin, ymax = -150, 160, -55, 75
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    # Draw a frame
    frame = plt.Rectangle((xmin, ymin), xmax-xmin, ymax-ymin,
                        linewidth=1, edgecolor='black', facecolor='lightblue')
    ax.add_patch(frame)
    world.plot(column='Athletes_vs_pop', ax=ax, legend=False,
            edgecolor='black',  
            linewidth=0.5,         
            missing_kwds={"color": "lightgrey"})

    # Set background
    ax.set_facecolor('lightblue')  
    fig.patch.set_facecolor('white')  


    # Plot design
    sm = plt.cm.ScalarMappable(Normalize(vmin=world['Athletes_vs_pop'].min(), vmax=world['Athletes_vs_pop'].max()))
    sm._A = []
    cbar = fig.colorbar(sm, ax=ax, orientation='vertical', pad=0.02, shrink=0.5)
    cbar.set_label('Density of Athletes by Country (/10000 person)', fontsize=12)
    ax.axis('off')

    # Save the figure
    output_path = os.path.join(output_dir, 'Athletes_countries_pop.png')
    plt.savefig(output_path, bbox_inches='tight', dpi=300)

