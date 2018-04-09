import Gates
import operator
#from Graph_Abramovici import G,bfs
from Graph_Sequential import  GUZ as G,bfs
import Implication_Stack as IS
from S_graph import No_of_unroll

def primary_input():
	PI_list= []
	
	for item in G.nodes(data=True):
		
		if(item[1]['type']=='input'):
				list_outedge =list(G.out_edges(nbunch=item[0], data=False))	
				PI_list.append(list_outedge[0])
	return PI_list
	
def primary_output():
	PO_list= []
	for item in G.nodes(data=True):
		if(item[1]['type']=='output'):
				list_outedge =list(G.in_edges(nbunch=item[0], data=False))	
				PO_list.append(list_outedge[0])
	return PO_list
	
	
def Forward_Implication_fanout(node1,node2,list_outedge):
	#print "@@@@@@@@@Forward Implication Fanout"
	global G
	#~ print "faulty_edge_list[:2]",faulty_edge_list[:2]
	#~ print "G[node1][node2]['value_faulty']",G[node1][node2]['value_faulty']
	for i in range(len(list_outedge)):
	
		G.edges[list_outedge[i]]['value_non_fault']  = G[node1][node2]['value_non_fault']
		if(faulty_edge_list[:2]!=list(list_outedge[i])):
			#~ print "***********"
			G.edges[list_outedge[i]]['value_faulty']  = G[node1][node2]['value_faulty']
		new_node1		=list_outedge[i][0]
		new_node2		=list_outedge[i][1]
		print "new_node1 new_node2",new_node1,new_node2	
		if(G.nodes[new_node2]['type']=='gate' or G.nodes[new_node2]['type']=='fanout'):
			Forward_Implication(new_node1,new_node2)
		
		new_node1	= node1
		new_node2	= node2
	
def Forward_Implication_gates(node1,node2):
	#print "@@@@@@@@@Forward Implication Gates"
	global G
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
			
			
	if(faulty_edge_list[:2] !=list(list(G.out_edges(nbunch=node2, data=False))[0])): 		
		G.edges[list(G.out_edges(nbunch=node2, data=False))[0]]['value_faulty']    =output_faulty 
	
	
		
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
			for j in bfs.keys():
				if(i==j):
					D_fronteir_level[i]=bfs[j]
		
		D_fronteir_level_sorted = sorted(D_fronteir_level.items(), key=operator.itemgetter(1),reverse=True)
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
			for i in range(len(gate_ip_edge)):
					if(G.edges[gate_ip_edge[i]]['value_non_fault']=='x' or G.edges[gate_ip_edge[i]]['value_faulty']=='x'):
						G.edges[gate_ip_edge[i]]['value_non_fault']	= str(int(not control_val))	
						G.edges[gate_ip_edge[i]]['value_faulty']	= G.edges[gate_ip_edge[i]]['value_non_fault']
						return gate_ip_edge[i]
			
			
											
						

						
