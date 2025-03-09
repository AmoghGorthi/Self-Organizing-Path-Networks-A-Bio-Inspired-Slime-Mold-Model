import random
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

def slime_mold_optimization(
    G,
    iterations=10,
    num_agents=5,
    evaporation_rate=0.1,
    alpha=1.0,
    beta=1.0,
    deposit_amount=1.0
):
    """
    A simplified slime mold-inspired algorithm (similar to Ant Colony Optimization).
    
    Parameters:
    -----------
    G : networkx.MultiDiGraph
        The road network graph from OSMnx.
    iterations : int
        Number of times we run the slime mold reinforcement process.
    num_agents : int
        Number of slime agents (like ants) exploring each iteration.
    evaporation_rate : float
        How much pheromone is lost each iteration (0 < evaporation_rate < 1).
    alpha : float
        Weight of current pheromone in edge selection.
    beta : float
        Weight of 1/distance in edge selection.
    deposit_amount : float
        Amount of pheromone deposited on each edge used by an agent.
    """
    
    # 1) Initialize pheromone on each edge
    pheromone = {}
    for u, v, k, data in G.edges(keys=True, data=True):
        pheromone[(u, v, k)] = 1.0  # start all edges at pheromone = 1.0

    # Helper function: get edge distance
    def get_distance(u, v, k):
        # OSMnx stores 'length' in edge attributes
        return G[u][v][k].get('length', 1.0)
    
    # Main iteration loop
    for _ in range(iterations):
        # 2) Evaporation step: reduce pheromone on all edges
        for edge in pheromone:
            pheromone[edge] = (1 - evaporation_rate) * pheromone[edge]

        # 3) Let each agent explore the graph
        nodes_list = list(G.nodes())
        for agent in range(num_agents):
            # Randomly pick start and goal nodes
            start_node = random.choice(nodes_list)
            end_node = random.choice(nodes_list)
            while end_node == start_node:
                end_node = random.choice(nodes_list)

            # Perform a random walk (or a greedy walk) from start to end
            path_edges = find_path_slime(
                G, pheromone, start_node, end_node, get_distance, alpha, beta
            )

            # 4) Reinforce edges used by this agent
            for edge in path_edges:
                pheromone[edge] += deposit_amount

    # After all iterations, return the updated pheromone dictionary
    return pheromone

def find_path_slime(G, pheromone, start, goal, get_distance, alpha, beta):
    """
    Find a path from 'start' to 'goal' using a slime-inspired probabilistic approach.
    Returns a list of edges used in the path.
    """
    path_edges = []
    current_node = start
    
    # To avoid infinite loops, we set a max steps limit
    max_steps = 200

    for _ in range(max_steps):
        if current_node == goal:
            break
        
        neighbors = list(G.successors(current_node))
        if not neighbors:
            # No outgoing edges - dead end
            break

        # Compute probabilities for each neighbor
        edge_probabilities = []
        total_prob = 0.0
        
        for nbr in neighbors:
            # Each edge can have multiple 'keys' if the graph is MultiDiGraph
            # We'll assume key=0 for simplicity or pick the first edge if multiple
            key = 0
            if (current_node, nbr, key) not in pheromone:
                # If missing, skip or treat as minimal pheromone
                continue

            ph = pheromone[(current_node, nbr, key)]
            dist = get_distance(current_node, nbr, key)
            # Probability weight = (pheromone^alpha) * ((1/dist)^beta)
            weight = (ph ** alpha) * ((1.0 / dist) ** beta)
            edge_probabilities.append((nbr, key, weight))
            total_prob += weight

        if total_prob == 0:
            # Can't move further if no edges have any weight
            break

        # Pick the next neighbor based on these probabilities
        r = random.random() * total_prob
        cumulative = 0.0
        chosen_nbr, chosen_key = None, None
        for nbr, key, w in edge_probabilities:
            cumulative += w
            if r <= cumulative:
                chosen_nbr, chosen_key = nbr, key
                break
        
        # If we found a valid next node, update path and move on
        if chosen_nbr is not None:
            path_edges.append((current_node, chosen_nbr, chosen_key))
            current_node = chosen_nbr
        else:
            break

    return path_edges