#The faulty and non fault output are computed seperately.The value to the faulty is assigned only when it is neither sa0 nor sa1. 


import Gates
import operator
#from Graph_Abramovici import G,bfs
#from Time_frame import  GU as G,bfs
import Implication_Stack as IS
from  Controlability_Observability import *
PO_list =[]
def primary_input():
	global G
	global PI_list
	PI_list= []
	for item in G.nodes(data=True):
		
		if(item[1]['type']=='input'):
				list_outedge =list(G.out_edges(nbunch=item[0], data=False))	
				PI_list.append(list_outedge[0])
	return PI_list

	
def primary_output():
	global PO_list
	PO_list= []
	for item in G.nodes(data=True):
		if(item[1]['type']=='output'):
				list_outedge =list(G.in_edges(nbunch=item[0], data=False))	
				PO_list.append(list_outedge[0])
	
	
	
def Forward_Implication_fanout(node1,node2,list_outedge):
	
	#print "@@@@@@@@@Forward Implication Fanout"
	global G
	#print "node1 node2",node1,node2,G[node1][node2]['value_non_fault'],G[node1][node2]['value_faulty']	

	for i in range(len(list_outedge)):
	
		G.edges[list_outedge[i]]['value_non_fault']  = G[node1][node2]['value_non_fault']
		if(G.edges[list(list_outedge[i])]['fault']=='sa0'):  		
		#Assign the computed value only if the edge is neither sao nor sa1
			G.edges[list(list_outedge[i])]['value_faulty']    ='0'
		elif(G.edges[list(list_outedge[i])]['fault']=='sa1'):
			G.edges[list(list_outedge[i])]['value_faulty']    ='1'
		else:
			G.edges[list(list_outedge[i])]['value_faulty']	=G[node1][node2]['value_faulty']
			
		new_node1		=list_outedge[i][0]
		new_node2		=list_outedge[i][1]
		
		if(G.nodes[new_node2]['type']=='gate' or G.nodes[new_node2]['type']=='fanout'):
			Forward_Implication(new_node1,new_node2)
		
		new_node1	= node1
		new_node2	= node2
	
def Forward_Implication_gates(node1,node2):
	#print "@@@@@@@@@Forward Implication Gates"
	global G
	#print "node1 node2",node1,node2,G[node1][node2]['value_non_fault'],G[node1][node2]['value_faulty']	
	list_inedge =list(G.in_edges(nbunch=node2, data=False))
	list_input_non_faulty =[]
	list_input_faulty	  =[]	
	for i in range(len(list_inedge)):
		list_input_non_faulty.append(G.edges[list_inedge[i]]['value_non_fault'])
		list_input_faulty.append(G.edges[list_inedge[i]]['value_faulty'])
	
	if(G.nodes[node2]['gatetype']=='and'):
		output_non_faulty = Gates.AND_gate(list_input_non_faulty)
		output_faulty	  = Gates.AND_gate(list_input_faulty)
	elif(G.nodes[node2]['gatetype']=='or'):
		output_non_faulty =	Gates.OR_gate(list_input_non_faulty)
		output_faulty	  =	Gates.OR_gate(list_input_faulty)
	elif(G.nodes[node2]['gatetype']=='nand'):
		output_non_faulty =	Gates.NAND_gate(list_input_non_faulty)
		output_faulty	  = Gates.NAND_gate(list_input_faulty)
	elif(G.nodes[node2]['gatetype']=='nor'):
		output_non_faulty =	Gates.NOR_gate(list_input_non_faulty)
		output_faulty      =Gates.NOR_gate(list_input_faulty)
	elif(G.nodes[node2]['gatetype']=='xor'):
		output_non_faulty =	Gates.XOR_gate(list_input_non_faulty)
		output_faulty      =Gates.XOR_gate(list_input_faulty)
	elif(G.nodes[node2]['gatetype']=='xnor'):
		output_non_faulty =	Gates.XNOR_gate(list_input_non_faulty)
		output_faulty      =Gates.XNOR_gate(list_input_faulty)
	elif(G.nodes[node2]['gatetype']=='not'):
		output_non_faulty =	Gates.NOT_gate(list_input_non_faulty[0])
		output_faulty	  = Gates.NOT_gate(list_input_faulty[0])
		#print "OUTPUT",output_non_faulty
	#Assign the value_non_fault to the output_non_faulty nodes
	
	G.edges[list(G.out_edges(nbunch=node2, data=False))[0]]['value_non_fault'] =output_non_faulty 
			
	#print "faulty_edge_list[:2]",faulty_edge_list[:2]
	#print "list(list(G.out_edges(nbunch=node2, data=False))[0]",list(list(G.out_edges(nbunch=node2, data=False))[0])
	edge_assign	=list(G.out_edges(nbunch=node2, data=False))[0]	
	if(G.edges[edge_assign]['fault']=='sa0'):  		
		#Assign the computed value only if the edge is neither sao nor sa1
		G.edges[edge_assign]['value_faulty']    ='0'
	elif(G.edges[edge_assign]['fault']=='sa1'):
		G.edges[edge_assign]['value_faulty']    ='1'
	else:
		G.edges[edge_assign]['value_faulty']	=output_faulty
	
		
	node1 =list(G.out_edges(nbunch=node2, data=False))[0][0]
	node2 =list(G.out_edges(nbunch=node2, data=False))[0][1]
	#print "node1 node2",node1,node2
	if(G.nodes[node2]['type']!='output'):		#Check whether Fault Propagated to Primary output_non_faulty
		Forward_Implication(node1,node2)																	   


