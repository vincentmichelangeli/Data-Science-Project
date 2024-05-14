from clustering import final_clustering
from age_distribution import plot_distribution
from age_distribution import plot_progression

final_clustering('Men')
final_clustering('Women')

plot_progression('Men')
plot_progression('Women')

plot_distribution('Men')
plot_distribution('Women')