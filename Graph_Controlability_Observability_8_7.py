import networkx as nx 
import networkx as nz
import operator
G = nx.DiGraph()
G.add_node('A',type='input',op_type='Primary_ip')
G.add_node('B',type='input',op_type='Primary_ip')
G.add_node('C',type='input',op_type='Primary_ip')
G.add_node('D',type='input',op_type='Primary_ip')


G.add_node('fanout1',type='fanout')
G.add_node('fanout2',type='fanout')



G.add_node('G1',type='gate',gatetype='and')
G.add_node('G2',type='gate',gatetype='nor')
G.add_node('G3',type='gate',gatetype='or')
G.add_node('G4',type='gate',gatetype='or')


G.add_node('FF1',type='FF')


G.add_node('output1',type='output',op_type='Primary_op')
G.add_node('output2',type='output',op_type='Primary_op')


G.add_edges_from([('G1','fanout1'),('fanout1','G2'),('fanout1','FF1'),('FF1','G4'),('G2','fanout2'),('fanout2','G3'),('fanout2','G4'),
					('G3','output1'),('G4','output2')], value_non_fault='x',value_faulty='x', fault='',cc0=0,cc1=0,dr1_0=10000,dr0_1=10000)


G.add_edge('A','G1', value_non_fault='x',value_faulty='x',fault='',cc0=4,cc1=4, dr1_0=10000,dr0_1=10000)
G.add_edge('B','G1', value_non_fault='x',value_faulty='x',fault='',cc0=6,cc1=4, dr1_0=10000,dr0_1=10000)
G.add_edge('C','G2', value_non_fault='x',value_faulty='x',fault='',cc0=10,cc1=15,dr1_0=10000,dr0_1=10000)
G.add_edge('D','G3', value_non_fault='x',value_faulty='x',fault='',cc0=11,cc1=16,dr1_0=10000,dr0_1=10000)



G.add_edge('A','G1', value_non_fault='x',value_faulty='0',fault='sa1',dr1_0=10000,dr0_1=10000)


def print_Graph(Graph):
	print "OUTPUT NODE"
	for i in  Graph.edges(data=True):
		if(Graph.nodes[i[1]]['type']=='output'):
			print i
	print "INPUT NODE"
	for i in  Graph.edges(data=True):
		if(Graph.nodes[i[0]]['type']=='input'):
			print i
	print "GATE"		
	for i in  Graph.edges(data=True):
		if(Graph.nodes[i[0]]['type']=='gate'):
			print i
	print "FANOUT"	
	for i in  Graph.edges(data=True):
		if(Graph.nodes[i[1]]['type']=='fanout'):
			print i
	for i in  Graph.edges(data=True):
		if(Graph.nodes[i[0]]['type']=='fanout'):
			print i
			
			
def print_Graph_nodes(Graph):
	for i in Graph.nodes(data=True):
			print i

#-----------------------------------------------Levelization of the Graph-------------------------------------------------------------------------



def assign(lis,dic):
	flag=0
	for k in lis:
			  	if(k in dic.keys()):
					continue
				else:
					flag=1
					break
	return flag

def maxi(lis,dic):
	maxim=0
	for i in lis:
		if(maxim <dic[i]):
			maxim =dic[i]
	return maxim





def Level (Graph):
	global dic_level
	dic_level={}
	#print Graph.nodes(data=True)
	for item in Graph.nodes():
		
		
		if(Graph.nodes[item]['type']=='input' ):
			dic_level[item]=1
	#print "Length of Graph",len(Graph)
	while (len(dic_level)<len(Graph)):	
		for item in Graph.nodes():
			if(Graph.nodes[item]['type']=='fanout' or Graph.nodes[item]['type']=='FF'):
				list_inedge =list(Graph.in_edges(nbunch=item, data=False))
				if(list_inedge[0][0] in dic_level.keys()):	
					dic_level[item]=dic_level[list_inedge[0][0]]+1
			elif(Graph.nodes[item]['type']=='output'):
				list_inedge =list(Graph.in_edges(nbunch=item, data=False))
				if(list_inedge[0][0] in dic_level.keys()):	
					dic_level[item]=dic_level[list_inedge[0][0]]
				
			elif(Graph.nodes[item]['type']=='gate'):
				list_inedge =list(Graph.in_edges(nbunch=item, data=False))	
				lis=[]
				lis =[i[0] for i in list_inedge]
				if(assign(lis,dic_level) ==0):
					dic_level[item] =maxi(lis,dic_level)+1
				else:
					continue
				#dic_level[item]=maxi
	return dic_level
#---------------------------------------------------------------------------------------------------------------------------------------	

bfs= Level (G)
print bfs
sorted_x = sorted(bfs.items(), key=operator.itemgetter(1))

list1=[]
def lis(sorted_x):
	global list1
	
	for i in sorted_x:
		list1.append(i[0])
		
lis(sorted_x)



