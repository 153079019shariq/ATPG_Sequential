
import matplotlib.pyplot as plt
import networkx as nx
from collections import OrderedDict

class MyOrderedDict(OrderedDict):
    def last(self):
        print  "last",list(self.items())[-1]
        return list(self.items())[-1]
    def lastbutone(self):
        print  "lastbutone",list(self.items())[-2]
        return list(self.items())[-2]






def preprocess(G):
    for items in G.nodes(data=True):
        if items[1]['type'] != 'input' and items[1]['cc0'] == 1 and items[1]['cc1'] == 1:
            get_controllability(G, items[0])
            print  items



def get_controllability(G, node):
    if G.node[node]['type'] == 'output' :
       for predecessors in G.predecessors(node):
			print "predecessors",predecessors
			l0 = G.node[predecessors]['cc0']
			l1 = G.node[predecessors]['cc1']
       G.node[node]['cc0'] = l0
       G.node[node]['cc1'] = l1
    else : 
         for incoming in G.predecessors(node):
             if G.node[incoming]['cc0'] == 1 and G.node[incoming]['cc1'] == 1 and G.node[incoming]['type'] != 'input':
               get_controllability(G, incoming)
               l0 = []
               l1 = []
               for predecessors in G.predecessors(node):
                     l0.append(G.node[predecessors]['cc0'])
                     l1.append(G.node[predecessors]['cc1'])

               if G.node[node]['gatetype'] == 'and':
                     G.node[node]['cc0'] = min(l0) + 1
                     G.node[node]['cc1'] = sum(l1) + 1

               elif G.node[node]['gatetype'] == 'nand':
                     G.node[node]['cc0'] = sum(l1) + 1
                     G.node[node]['cc1'] = min(l0) + 1

               elif G.node[node]['gatetype'] == 'or':
                     G.node[node]['cc0'] = sum(l0) + 1
                     G.node[node]['cc1'] = min(l1) + 1

               elif G.node[node]['gatetype'] == 'nor':
                     G.node[node]['cc0'] = min(l1) + 1
                     G.node[node]['cc1'] = sum(l0) + 1

               elif G.node[node]['gatetype'] == 'not':    
                     G.node[node]['cc0'] = sum(l1) + 1
                     G.node[node]['cc1'] = sum(l0) + 1

               elif G.node[node]['gatetype'] == 'xor':
					l2 = []
					l3 = []
					i = 0
					for predecessors in G.predecessors(node):
							  if i % 2 == 0 :
								  l2.append(G.node[predecessors]['cc0'])
								  l3.append(G.node[predecessors]['cc1'])
							  else :
								  l2.append(G.node[predecessors]['cc1'])
								  l3.append(G.node[predecessors]['cc0'])
							  i += 1
					G.node[node]['cc0'] = min(sum(l0), sum(l1)) + 1
					G.node[node]['cc1'] = min(sum(l2), sum(l3)) + 1

               elif G.node[node]['gatetype'] == 'xnor':
					l2 = []
					l3 = []
					i = 0
					for predecessors in G.predecessors(node):
						if i % 2 == 0 :
							l2.append(G.node[predecessors]['cc0'])
							l3.append(G.node[predecessors]['cc1'])
						else :
							l2.append(G.node[predecessors]['cc1'])
							l3.append(G.node[predecessors]['cc0'])
						i += 1
					G.node[node]['cc0'] = min(sum(l2), sum(l3)) + 1
					G.node[node]['cc1'] = min(sum(l0), sum(l1)) + 1




G = nx.DiGraph()
G.add_nodes_from([1, 2, 3], type='input', cc0=1, cc1=1)
G.add_node(4, type='gate', gatetype='and', cc0=1, cc1=1)
G.add_nodes_from([5, 6, 7], type='gate', gatetype='xnor', cc0=1, cc1=1)
G.add_nodes_from([8, 9], type='gate', gatetype='not', cc0=1, cc1=1)
G.add_nodes_from([10, 11], type='gate', gatetype='nand', cc0=1, cc1=1)
G.add_node(12, type='gate', gatetype='or', cc0=1, cc1=1)
G.add_nodes_from([13, 14, 15], type='output', cc0=1, cc1=1)
G.add_edges_from([(1, 4), (2, 4), (2, 6), (2, 7), (3, 11), (4, 10), (4, 5), (4, 6), (5, 8), (5, 10), (6, 5), (6, 9), (6, 11), (7, 11), (8, 7), (9, 12), (10, 13), (11, 15), (12, 14)], value='x', fault='none')
G.add_edge(8, 12, value='x', fault='sa1')
nx.draw_circular(G,with_labels=True)
plt.savefig("check_Graph.png")
plt.ion()
plt.show()
preprocess(G)
#implications = MyOrderedDict()
#print  implications.last()
