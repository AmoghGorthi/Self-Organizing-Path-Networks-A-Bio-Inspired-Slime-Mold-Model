import random
import os
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import imageio

def slime_mold_optimization_animated(
    G,
    iterations=10,
    num_agents=5,
    evaporation_rate=0.1,
    alpha=1.0,
    beta=1.0,
    deposit_amount=1.0,
    out_dir="frames"
):
    # Create frames directory if it doesn't exist
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Initialize pheromone on each edge
    pheromone = {}
    for u, v, k, data in G.edges(keys=True, data=True):
        pheromone[(u, v, k)] = 1.0  # initial pheromone value

    def get_distance(u, v, k):
        return G[u][v][k].get('length', 1.0)

    # Use a counter to save each step as a frame
    frame_count = 0

    # Main loop over iterations
    for iteration in range(iterations):
        # Evaporation step: reduce pheromone on all edges
        for edge in pheromone:
            pheromone[edge] *= (1 - evaporation_rate)
        
        # Capture a frame after evaporation (optional)
        save_pheromone_plot(G, pheromone, frame_count, out_dir, extra_info=f"Iteration {iteration} after evaporation")
        frame_count += 1

        # Each agent explores the graph
        nodes_list = list(G.nodes())
        for agent in range(num_agents):
            start_node = random.choice(nodes_list)
            end_node = random.choice(nodes_list)
            while end_node == start_node:
                end_node = random.choice(nodes_list)
            path_edges = find_path_slime(G, pheromone, start_node, end_node, get_distance, alpha, beta)
            # Reinforce the path: increase pheromone on edges used
            for edge in path_edges:
                pheromone[edge] += deposit_amount

            # Save a frame after each agent's exploration
            save_pheromone_plot(G, pheromone, frame_count, out_dir, extra_info=f"Iter {iteration}, Agent {agent}")
            frame_count += 1
            print(f"Iteration {iteration}, Agent {agent} completed and frame saved.")

    # Create an animated GIF from the saved frames
    create_gif(out_dir)
    print(f"Animation saved as {out_dir}/slime_growth.gif")

def find_path_slime(G, pheromone, start, goal, get_distance, alpha, beta):
    path_edges = []
    current_node = start
    max_steps = 200  # prevent infinite loops
    for _ in range(max_steps):
        if current_node == goal:
            break
        neighbors = list(G.successors(current_node))
        if not neighbors:
            break

        edge_probs = []
        total_prob = 0.0
        for nbr in neighbors:
            key = 0  # assuming one edge per pair
            if (current_node, nbr, key) not in pheromone:
                continue
            ph = pheromone[(current_node, nbr, key)]
            dist = get_distance(current_node, nbr, key)
            weight = (ph ** alpha) * ((1.0 / dist) ** beta)
            edge_probs.append((nbr, key, weight))
            total_prob += weight

        if total_prob == 0:
            break

        r = random.random() * total_prob
        cumulative = 0.0
        chosen_nbr, chosen_key = None, None
        for nbr, key, weight in edge_probs:
            cumulative += weight
            if r <= cumulative:
                chosen_nbr, chosen_key = nbr, key
                break

        if chosen_nbr is not None:
            path_edges.append((current_node, chosen_nbr, chosen_key))
            current_node = chosen_nbr
        else:
            break

    return path_edges

def save_pheromone_plot(G, pheromone, frame_number, out_dir, extra_info=""):
    # Map pheromone to an RGB color: higher pheromone = more red
    edge_colors = []
    for u, v, k in G.edges(keys=True):
        ph = pheromone[(u, v, k)]
        # Scale pheromone value (adjust scale factor as needed)
        red_intensity = min(ph / 5.0, 1.0)
        # White (low pheromone) to red (high pheromone)
        edge_colors.append((1, 1 - red_intensity, 1 - red_intensity))
    
    fig, ax = ox.plot_graph(G, edge_color=edge_colors, show=False, close=False)
    plt.title(f"Frame {frame_number}: {extra_info}")
    frame_path = os.path.join(out_dir, f"frame_{frame_number}.png")
    plt.savefig(frame_path)
    plt.close(fig)

def create_gif(out_dir):
    frames = []
    png_files = sorted([f for f in os.listdir(out_dir) if f.endswith(".png")])
    for png in png_files:
        frame = imageio.imread(os.path.join(out_dir, png))
        frames.append(frame)
    gif_path = os.path.join(out_dir, "slime_growth.gif")
    imageio.mimsave(gif_path, frames, fps=2)  # Increase fps if desired

if __name__ == '__main__':
    # Use a small bounding box for a quick test in Downtown SF
    north, south, east, west = 37.7910, 37.7880, -122.4000, -122.4050
    G = ox.graph_from_bbox(bbox=(north, south, east, west), network_type="drive")
    
    slime_mold_optimization_animated(
        G,
        iterations=10,
        num_agents=5,
        evaporation_rate=0.1,
        alpha=1.0,
        beta=1.0,
        deposit_amount=1.0,
        out_dir="frames"
    )
