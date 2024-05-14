from clustering import final_clustering
from age_distribution import plot_distribution
from age_distribution import plot_progression
from map_generation import plot_countries
from map_generation import plot_countries_vs_pop

final_clustering('Men')
final_clustering('Women')

plot_progression('Men')
plot_progression('Women')

plot_distribution('Men')
plot_distribution('Women')

world = plot_countries()
plot_countries_vs_pop(world)