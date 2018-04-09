import networkx as nx 
G = nx.DiGraph()
G.add_node('A',type='input')
G.add_node('B',type='input')
G.add_node('C',type='input')
G.add_node('D',type='input')
G.add_node('E',type='input')
G.add_node('F',type='input')

G.add_node('fanout1',type='fanout')
G.add_node('fanout2',type='fanout')
G.add_node('fanout3',type='fanout')
G.add_node('fanout4',type='fanout')
G.add_node('fanout5',type='fanout')
G.add_node('fanout6',type='fanout')
G.add_node('fanout7',type='fanout')


G.add_node('G1',type='gate',gatetype='nand')
G.add_node('G2',type='gate',gatetype='nand')
G.add_node('G3',type='gate',gatetype='nand')
G.add_node('G5',type='gate',gatetype='nand')
G.add_node('G7',type='gate',gatetype='nand')
G.add_node('G8',type='gate',gatetype='nand')
G.add_node('G9',type='gate',gatetype='nand')
G.add_node('G10',type='gate',gatetype='nand')

G.add_node('G11',type='gate',gatetype='not')
G.add_node('G12',type='gate',gatetype='not')
G.add_node('G13',type='gate',gatetype='not')



G.add_node('output1',type='output')


G.add_edges_from([('A', 'fanout1'),('fanout1', 'G1'),('fanout1','G2'),('B','fanout2'),('fanout2','G1'),('fanout2','G3'),('C','fanout3'),('fanout3','G1'),
('fanout3','G8'),('G1','fanout4'),('fanout4','G5'),('fanout4','G7'),('fanout4','G9'),('D','fanout5'),('fanout5','G11'),('fanout5','G5'),('G11','G2'),
('E','fanout6'),('fanout6','G12'),('fanout6','G7'),('G12','G3'),('F','fanout7'),('fanout7','G13'),('fanout7','G9'),('G13','G8'),('G2','G10'),('G10','output1')
,('G5','G10'),('G3','G10'),('G7','G10'),('G8','G10'),('G9','G10')], value_non_fault='x',value_faulty='x', fault='')

G.add_edge('fanout1','G1', value_non_fault='x',value_faulty='x',fault='sa1')


#Dummy node for bfs
G.add_node('PI',type='check')
G.add_edge('PI','A', value_non_fault='x',value_faulty='x',fault='')
G.add_edge('PI','B', value_non_fault='x',value_faulty='x',fault='')
G.add_edge('PI','C', value_non_fault='x',value_faulty='x',fault='')
G.add_edge('PI','D', value_non_fault='x',value_faulty='x',fault='')
G.add_edge('PI','E', value_non_fault='x',value_faulty='x',fault='')
G.add_edge('PI','F', value_non_fault='x',value_faulty='x',fault='')



bfs=nx.single_source_shortest_path_length(G,'PI')
#print bfs