def Forward_Implication(node1,node2):
	
	list_outedge =list(G.out_edges(nbunch=node2, data=False))				#Checking the forward implication of node2 as node1 is the Primary input

	
	if(G.nodes[node2]['type']=='fanout'):
		Forward_Implication_fanout(node1,node2,list_outedge)
	elif(G.nodes[node2]['type']=='gate'):
		Forward_Implication_gates(node1,node2)
		
		 
	

def Objective():
		global G
		global D_fronteir_list
		print  "D_fronteir_list",D_fronteir_list
		
		if(G[faulty_edge_list[0]][faulty_edge_list[1]]['value_non_fault']=='x'):	#Sensitize the fault
			if(faulty_edge_list[2]=='sa1'):									# if sa1 then it should have value_non_fault of 0
				G[faulty_edge_list[0]][faulty_edge_list[1]]['value_non_fault']='0'
				G[faulty_edge_list[0]][faulty_edge_list[1]]['value_faulty']   ='1'
				
				
			elif(faulty_edge_list[2]=='sa0'):								# if sa0 then it should have value_non_fault of 1
				G[faulty_edge_list[0]][faulty_edge_list[1]]['value_non_fault']='1'
				G[faulty_edge_list[0]][faulty_edge_list[1]]['value_faulty']   ='0'
			
			
			D_fronteir_list.append(faulty_edge_list[1])
			return  faulty_edge_list[0],faulty_edge_list[1]
			
											#Enable the propagation ofthe fault by assigning them non controling values
			
		D_fronteir_list= D_fronteir()	
		D_fronteir_list	=	sort_D_fronteir(D_fronteir_list)
		print "D_fronteir_list",D_fronteir_list
		gate_ip_edge = undefined_ip(D_fronteir_list[0][0])
		
		
		
		
		
		return gate_ip_edge
				



def sort_D_fronteir(D_fronteir_list):			#Found the bfs(to levelise the circuit) and choose the D_fronteir nearest to the output
		print "sort_D_fronteir"
		D_fronteir_level ={}
		for i in D_fronteir_list:
			gate_out_edge = list(G.out_edges(nbunch=i, data=False))
			print gate_out_edge
			D_fronteir_level[i]=G.edges[gate_out_edge[0]]['co']
		
		D_fronteir_level_sorted = sorted(D_fronteir_level.items(), key=operator.itemgetter(1))
		return 	D_fronteir_level_sorted
		
		
		


def D_fronteir():
	
	D_fronteir_li	=[]
	for i in G.nodes:
		flag1 =False
		flag2 =False
		if(G.nodes[i]['type']=='gate'):
			#print "ioaefjpeiofljpowef'''''"
			gate_op_edge = list(G.out_edges(nbunch=i, data=False))
			gate_ip_edge = list(G.in_edges(nbunch=i, data=False))
			
			if(G.edges[gate_op_edge[0]]['value_non_fault']=='x' or G.edges[gate_op_edge[0]]['value_faulty']=='x'):		#Output is 'x'
				for j in gate_ip_edge:
					if(check_gate_valid(G.edges[j]['value_non_fault'],G.edges[j]['value_faulty'])==True):				#Input is D or D_bar check
						flag1=True	
					if(G.edges[j]['value_non_fault']=='x' or G.edges[j]['value_faulty']=='x'):							#Other Input is 'x'
						flag2= True
			
			if(flag1==True and flag2 ==True):
							print "D_fronteir", D_fronteir_li
							D_fronteir_li.insert(0,i)
							print "D_fronteir", D_fronteir_li
	return D_fronteir_li



				
			
