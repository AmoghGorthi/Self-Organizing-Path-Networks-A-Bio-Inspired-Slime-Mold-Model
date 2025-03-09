import osmnx as ox
import matplotlib.pyplot as plt

# Define a small bounding box for a quick test (a compact area in Downtown SF)
north, south, east, west = 37.7910, 37.7880, -122.4000, -122.4050

# Fetch the road network using OSMnx for driving routes
# OSMnx 2.0.1 requires a tuple for the bounding box with the 'bbox' keyword
G = ox.graph_from_bbox(bbox=(north, south, east, west), network_type="drive")

# Plot the road network
fig, ax = ox.plot_graph(G, show=True, close=True)