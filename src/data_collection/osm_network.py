import osmnx as ox
import networkx as nx
import geopandas as gpd
from shapely.geometry import Point, box

def extract_road_network(bbox_coords: list, network_type: str = 'drive'):
    """
    Extracts road network from OpenStreetMap for a given bounding box.
    bbox_coords: [north, south, east, west]  (Note osmnx expects N, S, E, W)
    """
    try:
        north, south, east, west = bbox_coords
        # Download the graph
        G = ox.graph_from_bbox(north, south, east, west, network_type=network_type)
        print(f"Extracted road network with {len(G.nodes)} nodes and {len(G.edges)} edges.")
        return G
    except Exception as e:
        print(f"Error extracting road network: {e}")
        return nx.MultiDiGraph()

def identify_competing_routes(G: nx.MultiDiGraph, origin_coords: tuple, dest_coords: tuple):
    """
    Finds the shortest path and alternative paths between origin and destination.
    Useful for assessing traffic risk (if competing toll-free routes exist).
    origin_coords: (lat, lon)
    dest_coords: (lat, lon)
    """
    if len(G) == 0:
        return []

    try:
        # Find nearest nodes to the coordinates
        orig_node = ox.distance.nearest_nodes(G, X=origin_coords[1], Y=origin_coords[0])
        dest_node = ox.distance.nearest_nodes(G, X=dest_coords[1], Y=dest_coords[0])

        # Shortest path by travel time (assuming edge weights are computed, otherwise length)
        # Using length here as default
        shortest_path = nx.shortest_path(G, orig_node, dest_node, weight='length')
        
        # In a more advanced implementation, use Yen's k-shortest paths
        # or penalize the shortest path to find viable alternatives.
        
        # Simple placeholder for alternatives
        # alt_paths = list(nx.shortest_simple_paths(G, orig_node, dest_node, weight='length'))[:3]
        
        return [shortest_path]
    except nx.NetworkXNoPath:
        print("No path found between origin and destination.")
        return []
    except Exception as e:
        print(f"Error finding routes: {e}")
        return []

def compute_accessibility_score(G: nx.MultiDiGraph, location: tuple, radius_km: float = 5.0):
    """
    Computes a simple accessibility score for a location based on road network density.
    location: (lat, lon)
    """
    if len(G) == 0:
        return 0.0

    # Project graph to UTM for accurate distance measurements
    try:
        G_proj = ox.project_graph(G)
        
        # Get point geometry and project it
        pt = gpd.GeoSeries([Point(location[1], location[0])], crs="EPSG:4326")
        pt_proj = pt.to_crs(G_proj.graph['crs']).iloc[0]
        
        # Create a buffer (radius)
        buffer = pt_proj.buffer(radius_km * 1000) # meters
        
        # Count nodes/edges within buffer as a proxy for accessibility/connectivity
        # A more robust metric would be calculating isochrones (travel time polygons).
        nodes_gdf, edges_gdf = ox.graph_to_gdfs(G_proj)
        
        edges_within = edges_gdf[edges_gdf.intersects(buffer)]
        
        # Score = total road length within radius (km)
        total_road_length_m = edges_within['length'].sum()
        score = total_road_length_m / 1000.0
        
        return score
    except Exception as e:
        print(f"Error computing accessibility score: {e}")
        return 0.0

if __name__ == "__main__":
    # Example usage for a small area in San Francisco
    # bbox = [37.8, 37.7, -122.4, -122.5] # N, S, E, W
    # G = extract_road_network(bbox)
    pass