def undefined_ip(node_D_fronteir):
		#Assigning a non-controlling value to the gate
		print "@@@@@@@@@@@ undefined_ip"
		print "node_D_fronteir",node_D_fronteir 
		global G
		gate_type =G.nodes[node_D_fronteir]['gatetype']
		gate_ip_edge = list(G.in_edges(nbunch=node_D_fronteir, data=False))
		#new_D_fronteir_edge=list(list(G.out_edges(nbunch=node_D_fronteir, data=False))[0])
		if (gate_type =='not'):
			#print "gate_ip_edge",list(gate_ip_edge[0])
			return list(gate_ip_edge[0])
		else:
			if(gate_type=='and' or  gate_type=='nand'):
				control_val =0
			elif(gate_type=='or' or  gate_type=='nor'):
				control_val =1
			elif(gate_type=='xor' or  gate_type=='xnor'):
				control_val	=1
			for i in range(len(gate_ip_edge)):
					if(G.edges[gate_ip_edge[i]]['value_non_fault']=='x' or G.edges[gate_ip_edge[i]]['value_faulty']=='x'):
						G.edges[gate_ip_edge[i]]['value_non_fault']	= str(int(not control_val))	
						G.edges[gate_ip_edge[i]]['value_faulty']	= G.edges[gate_ip_edge[i]]['value_non_fault']
						return gate_ip_edge[i]
			
			
											
					

def hardest_to_assign_val(Gate):
	global setting_all_ip
	if(Gate=='and'):
		setting_all_ip		='1'		#Non_control_val
	elif(Gate=='or'):
		setting_all_ip		='0'
	elif(Gate=='nand'):
		setting_all_ip		='0'		
	elif(Gate=='nor'):
		setting_all_ip		='1'
	


def max_min_Controllability(l,node1,val_assign):
		max_cc0_controllability	=0
		edge_max_cc0_controllability =''
		min_cc0_controllability	=10000 
		edge_min_cc0_controllability =''
		
		max_cc1_controllability	=0
		edge_max_cc1_controllability =''
		min_cc1_controllability	=10000 
		edge_min_cc1_controllability =''
		if(G.nodes[node1]['type']=='gate'):
			print "G.nodes[node1]['gatetype']",node1
			print "val_assign",val_assign
			for i in l:
				if(G.edges[i]['value_non_fault']=='x'):
					if(max_cc0_controllability < G.edges[i]['cc0']):
						max_cc0_controllability 	=G.edges[i]['cc0']
						edge_max_cc0_controllability =i
					if(min_cc0_controllability > G.edges[i]['cc0']):
						min_cc0_controllability	=G.edges[i]['cc0']
						edge_min_cc0_controllability =i
						
					if(max_cc1_controllability < G.edges[i]['cc1']):
						max_cc1_controllability 	=G.edges[i]['cc1']
						edge_max_cc1_controllability =i
					if(min_cc1_controllability > G.edges[i]['cc1']):
						min_cc1_controllability	=G.edges[i]['cc1']
						edge_min_cc1_controllability =i
			
			#~ print "edge_max_cc0_controllability",edge_max_cc0_controllability
			#~ print "edge_min_cc0_controllability",edge_min_cc0_controllability
			#~ print  "edge_max_cc1_controllability",edge_max_cc1_controllability
			#~ print "edge_min_cc1_controllability",edge_min_cc1_controllability
			
			hardest_ip = hardest_to_assign_val(G.nodes[node1]['gatetype'])
			print "G.nodes[node1]['gatetype']",G.nodes[node1]['gatetype']
			
			if(G.nodes[node1]['gatetype']=='and' or G.nodes[node1]['gatetype']=='nand'):
				if(val_assign ==hardest_ip):
					edge =edge_max_cc1_controllability
				else:
					edge =edge_min_cc0_controllability
			if(G.nodes[node1]['gatetype']=='or' or G.nodes[node1]['gatetype']=='nor'):
				if(val_assign ==hardest_ip):
					edge =edge_max_cc0_controllability
				else:
					edge =edge_min_cc1_controllability
					
			if(G.nodes[node1]['gatetype']=='xor' or G.nodes[node1]['gatetype']=='xnor' ):
				if(val_assign =='1'):
					edge =edge_max_cc1_controllability
				else:
					edge =edge_max_cc1_controllability
					
			
			
			if(G.nodes[node1]['gatetype']=='not'):
					edge =l[0]
			
			
			return edge	
				
				
