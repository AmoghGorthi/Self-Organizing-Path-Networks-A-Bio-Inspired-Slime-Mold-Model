import random
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

from slime_mold_optimization import slime_mold_optimization

# 1) Fetch or load the same small bounding box
north, south, east, west = 37.7910, 37.7880, -122.4000, -122.4050
G = ox.graph_from_bbox(bbox=(north, south, east, west), network_type="drive")

# 2) Run Slime Mold Optimization
pheromone_dict = slime_mold_optimization(
    G,
    iterations=15,
    num_agents=5,
    evaporation_rate=0.1,
    alpha=1.0,
    beta=1.0,
    deposit_amount=1.0
)

# 3) Pick a random start/end node for path comparison
all_nodes = list(G.nodes())
start_node = random.choice(all_nodes)
end_node = random.choice(all_nodes)
while end_node == start_node:
    end_node = random.choice(all_nodes)

print(f"Comparing routes from {start_node} to {end_node}")

# 4) Identify "strong" edges from Slime Mold
threshold = 2.0
strong_edges = [(u, v, k) for (u, v, k), ph in pheromone_dict.items() if ph > threshold]

# Convert strong edges to a path-like sequence (greedy approach)
# NOTE: This is a simplistic way to pick a path from strong edges.
slime_path_nodes = [start_node]
current_node = start_node
while current_node != end_node:
    neighbors = list(G.successors(current_node))
    # Filter neighbors that are in strong_edges
    strong_neighbors = []
    for nbr in neighbors:
        key = 0  # assume key=0
        if (current_node, nbr, key) in strong_edges:
            strong_neighbors.append(nbr)
    if not strong_neighbors:
        break
    current_node = strong_neighbors[0]  # pick first strong neighbor
    slime_path_nodes.append(current_node)
    
print("Slime mold path (approx):", slime_path_nodes)

# 5) Dijkstra’s Path
dijkstra_path_nodes = nx.shortest_path(G, source=start_node, target=end_node, weight='length')
print("Dijkstra's path:", dijkstra_path_nodes)

# 6) A* Path
a_star_path_nodes = nx.astar_path(G, start_node, end_node, heuristic=None, weight='length')
print("A* path:", a_star_path_nodes)

# 7) Plot All Paths
# First, create a function to convert node-path to edge list
def nodes_to_edges(path):
    return list(zip(path[:-1], path[1:], [0]*(len(path)-1)))  # key=0

slime_edges = nodes_to_edges(slime_path_nodes)
dijkstra_edges = nodes_to_edges(dijkstra_path_nodes)
astar_edges = nodes_to_edges(a_star_path_nodes)

edge_colors = []
for u, v, k in G.edges(keys=True):
    if (u, v, k) in slime_edges:
        edge_colors.append("red")       # Slime path
    elif (u, v, k) in dijkstra_edges:
        edge_colors.append("blue")      # Dijkstra
    elif (u, v, k) in astar_edges:
        edge_colors.append("green")     # A*
    else:
        edge_colors.append("gray")

fig, ax = ox.plot_graph(G, edge_color=edge_colors, show=True, close=True)