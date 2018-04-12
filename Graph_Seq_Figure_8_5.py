import networkx as nx 
import networkx as nz

G = nx.DiGraph()
G.add_node('A',type='input',op_type='Primary_ip')



G.add_node('fanout1',type='fanout')
G.add_node('fanout2',type='fanout')


G.add_node('G1',type='gate',gatetype='and')
G.add_node('G2',type='gate',gatetype='or')


G.add_node('FF1',type='FF')
G.add_node('FF2',type='FF')

G.add_node('out1',type='output',op_type='Primary_op')


G.add_edges_from([('A', 'fanout1'),('fanout1','G1'),('fanout1','FF2'),('G1','FF1'),('FF1','fanout2'),('fanout2','G2'),('fanout2','G1'),
					('FF2','G2'),('G2','out1')], value_non_fault='x',value_faulty='x', fault='',cc0=0,cc1=0,co=0)

G.add_edge('A','fanout1', value_non_fault='x',value_faulty='1',fault='sa1',cc0=1,cc1=1,co=0)





#######################################PRINT_Graph###################################################################################

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
		#if(Graph.nodes[i]['type']=='FF_ip'):
			print i















#####################################################################################################################################
#------------------------------------------------------------Loop Unrolling--------------------------------------------------------------------

#print G.nodes(data=False)
#print G.edges(data=False)




def Loop_Unroll_Once(GU):
	
	
	
	
	
	print "########################################################################################"	
	for i in  G.edges:
		if(G.nodes[i[0]]['type']=='FF'):
			#print i
			GU.remove_edge(i[0], i[1])
			GU.add_edge(i[0]+"_op", i[1],value_non_fault='x',value_faulty='x', fault='',cc0=1,cc1=1,co=0)
		if(G.nodes[i[1]]['type']=='FF'):
			#print i
			GU.remove_edge(i[0], i[1])
			GU.add_edge(i[0], i[1]+"_ip",value_non_fault='x',value_faulty='x', fault='',cc0=0,cc1=0,co=0)
	print "########################################################################################"	
	
	
	
	
	
	for i in G.nodes: 
		if(G.nodes[i]['type']=='FF'):
			GU.remove_node(i)
			GU.add_node((i + "_ip"),type='output',op_type='FF_ip')
			GU.add_node((i + "_op"),type='input',op_type='FF_op')
	print "Unrolled_Graph"		
	print_Graph(GU)
	return GU
	
#print "GU",GU.nodes(data=True)
#############################################GUZ_creation(Unrolled graph by dseq+1)##################################################################################		

#~ 
#~ 

def Total_Graph(No_of_Unroll):
	dic={}
	global GUZ
	
	GU = Loop_Unroll_Once(G.copy())
	
	if(No_of_Unroll >1):
		for j in range(No_of_Unroll):
			
			for i in GU.nodes(data=False):
				dic[i] =i+"_"+str(j)
				H=nx.relabel_nodes(GU, dic)
			if(j==0):
				GUZ =H.copy()
			else:
				GUZ = nx.compose(GUZ,H)
		print "##########################################################"
		#Output of FF is the previous cycle input 
		Connect_FF_op_FF_ip(GUZ,No_of_Unroll)
	else:
		
		GUZ=GU
	#print_Graph(GUZ)	
	return GUZ

#-------------------------------Connect the FF i/p to the next time frame FF o/p---------------------------------------		
def Connect_FF_op_FF_ip(Graph,No_of_Unroll):
	list_ip_FF=[]
	list_op_FF=[]
	#print_Graph_nodes(Graph)
	for i in Graph.node(data= False):
			if(Graph.nodes[i]['type']=='output' and Graph.nodes[i]['op_type']=='FF_ip'):
				
				if(int(i[len(i)-1])<No_of_Unroll-1 and int(i[len(i)-1])>=0):
					list_ip_FF.append(i)
					
			if(Graph.nodes[i]['type']=='input' and Graph.nodes[i]['op_type']=='FF_op'):
				print  Graph.nodes[i]['op_type']
				print  i
				if(int(i[len(i)-1])<No_of_Unroll and int(i[len(i)-1])>0):
					list_op_FF.append(i)
					
	
	print "list_ip_FF",sorted(list_ip_FF)
	print "list_op_FF",sorted(list_op_FF)
	#print "Graph Adding edge between FF_in in previous cycle and FF o/p "
	for i in range(len(list_ip_FF)):
	
		
			list_inedge =list(Graph.in_edges(nbunch=list_ip_FF[i], data=False))[0]
		
			Graph.remove_edge(list_inedge[0], list_inedge[1])
			Graph.remove_node(list_inedge[1])
			k=int(list_inedge[1][len(list_inedge[1])-1])
			print k
			j=list_inedge[1][0:3]+"_"+"op"+"_"+str(k+1)
			print j
			list_outedge =list(Graph.out_edges(nbunch=j, data=False))[0]
			print "list_outedge",list_outedge
			Graph.remove_edge(list_outedge[0], list_outedge[1])
			Graph.remove_node(list_outedge[0])
			
		
			Graph.add_edge(list_inedge[0], list_outedge[1],value_non_fault='x',value_faulty='x',cc0=0,cc1=0,co=0,fault='')
			
		#----------Adding edge between FF_in in previous cycle and FF o/p
		
	
	
	

		


		


		







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
			if(Graph.nodes[item]['type']=='fanout'):
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






#overall_Graph_Seq()