def Backtrace(node1,node2):
		global G
		backtrack=0
		while(G.nodes[node1]['type']=='gate' or  G.nodes[node1]['type']=='fanout'):
			l= list (G.in_edges(nbunch=node1, data=False))
			print "node1,node2",node1 ,node2
			print "Before Backtrace",print_Backtrace_Graph_edges(l)
			
			if(G.nodes[node1]['type']=='gate'):
					edge_to_assign =max_min_Controllability(l,node1,G[node1][node2]['value_non_fault']	)
					print "edge_to_assign",edge_to_assign
			

					if(G.nodes[node1]['gatetype']=='nand' or G.nodes[node1]['gatetype']=='nor' or G.nodes[node1]['gatetype']=='not' or G.nodes[node1]['gatetype']=='xnor'):
						G.edges[edge_to_assign]['value_non_fault'] = str(int(not(int(G[node1][node2]['value_non_fault']))))				# Inversion parity =1
						
					else:
						G.edges[edge_to_assign]['value_non_fault'] 	= 	G[node1][node2]['value_non_fault']						#  Inversion parity =0



					backtrack=assign_faulty(edge_to_assign)																	#Assigning value to a non -faulty circuit 		
					print "After Backtrace",print_Backtrace_Graph_edges(l)
					#~ node1 	=i[0]
					#~ node2 	=i[1]
					
					new_node1		=edge_to_assign[0]
					new_node2		=edge_to_assign[1]
					print "node1,node2"	,new_node1,new_node2
					
					
																		
			if(G.nodes[node1]['type']=='fanout'):	
					for i in l:											# For fanout branches
						G.edges[i]['value_non_fault'] = G[node1][node2]['value_non_fault']	
						backtrack=assign_faulty(i)		#Assigning value to a non -faulty circuit 		
						print "After Backtrace",print_Backtrace_Graph_edges(l)
						new_node1 	=i[0]
						new_node2 	=i[1]	
						print "node1,node2"	,new_node1,new_node2
					
			
			
			node1 =new_node1
			node2 =new_node2
			if(backtrack ==True):
				#print backtrack
				break
			
						
		return node1,node2,G[node1][node2]['value_non_fault'],backtrack			
			
			
			

		
		
		





def assign_faulty(i):
	
		G.edges[i]['value_faulty']	= G.edges[i]['value_non_fault']
		#print G.edges[i]['value_faulty'],G.edges[i]['value_non_fault']
		if (tuple(faulty_edge_list[:2]) !=i):
					
			backtrack =0			
		else:
			backtrack =1			#Fault sentize is affected by backtrace
	
		return backtrack
						
					
def check_gate_valid(val1,val2):
	
	if((val1=='1' and val2 =='0') or (val1=='0' and val2=='1')):
		return True
	else:
		return False
	

def print_Backtrace_Graph_edges(l):	
	for i in range(len(l)):
				print 	l[i] ,G.edges[l[i]]['value_non_fault'],G.edges[l[i]]['value_faulty']
		
def print_Graph_edges():
	global G	
	
	print "faulty_edge_list",faulty_edge_list
	print "OUTPUT"
	for item in G.edges(data=True):	
			#if(G.nodes(data=True)[item[1]]['type'] =='output'):
					print item[0],item[1],item[2]['value_non_fault'] ,item[2]['value_faulty']
					
	#~ print "INPUT"
	#~ for item in G.edges(data=True):	
			#~ if(G.nodes(data=True)[item[0]]['type'] =='input'):
					#~ print item[0],item[1],item[2]['value_non_fault'] ,item[2]['value_faulty']
	#~ 
	
def error_at_PO():
		global G
		for i in PO_list:
			if(G.edges[i]['value_non_fault']!='x' and G.edges[i]['value_faulty']!='x' and G.edges[i]['value_non_fault']!=G.edges[i]['value_faulty'] ):
				return True
		return False 


