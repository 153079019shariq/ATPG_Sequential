import networkx as ny
import networkx as nx
from Graph_Sequential import G

###################################################################S_Graph########################################################################
S = ny.DiGraph()
#print G.nodes(data=True)

def check_path_FF(Source,Destination):
	for path in nx.all_simple_paths(G, source=Source, target=Destination):
			return True


#Finding the number of FF in the circuit
FF_list=[]
for item in G.nodes(data=True):
		if(item[1]['type']=='FF'):
			FF_list.append(item[0])
			S.add_node(item[0],type='FF',level=0)

#print FF_list
			
FF_connected_edges =[]
for i in FF_list:
	for j in FF_list:
		if(i !=j):
			#print i,j,check_path_FF(i,j)
			if (check_path_FF(i,j) ==True ):
				FF_connected_edges.append((i,j))
				S.add_edge(i,j)
#print FF_connected_edges
#print S.edges(data=True)
#print S.nodes(data=True)

for i in S.nodes:
	#print i
	list_inedge =len(list(S.in_edges(nbunch=i, data=False)))
	#print type(list_inedge)
	#S.add_node(item[0],type='FF',level=list_inedge)
	S.nodes[i]['level']=list_inedge	
#print S.nodes(data=True)


def Depth_seq_circuit():
	global S
	depth_seq=0
	for i in S.nodes:
		if(S.nodes[i]['level']>depth_seq):
			depth_seq = S.nodes[i]['level']
	return depth_seq
	
No_of_unroll=0
No_of_unroll= Depth_seq_circuit()+1
#print No_of_unroll
			
#####################################################################################################################################
