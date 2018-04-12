#import Podem as Podem
from Podem import *
from Graph_Seq_8_3 import *
from Controlability_Observability import *

#Positive Time Frame
def error_at_FF_ip_or_Primary_output(Graph,PO_list):
		
		for i in PO_list:
			if(Graph.edges[i]['value_non_fault']!='x' and Graph.edges[i]['value_faulty']!='x' and Graph.edges[i]['value_non_fault']!=Graph.edges[i]['value_faulty'] ):
				if(Graph.nodes[i[1]]['type']=='output' and  Graph.nodes[i[1]]['op_type']=='FF_ip'):
					return True
		return False 
		



#~ #----------------------------------------------Faulty edge(If Fault cannot be propagated to primary o/p then increase No of unroll)-------------------------------------------------------------------------------


#Negative Time Frame
def error_at_FF_op_or_Primary_input(Graph,PI_list):
	for i in PI_list:
			if(Graph.edges[i]['value_non_fault']!='x' and Graph.edges[i]['value_faulty']!='x'):
				if(Graph.nodes[i[0]]['type']=='input'and  Graph.nodes[i[0]]['op_type']=='FF_op'):
					return True
						
	return False 






def check_path(Source,Destination,Graph):
	for path in nx.all_simple_paths(Graph, source=Source, target=Destination):
			return True
	return False
	
		
			
def check_path_op(Source,Graph):
	for item in Graph.nodes(data=True):
		
		if(item[1]['type']=='output'):
			if(item[1]['op_type']=='Primary_op'):
				if(check_path(Source,item[0],Graph)==True):
					return True
				elif(Source==item[0]):					#For the case of fault at o/p edge
					return True
				
			
#~ #---------------------------------------------------------------------------------------------------------------------------------------------------
#~ 
#~ 
def faulty_edg_len(Graph):
	stuck_at_list=[]	
	faulty_node1_list=[]
	faulty_node2_list=[]
	fault_path_to_op	=	False							
	for item in Graph.edges(data=True):
		
		if(item[2]['fault']=='sa1' ):
				stuck_at_list.append('sa1')
				faulty_node1_list.append(item[0])
				faulty_node2_list.append(item[1])			
		elif(item[2]['fault']=='sa0'):
				print "item",item[2]['fault']
				stuck_at_list.append('sa0')
				faulty_node1_list.append(item[0])
				faulty_node2_list.append(item[1])
				
				
	for item in Graph.edges(data=True):
		if(item[2]['fault']=='sa0' or item[2]['fault']=='sa1'):
			print "item[1]",item[1]
			if(check_path_op(item[1],Graph)==True):
				fault_path_to_op	=	True
				break
	
	return faulty_node1_list,faulty_node2_list,stuck_at_list,fault_path_to_op











def lis(sorted_x):
	list1=[]
	for i in sorted_x:
		list1.append(i[0])
	return list1


No_of_Unroll=1
faulty_list=[]
faulty_edge_select=0
def overall_Graph_Seq():
	global No_of_Unroll
	global faulty_list
	global faulty_node1_list
	global faulty_node2_list
	global stuck_at_list
	global bfs
	global faulty_edge_select
	
	GU	=Total_Graph(No_of_Unroll)
	
	print "No_of_Unroll",No_of_Unroll
	faulty_node1_list,faulty_node2_list,stuck_at_list,fault_path_to_op= faulty_edg_len(GU)
	bfs = Level (GU)
	sorted_x = sorted(bfs.items(), key=operator.itemgetter(1))
	list1=lis(sorted_x)
	overall_Controllability(GU,list1)
	print "fault_path_to_op",fault_path_to_op
	if(No_of_Unroll==10):
				print "Current Time Frame not suitable to test the fault"
	
	elif(fault_path_to_op==0):		#Check if the fault can be propagated to the Primary output with No_of_Unroll
		No_of_Unroll +=1
		overall_Graph_Seq()
	else:
		fault_edge_select_rev =len(faulty_node1_list)-faulty_edge_select-1
		print"faulty_edge_select",faulty_edge_select
		faulty_list =[faulty_node1_list[fault_edge_select_rev],faulty_node2_list[fault_edge_select_rev],stuck_at_list[fault_edge_select_rev]]
		
		PO_list,PI_list=overall_Podem_for_No_of_Unroll(GU,bfs,faulty_list)
		
		
		if(error_at_FF_ip_or_Primary_output(GU,PO_list)==True):
				No_of_Unroll+=1					#Increase the number of Unroll
				print "G_Seq.No_of_Unroll",No_of_Unroll
				overall_Graph_Seq()            #Call the function recursively so that fault reaches PO
		elif(error_at_FF_op_or_Primary_input(GU,PI_list)==True):	
				No_of_Unroll+=1					#Increase the number of Unroll
				print "G_Seq1.No_of_Unroll",No_of_Unroll
				faulty_edge_select +=1
				overall_Graph_Seq()            #Call the function recursively so that it bactrace it assignment from FF_op to Primary_ip
		
		


overall_Graph_Seq()