#--------------------------------------------X_path_check-----------------------------------------------------------------------------	
def X_path(faulty_edge_list,PO_list):
	print "PO_list",PO_list
	print "faulty_edge_list",faulty_edge_list
		
	for i in PO_list:
			if (X_check_path(faulty_edge_list[1],i[1])==True):
				return True
				
				
	return False
	
	
def X_create_edge(path):		
		print path
		edge_list=[]
		if(len(path)>0):
			for i in range(len(path)):
				if(i>0):
					edge_list.append((path[i-1],path[i]))
			print "edges",edge_list
		return edge_list
		
			
def X_check_path(Source,Destination):
	flag =0
	
	for path in nx.all_simple_paths(G, source=Source, target=Destination):
		edges = X_create_edge(path)
	
		if(len(edges)!=0):
			for i in edges:
					print "i",i
					if((G.edges[i]['value_non_fault']=='x' or G.edges[i]['value_faulty']=='x') or  #X
					   (G.edges[i]['value_non_fault']=='1' and G.edges[i]['value_faulty']=='0')or	#D
					   (G.edges[i]['value_non_fault']=='0' and G.edges[i]['value_faulty']=='1')):	#D_bar
					
						flag=1
					else: 
						flag =0
						break
	
	if(flag==1):
		print Source,Destination
		return True
	else:
		print Source,Destination
		return False
#-----------------------------------------------------------------------------------------------------------------------------------------

	
def atpg_PODEM():
		global G
		global I_Stack
		count =0
		if(error_at_PO()==True):
			return True
		
		if(X_path(faulty_edge_list,PO_list)==False):
			print "X_path False"
			return False
		else:
			print "X_path True"
		#while (G.edges[PO_list[0]]['value_non_fault']=='x' ):
			#print "faulty_edge_list",faulty_edge_list
		print "**********************Objective ********************"
		[node1,node2]=Objective()
		#print "node1 node2",node1, node2
		print "**********************Backtrace ********************"
		[node1,node2,value,backtrack]	  =Backtrace(node1,node2)
		print "Backtrace node",node1 ,node2,value,backtrack
		if(backtrack==0):
			I_Stack.push((node1, node2),value)
		print "I_Stack.peek()",I_Stack.display_stack()
		
		print "**********************Forward Implication 1st********************"
		Forward_Implication(node1,node2)
		print "**************************************************************"
		print_Graph_edges()	
		print "One turn over try another"
		if(atpg_PODEM()==True):
			return True
		print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$SECOND TURN BEGIN$$$$$$$$$"
		I_Stack.complement_top_stack()
		[edges,val]=I_Stack.peek()
		G.edges[edges]['value_non_fault']=val
		G.edges[edges]['value_faulty']=val
		#print_Graph_edges()	
		print "**********************Forward Implication 2nd********************"
		Forward_Implication(node1,node2)
		if(atpg_PODEM()==True):
			return True	
		[edge_removed,val_removed]=I_Stack.pop()
		if(I_Stack.isEmpty()==True):
			print "NO TEST VECTOR POSSIBLE"
		else:
			[edges,val]=I_Stack.peek()
			G.edges[edges]['value_non_fault']=val
			G.edges[edges]['value_faulty']=val
			#print_Graph_edges()	
			return False
		
	


#Finding the Faulty edges
#~ def faulty_edg():					
	#~ global G			
	#~ for item in G.edges(data=True):
				#~ 
		#~ if(item[2]['fault']=='sa1' ):
				#~ stuck_at 		='sa1'
				#~ faulty_node1 	=item[0]
				#~ faulty_node2 	=item[1]			
		#~ elif(item[2]['fault']=='sa0'):
				#~ stuck_at	 	='sa0'
				#~ faulty_node1 	=item[0]
				#~ faulty_node2 	=item[1]
				#~ 
	#~ #return [faulty_node1,faulty_node2,stuck_at]
	#~ return ['fanout1_0','G1_0','sa0']



def overall_Podem_for_No_of_Unroll(GU,bfs1,faulty1_edge_list):
	global faulty_edge_list
	global D_fronteir_list
	global I_Stack
	global G
	global bfs
	G=GU
	bfs=bfs1
	faulty_edge_list	=faulty1_edge_list
	primary_input()
	primary_output()
	

	D_fronteir_list =[]

	I_Stack=IS.Impl_Stack()

	print_Graph_edges()
	
	atpg_PODEM()
	return PO_list,PI_list
	


#overall_Podem_for_No_of_Unroll(G,bfs)
#print_Graph_edges()	



