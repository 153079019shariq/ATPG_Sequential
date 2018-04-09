import networkx as nx 
import operator
G = nx.DiGraph()


G.add_node('A',type='input')
G.add_node('B',type='input')
#G.add_node('C',type='input')

G.add_node('1',type='gate',gatetype='and')
G.add_node('2',type='gate',gatetype='xnor')
G.add_node('3',type='gate',gatetype='xnor')
G.add_node('4',type='gate',gatetype='not')
G.add_node('5',type='gate',gatetype='not')
G.add_node('7',type='gate',gatetype='nand')
G.add_node('9',type='gate',gatetype='or')
G.add_node('6',type='gate',gatetype='xor')
G.add_node('8',type='gate',gatetype='nand')

G.add_node('fanout1',type='fanout')
G.add_node('fanout2',type='fanout')
G.add_node('fanout3',type='fanout')
G.add_node('fanout4',type='fanout')
G.add_node('fanout5',type='fanout')
G.add_node('fanout6',type='fanout')

G.add_node('X',type='output')
G.add_node('Z',type='output')
G.add_node('Y',type='output')

G.add_edges_from([('A','1'),('B','fanout1'),('fanout1','1'),('1','fanout3'),('fanout1','fanout2'),('fanout2','2'),('fanout3','2'),('2','fanout4'),('fanout2','6'),
('fanout3','3'),('fanout3','7'),('fanout4','3'),('fanout4','4'),('fanout4','8'),('3','fanout6'),('fanout6','5'),('fanout6','7'),('5','fanout5'),('fanout5','9'),
('fanout5','6'),('4','9'),('6','8'),('7','X'),('9','Y'),('8','Z')
 ], value_non_fault='x',value_faulty='x', fault='',cc0=0,cc1=0,co=0)
#Assigning controllability of PI as 1 
G.add_edge('A', '1', value_non_fault='x',value_faulty='x',fault='',cc0=1,cc1=1,co=0)
G.add_edge('B','fanout1', value_non_fault='x',value_faulty='x',fault='',cc0=1,cc1=1,co=0)





#Fault
G.add_edge('5','fanout5', value_non_fault='x',value_faulty='x',fault='sa1',cc0=1,cc1=1,co=0)



#bfs = sorted(x.items(), key=operator.itemgetter(1))
#print bfs

#~ plt.savefig("check_Graph.png")
#~ plt.ion()
#~ plt.show()
