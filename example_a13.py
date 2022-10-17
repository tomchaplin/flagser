import networkx as nx
from GrPdFlH import GrPdFlH

flag_path= "./flagser"

G = nx.DiGraph()
H = nx.DiGraph()
for i in range(5):
    G.add_node(i)
for i in range(4):
    H.add_node(i)

G.add_edge(0, 1, weight = 10)
G.add_edge(1, 2, weight = 10)
G.add_edge(2, 3, weight = 10)
G.add_edge(3, 0, weight = 10)
G.add_edge(4, 0, weight = 1)

H.add_edge(0, 1, weight = 10)
H.add_edge(1, 2, weight = 10)
H.add_edge(2, 3, weight = 10)
H.add_edge(3, 0, weight = 10)

print(GrPdFlH(G, flag_path))
print(GrPdFlH(H, flag_path))