def Backtrace(node1,node2):
		global G
		backtrack=0
		#for iter1 in range(No_of_unroll):
		while(G.nodes[node1]['type']=='gate' or  G.nodes[node1]['type']=='fanout'):			# Checking whether PI is reached then terminate
			l= list (G.in_edges(nbunch=node1, data=False))
			print "node1",node1
			print "Before Backtrace",print_Backtrace_Graph_edges(l)
			
			for i in l:
				
				if(G.nodes[node1]['type']=='gate'and G.edges[i]['value_non_fault']=='x'):										#For all the gates
					if(G.nodes[node1]['gatetype']=='nand' or G.nodes[node1]['gatetype']=='nor' or G.nodes[node1]['gatetype']=='not'):
						G.edges[i]['value_non_fault'] = str(int(not(int(G[node1][node2]['value_non_fault']))))				# Inversion parity =1
						
					else:
						G.edges[i]['value_non_fault'] = 	G[node1][node2]['value_non_fault']						#  Inversion parity =0
					backtrack=assign_faulty(i)																	#Assigning value to a non -faulty circuit 		
					print "After Backtrace",print_Backtrace_Graph_edges(l)
					node1 	=i[0]
					node2 	=i[1]
					
					break
					
																			
				elif(G.nodes[node1]['type']=='fanout'):											# For fanout branches
					G.edges[i]['value_non_fault'] = G[node1][node2]['value_non_fault']	
					backtrack=assign_faulty(i)		#Assigning value to a non -faulty circuit 		
					print "After Backtrace",print_Backtrace_Graph_edges(l)
					node1 	=i[0]
					node2 	=i[1]	
					
			
			if(backtrack ==True):
				#print backtrack
				break
			#Assigning output of FF to input of FF		
			#~ if(G.nodes[node1]['type']=='FF'):
				#~ print "HEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEELLLLLLLLLLLLLLLLOOOOOOOOOOOOOOOOOOOOOO"
				#~ print (node1[0:3]+ "_ip")
				#~ print list(G.in_edges(nbunch=node1[0:3]+"_ip", data=False))[0]
				#~ G.edges[list(G.in_edges(nbunch=node1[0:3]+"_ip", data=False))[0]]['value_non_fault'] =	G[node1][node2]['value_non_fault']	
				#~ G.edges[list(G.in_edges(nbunch=node1[0:3]+"_ip", data=False))[0]]['value_faulty'] =	G[node1][node2]['value_faulty']	
				#~ print "BACTRACE_RESULT"
				#~ print_Graph_edges()
				
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
	output =str(faulty_edge_list) +"\n"
	print "faulty_edge_list",faulty_edge_list
	for item in G.edges(data=True):
					#print item
		#	if(G.nodes(data=True)[item[0]]['type'] =='input' or G.nodes(data=True)[item[1]]['type'] =='output' or  G.nodes(data=True)[item[0]]['type'] =='FF_op'):
					
					print item[0],item[2]['value_non_fault'] ,item[2]['value_faulty']
					output +=str(item[0])+" " + str(item[1])+" " + str(item[2]['value_non_fault'])+" " +str(item[2]['value_faulty']) +"\n" 
	
	output += "\n" 
	f = open("ATPG_output.txt", 'a+')
	f.write(output)
	f.close()
	
def error_at_PO():
		global G
		for i in PO_list:
			if(G.edges[i]['value_non_fault']!='x' and G.edges[i]['value_faulty']!='x' and G.edges[i]['value_non_fault']!=G.edges[i]['value_faulty'] ):
				return True
		return False 
def test_not_possible_with_this_val():
		global G
		for i in PO_list:
			if(G.edges[i]['value_non_fault']==G.edges[i]['value_faulty'] and G.edges[i]['value_non_fault']!='x' and G.edges[i]['value_faulty']!='x' and
			all_PI_assigned()==True):
				return True
		return False
			
def all_PI_assigned():
	global G
	for i in PI_list:
		if(G.edges[i]['value_non_fault']=='x'):
			return False
	
	return True

	
def atpg_PODEM():
		global G
		global I_Stack
		count =0
		if(error_at_PO()==True):
			return True
		print "test_not_possible_with_this_val()",test_not_possible_with_this_val()
		if(test_not_possible_with_this_val()==True):
			return False	
		#while (G.edges[PO_list[0]]['value_non_fault']=='x' ):
			#print "faulty_edge_list",faulty_edge_list
		print "**********************Objective ********************"
		[node1,node2]=Objective()
		print "node1 node2",node1, node2
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
def faulty_edg():								
	for item in G.edges(data=True):
				
		if(item[2]['fault']=='sa1' ):
				stuck_at 		='sa1'
				faulty_node1 	=item[0]
				faulty_node2 	=item[1]			
		elif(item[2]['fault']=='sa0'):
				stuck_at	 	='sa0'
				faulty_node1 	=item[0]
				faulty_node2 	=item[1]
				
	#return [faulty_node1,faulty_node2,stuck_at]
	return ['fanout1_4','G1_4','sa1']



faulty_edge_list=faulty_edg()
PI_list  = primary_input()
PO_list  = primary_output()


D_fronteir_list =[]

I_Stack=IS.Impl_Stack()
atpg_PODEM()
print_Graph_edges()	



