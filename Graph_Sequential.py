import networkx as nx 
import networkx as nz

G = nx.DiGraph()
G.add_node('A',type='input')
G.add_node('B',type='input')


G.add_node('fanout1',type='fanout')
G.add_node('fanout2',type='fanout')
G.add_node('fanout3',type='fanout')


G.add_node('G1',type='gate',gatetype='or')
G.add_node('G2',type='gate',gatetype='nand')
G.add_node('G3',type='gate',gatetype='not')
G.add_node('G4',type='gate',gatetype='or')




G.add_node('FF1',type='FF')
G.add_node('FF2',type='FF')
G.add_node('FF3',type='FF')

G.add_node('output1',type='output')


G.add_edges_from([('A', 'fanout1'),('fanout1', 'G1'),('fanout1','G3'),('B','FF1'),('FF1','fanout2'),('fanout2','G2'),('fanout2','G1'),
					('G1','FF2'),('FF2','G2'),('G2','fanout3'),('fanout3','G4'),('fanout3','FF3'),('FF3','G4'),('G3','G4'),('G4','output1')
						], value_non_fault='x',value_faulty='x', fault='')

G.add_edge('fanout1','G1', value_non_fault='x',value_faulty='x',fault='sa0')




def print_Graph(Graph):
	for i in  Graph.edges(data=False):
		print i

def print_Graph_nodes(Graph):
	for i in Graph.nodes():
		if(Graph.nodes[i]['type']=='FF_ip'):
			print i

#####################################################################################################################################
#------------------------------------------------------------Loop Unrolling--------------------------------------------------------------------

print G.nodes(data=False)
print G.edges(data=False)



GU = nx.DiGraph()
GU=G.copy()



print "########################################################################################"	
for i in  G.edges:
	if(G.nodes[i[0]]['type']=='FF'):
		#print i
		GU.remove_edge(i[0], i[1])
		GU.add_edge(i[0]+"_op", i[1],value_non_fault='x',value_faulty='x', fault='')
	if(G.nodes[i[1]]['type']=='FF'):
		#print i
		GU.remove_edge(i[0], i[1])
		GU.add_edge(i[0], i[1]+"_ip",value_non_fault='x',value_faulty='x', fault='')
print "########################################################################################"	





for i in G.nodes: 
	if(G.nodes[i]['type']=='FF'):
		GU.remove_node(i)
		GU.add_node((i + "_ip"),type='FF_ip')
		GU.add_node((i + "_op"),type='FF_op')
		
#print_Graph(GU)
###############################################################################################################################		

#~ 
#~ 

def Total_Graph(Graph,No_of_Unroll):
	dic={}
	global GUZ
	for j in range(No_of_Unroll):
		
		for i in Graph.nodes(data=False):
			dic[i] =i+"_"+str(j)
			H=nx.relabel_nodes(GU, dic)
		if(j==0):
			GUZ =H.copy()
		else:
			GUZ = nx.compose(GUZ,H)
	print "##########################################################"
	#print_Graph(GUZ)	
	
	
	#Output of FF is the previous cycle input 
	Connect_FF_op_FF_ip(GUZ,No_of_Unroll)
	

		
def Connect_FF_op_FF_ip(Graph,No_of_Unroll):
	list_ip_FF=[]
	list_op_FF=[]
	
	for i in Graph.node(data= False):
			if(Graph.nodes[i]['type']=='FF_ip'):
				
				if(int(i[len(i)-1])<No_of_Unroll-1 and int(i[len(i)-1])>=0):
					list_ip_FF.append(i)
					
			if(Graph.nodes[i]['type']=='FF_op'):
				if(int(i[len(i)-1])<No_of_Unroll and int(i[len(i)-1])>0):
					list_op_FF.append(i)
					
	
	
	#print "Graph Adding edge between FF_in in previous cycle and FF o/p "
	for i in range(len(list_ip_FF)):
	
		
			list_inedge =list(Graph.in_edges(nbunch=list_ip_FF[i], data=False))[0]
		
			Graph.remove_edge(list_inedge[0], list_inedge[1])
			Graph.remove_node(list_inedge[1])
			k=int(list_inedge[1][len(list_inedge[1])-1])
			
			j=list_inedge[1][0:3]+"_"+"op"+"_"+str(k+1)
			
			list_outedge =list(Graph.out_edges(nbunch=j, data=False))[0]
			Graph.remove_edge(list_outedge[0], list_outedge[1])
			Graph.remove_node(list_outedge[0])
			
		
			Graph.add_edge(list_inedge[0], list_outedge[1],value_non_fault='x',value_faulty='x', fault='')
			
		#----------Adding edge between FF_in in previous cycle and FF o/p
		
	#print_Graph(Graph)
	
	

		
No_of_Unroll=7
Total_Graph(GU,No_of_Unroll)
		
#print_Graph_nodes(GUZ)
#print_Graph(GUZ)


#Dummy node for bfs
#~ GU.add_node('PI',type='check')
#~ for i in GU.nodes:
	#~ if(GU.nodes[i]['type']=='input'or GU.nodes[i]['type']=='FF_op'):
		#~ GU.add_edge('PI',i, value_non_fault='x',value_faulty='x',fault='')
		#~ 
#~ bfs=nx.single_source_shortest_path_length(GU,'PI')
#bfs	=list(nx.dfs_edges(GU,'PI'))

#heaviest_path = max(path for path in nx.all_simple_paths(GUZ, 'PI', 'output1_1'),key=lambda path: get_weight(path))

print "***********************************"





def check_path(Source,Destination):
	for path in nx.all_simple_paths(GUZ, source=Source, target=Destination):
			#print path
			return True
			
def check_path_op(Source):
	for item in GUZ.nodes(data=True):
		
		if(item[1]['type']=='output'):
			if(check_path(Source,item[0])==True):
				return True


def faulty_edg(G):
	stuck_at_list=[]	
	faulty_node1_list=[]
	faulty_node2_list=[]							
	for item in G.edges(data=True):
				
		if(item[2]['fault']=='sa1' ):
			if(check_path_op(item[1])==True):
				stuck_at_list.append('sa1')
				faulty_node1_list.append(item[0])
				faulty_node2_list.append(item[1])			
		elif(item[2]['fault']=='sa0'):
			if(check_path_op(item[1])==True):
				stuck_at_list.append('sa1')
				faulty_node1_list.append(item[0])
				faulty_node2_list.append(item[1])
	#print stuck_at_list
	#print faulty_node1_list
	#print faulty_node2_list	
#	return [faulty_node1,faulty_node2,stuck_at]

faulty_edg(GUZ)

#----------------------------------------------------------------------------------------------------------------------------------------------





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
	for item in Graph.nodes():
		#print item,Graph.nodes[item]['type']
		
		if(Graph.nodes[item]['type']=='input' or Graph.nodes[item]['type']=='FF_op'):
			dic_level[item]=1
	print "Length of Graph",len(Graph)
	while (len(dic_level)<len(Graph)):	
		for item in Graph.nodes():		
			if(Graph.nodes[item]['type']=='fanout' or Graph.nodes[item]['type']=='FF_ip'):
				list_inedge =list(Graph.in_edges(nbunch=item, data=False))
				if(list_inedge[0][0] in dic_level.keys()):	
					dic_level[item]=dic_level[list_inedge[0][0]]+1
			elif(Graph.nodes[item]['type']=='FF_ip' or Graph.nodes[item]['type']=='output'):
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
bfs = Level (GUZ)
#print "bfs",bfs
