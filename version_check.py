import osmnx as ox
import networkx as nx
import matplotlib
import numpy as np
import pyrosm
import pandas as pd
import geopandas as gpd

print("OSMnx version:", ox.__version__)
print("NetworkX version:", nx.__version__)
print("Matplotlib version:", matplotlib.__version__)
print("NumPy version:", np.__version__)

try:
    print("Pyrosm version:", pyrosm.__version__)
except AttributeError:
    print("Pyrosm version: Not available")
    
print("Pandas version:", pd.__version__)
print("GeoPandas version:", gpd.__version__)