import networkx as nx 
G = nx.DiGraph()
G.add_node('G1',type='input')
G.add_node('G2',type='input')
G.add_node('G3',type='input')
G.add_node('G4',type='input')
G.add_node('G5',type='input')
G.add_node('G8',type='gate',gatetype='nand')
G.add_node('G9',type='gate',gatetype='nand')
G.add_node('G12',type='gate',gatetype='nand')
G.add_node('G15',type='gate',gatetype='nand')
G.add_node('G16',type='gate',gatetype='nand')
G.add_node('G17',type='gate',gatetype='nand')
G.add_node('fanout1',type='fanout')
G.add_node('fanout2',type='fanout')
G.add_node('fanout3',type='fanout')
G.add_node('output1',type='output')
G.add_node('output2',type='output')
G.add_edges_from([('G3', 'fanout1'),('G9', 'fanout2'),('G12', 'fanout3'),('G16', 'output1'),('G17', 'output2'),('fanout1', 'G8'),('G4', 'G9'),('fanout2', 'G12'),('G5', 'G15'),('fanout3', 'G16'),('G15', 'G17'),('G1', 'G8'),('fanout1', 'G9'),('G2', 'G12'),('fanout2', 'G15'),('G8', 'G16'),('fanout3', 'G17')], value_non_fault='x',value_faulty='x', fault='')
G.add_edge('G3','fanout1', value_non_fault='x',value_faulty='x',fault='sa1')


#Dummy node for bfs
G.add_node('PI',type='check')
G.add_edge('PI','G1', value_non_fault='x',value_faulty='x',fault='')
G.add_edge('PI','G2', value_non_fault='x',value_faulty='x',fault='')
G.add_edge('PI','G3', value_non_fault='x',value_faulty='x',fault='')
G.add_edge('PI','G4', value_non_fault='x',value_faulty='x',fault='')
G.add_edge('PI','G5', value_non_fault='x',value_faulty='x',fault='')



#bfs=nx.single_source_shortest_path_length(G,'PI')
#print bfs

#print G.nodes(data=True)

print G.edges[('G3', 'fanout1')]['value_faulty']

