import networkx as nx
import matplotlib.pyplot as plt
# Step 1: Represent a small road network as a graph (adjacency list)
# Notice 'Mumbai' and 'Pune' are connected to each other, but NOT to the rest of the map.
city_graph = {
  'Kolkata': ['Durgapur', 'Andul'],
  'Durgapur': ['Kolkata', 'Barasat'],
  'Andul': ['Kolkata', 'Dhanbad'],
  'Barasat': ['Durgapur'],
  'Dhanbad': ['Andul', 'Ranchi'],
  'Ranchi': ['Dhanbad'],
  'Mumbai': ['Bangalore'],
  'Bangalore': ['Mumbai']
}

# Step 2: DFS function that checks if a path exists between two cities
def dfs_path_exists(graph, current_city, destination_city, visited=None):
  if visited is None:
    visited = set()
  visited.add(current_city)
  if current_city == destination_city:
    return True
  if current_city not in graph:      # <-- guard added
    return False
  for neighbour_city in graph[current_city]:
    if neighbour_city not in visited:
      if dfs_path_exists(graph, neighbour_city, destination_city, visited):
        return True
  return False

# Step 3: DFS function that returns the full visited order (for connected components)
def dfs_traversal(graph, start_city, visited=None):
    if visited is None:
        visited = set()
    order = []
    visited.add(start_city)
    order.append(start_city)
    for neighbour_city in graph[start_city]:
      if neighbour_city not in visited:
        order.extend(dfs_traversal(graph, neighbour_city, visited))
    return order

# Step 4: Test whether a route exists between different city pairs
pairs_to_check = [('Kolkata', 'Ranchi'), ('Kolkata', 'Mumbai'), ('Bankura', 'Dhanbad'), ('Kolkata','Mumbai')]
print("Checking whether a road route exists between cities using DFS:\n")
for city_a, city_b in pairs_to_check:
  result = dfs_path_exists(city_graph, city_a, city_b)
  status = "YES, a route exists" if result else "NO route exists"
  print(f" {city_a} -> {city_b} ? {status}")

# Step 5: Find all separate (disconnected) groups of cities using DFS
print("\nFinding all separate groups of connected cities:")
all_cities = list(city_graph.keys())
visited_overall = set()
group_number = 1
for city in all_cities:
  if city not in visited_overall:
    group = dfs_traversal(city_graph, city, visited_overall)
    print(f" Group {group_number}: {group}")
    group_number += 1

# Step 6: Draw the map
G = nx.Graph()
for city, neighbours in city_graph.items():
  for n in neighbours:
    G.add_edge(city, n)

plt.figure(figsize=(7, 5.5))
pos = nx.spring_layout(G, seed=11, k=1.6)
nx.draw(G, pos, with_labels=True, node_color='#F9E79F', node_size=1900,
font_size=12, font_weight='bold', edge_color='#7D6608', width=2)
plt.title("City Road Network used in Problem 3")
plt.savefig("city-graph.png")
print("Saved succesfully!")