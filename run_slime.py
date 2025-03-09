import osmnx as ox
import matplotlib.pyplot as plt
from slime_mold_optimization import slime_mold_optimization

# 1) Fetch or load the same small bounding box in Downtown SF
north, south, east, west = 37.7910, 37.7880, -122.4000, -122.4050
G = ox.graph_from_bbox(bbox=(north, south, east, west), network_type="drive")

# 2) Run the Slime Mold optimization
pheromone_dict = slime_mold_optimization(
    G,
    iterations=10,
    num_agents=5,
    evaporation_rate=0.1,
    alpha=1.0,
    beta=1.0,
    deposit_amount=1.0
)

# 3) Identify the "strongest" edges
# Let's define a threshold to consider edges as "optimized"
threshold = 2.0
strong_edges = [(u, v, k) for (u, v, k), ph in pheromone_dict.items() if ph > threshold]

# 4) Plot the final network
# We'll highlight strong edges in a different color
edge_colors = []
for u, v, k in G.edges(keys=True):
    if (u, v, k) in strong_edges:
        edge_colors.append("red")  # strong edges in red
    else:
        edge_colors.append("gray")

fig, ax = ox.plot_graph(
    G,
    edge_color=edge_colors,
    show=True,
    close=True
)