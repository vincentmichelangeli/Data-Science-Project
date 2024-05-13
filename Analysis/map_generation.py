import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize


# Load your data into a pandas DataFrame
df = pd.read_csv('Data/Preprocessed_data/Men_athletes.csv')

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


df['Nationality'] = df['Nationality'].replace(replacements)

# Count the number of occurrences of each country
country_counts = df['Nationality'].value_counts().reset_index()
country_counts.columns = ['Nationality', 'Count']
print(country_counts)

# Load the world map from GeoPandas
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Exclude Antarctica
world = world[world.name != "Antarctica"]
print(world)

# Merge the country counts with the world map
world = world.merge(country_counts, how='left', left_on='iso_a3', right_on='Nationality')

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(15, 10))

xmin, xmax, ymin, ymax = -150, 160, -55, 75
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

# Draw a frame around the continents
frame = plt.Rectangle((xmin, ymin), xmax-xmin, ymax-ymin,
                      linewidth=1, edgecolor='black', facecolor='lightblue')
ax.add_patch(frame)

# Plot the world map with shades of red and a thin black outline
world.plot(column='Count', ax=ax, legend=False,
           edgecolor='black',  # Add a thin black outline on borders
           linewidth=0.5,      # Set the outline thickness    
           missing_kwds={"color": "lightgrey"})

# Create a background within the frame
ax.set_facecolor('lightblue')  # Set background color within the frame
fig.patch.set_facecolor('white')  # Set background color for the figure


# Add a vertical color bar
sm = plt.cm.ScalarMappable(Normalize(vmin=country_counts['Count'].min(), vmax=country_counts['Count'].max()))
sm._A = []  # Empty array for the ScalarMappable
cbar = fig.colorbar(sm, ax=ax, orientation='vertical', pad=0.02, shrink=0.5)
cbar.set_label('Number of Athletes by Country', fontsize=12)

# Remove the axis for a cleaner look
ax.axis('off')

plt.show()
plt.savefig()