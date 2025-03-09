import time
import statistics
from slime_mold_optimization import slime_mold_optimization

def measure_slime_metrics(G, iterations=10, num_agents=5, evaporation_rate=0.1, alpha=1.0, beta=1.0, deposit_amount=1.0, strong_threshold=2.0):
    start_time = time.time()
    pheromone = slime_mold_optimization(G, iterations, num_agents, evaporation_rate, alpha, beta, deposit_amount)
    simulation_time = time.time() - start_time
    strong_edges_count = sum(1 for ph in pheromone.values() if ph > strong_threshold)
    avg_pheromone = sum(pheromone.values()) / len(pheromone)
    pheromone_values = list(pheromone.values())
    std_dev_pheromone = statistics.stdev(pheromone_values) if len(pheromone_values) > 1 else 0.0
    return {"simulation_time": simulation_time, "strong_edges_count": strong_edges_count, "average_pheromone": avg_pheromone, "pheromone_std_dev": std_dev_pheromone}

if __name__ == '__main__':
    import osmnx as ox
    north, south, east, west = 37.7910, 37.7880, -122.4000, -122.4050
    G = ox.graph_from_bbox(bbox=(north, south, east, west), network_type="drive")
    metrics = measure_slime_metrics(G, iterations=10, num_agents=5, evaporation_rate=0.1, alpha=1.0, beta=1.0, deposit_amount=1.0, strong_threshold=2.0)
    print("=== Slime Mold Metrics ===")
    print("Simulation Time (seconds):", metrics["simulation_time"])
    print("Number of Strong Edges:", metrics["strong_edges_count"])
    print("Average Pheromone Level:", metrics["average_pheromone"])
    print("Pheromone Standard Deviation:", metrics["pheromone_std_dev"])