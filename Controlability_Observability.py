from Graph_Controlability_Observability_8_7  import *
import Gates
import networkx as nx
from collections import OrderedDict

		
def print_Graph_edges():
	global G	
	for item in G.edges(data=True):
			print item[0],item[1], item[2]['cc0'],item[2]['cc1'],item[2]['dr1_0'],item[2]['dr0_1']
					

def controlabilty(node):
	global G
	list_predecessorCC0 =[]
	list_predecessorCC1 =[]
	
	if(G.nodes[node]['type']=='gate' or G.nodes[node]['type']=='fanout' or  G.nodes[node]['type']=='FF'):
		
		for predecessor in  list(G.in_edges(nbunch=node, data=False)):
			list_predecessorCC0.append(G.edges[predecessor]['cc0'])					#Multiple inedge
			list_predecessorCC1.append(G.edges[predecessor]['cc1'])
		
		if(G.nodes[node]['type']=='gate'):
				
				i= list(G.out_edges(nbunch=node, data=False))[0]					#One outedge as output of Gate is one
				if(G.nodes[node]['gatetype']=='and'):
					G.edges[i]['cc0'],G.edges[i]['cc1']= Gates.AND_Control(list_predecessorCC0,list_predecessorCC1)
				elif(G.nodes[node]['gatetype']=='or'):
					G.edges[i]['cc0'],G.edges[i]['cc1']= Gates.OR_Control(list_predecessorCC0,list_predecessorCC1)
				elif(G.nodes[node]['gatetype']=='nand'):
					G.edges[i]['cc0'],G.edges[i]['cc1']= Gates.NAND_Control(list_predecessorCC0,list_predecessorCC1)
				elif(G.nodes[node]['gatetype']=='nor'):
					G.edges[i]['cc0'],G.edges[i]['cc1']= Gates.NOR_Control(list_predecessorCC0,list_predecessorCC1)
				elif(G.nodes[node]['gatetype']=='xor'):
					G.edges[i]['cc0'],G.edges[i]['cc1']= Gates.XOR_Control(list_predecessorCC0,list_predecessorCC1)									
				elif(G.nodes[node]['gatetype']=='xnor'):
					G.edges[i]['cc0'],G.edges[i]['cc1']= Gates.XNOR_Control(list_predecessorCC0,list_predecessorCC1)
				elif(G.nodes[node]['gatetype']=='not'):
					G.edges[i]['cc0'],G.edges[i]['cc1']= Gates.NOT_Control(list_predecessorCC0,list_predecessorCC1)
				#print "G.edges[i]['cc0'],G.edges[i]['cc1']",G.edges[i]['cc0'],G.edges[i]['cc1']
		
		elif(G.nodes[node]['type']=='fanout'):
				for i in  list(G.out_edges(nbunch=node, data=False)):
					G.edges[i]['cc0'],G.edges[i]['cc1']= list_predecessorCC0[0],list_predecessorCC1[0] #Multiple outedge
				#print "G.edges[i]['cc0'],G.edges[i]['cc1']",G.edges[i]['cc0'],G.edges[i]['cc1']
				
		elif(G.nodes[node]['type']=='FF'):
				for i in  list(G.out_edges(nbunch=node, data=False)):
					G.edges[i]['cc0'],G.edges[i]['cc1']= list_predecessorCC0[0]+1,list_predecessorCC1[0]+1	#One outedge
				#print "G.edges[i]['cc0'],G.edges[i]['cc1']",G.edges[i]['cc0'],G.edges[i]['cc1']
					
		#print_Graph_edges()
	
	
	
def drivibility(node):
	global G
	
	for i in G.edges():
		
		if (G.edges[i]['fault']=='sa0'):
				G.edges[i]['dr1_0']	=G.edges[i]['cc1']
				G.edges[i]['dr0_1']	=10000
		elif(G.edges[i]['fault']=='sa1'):
				G.edges[i]['dr0_1']	=G.edges[i]['cc0']
				G.edges[i]['dr1_0']	=10000
	
	if(G.nodes[node]['type']=='gate'):
		print "Gate_node",node,G.nodes[node]['gatetype']
		list_predecessor_1	=[]
		list_drivibility1_0	=[]
		list_drivibility0_1	=[]
		for predecessor in  list(G.in_edges(nbunch=node, data=False)):
				val_predecessor=0
				for predecessor2 in  list(G.in_edges(nbunch=node, data=False)):
						print "predecessor2",predecessor2 ,G.edges[predecessor2]['cc0']
						if(predecessor !=predecessor2 and len(list(G.in_edges(nbunch=node, data=False)))>1): #Excluding NOT gate
							if(G.nodes[node]['gatetype']=='and' or G.nodes[node]['gatetype']=='nand'):
								val_predecessor+=G.edges[predecessor2]['cc1']
							elif(G.nodes[node]['gatetype']=='or' or G.nodes[node]['gatetype']=='nor'):
								val_predecessor+=G.edges[predecessor2]['cc0']
						
				
				list_predecessor_1.append(val_predecessor)
				list_drivibility1_0.append(G.edges[predecessor]['dr1_0'])
				list_drivibility0_1.append(G.edges[predecessor]['dr0_1'])
				if(G.nodes[node]['gatetype']=='and' or G.nodes[node]['gatetype']=='or'):
					print "AND_OR_Drive",Gates.AND_OR_Drive(list_drivibility1_0,list_predecessor_1)
					G.edges[list(G.out_edges(nbunch=node, data=False))[0]]['dr1_0']=Gates.AND_OR_Drive(list_drivibility1_0,list_predecessor_1)
					G.edges[list(G.out_edges(nbunch=node, data=False))[0]]['dr0_1']=Gates.AND_OR_Drive(list_drivibility0_1,list_predecessor_1)
				elif(G.nodes[node]['gatetype']=='nand' or G.nodes[node]['gatetype']=='nor'):
					print "NAND_NOR_Drive",Gates.NAND_NOR_Drive(list_drivibility1_0,list_predecessor_1)
					G.edges[list(G.out_edges(nbunch=node, data=False))[0]]['dr1_0']=Gates.NAND_NOR_Drive(list_drivibility0_1,list_predecessor_1)
					G.edges[list(G.out_edges(nbunch=node, data=False))[0]]['dr0_1']=Gates.NAND_NOR_Drive(list_drivibility1_0,list_predecessor_1)
				elif(G.nodes[node]['gatetype']=='not'):
					G.edges[list(G.out_edges(nbunch=node, data=False))[0]]['dr1_0']=G.edges[list(G.in_edges(nbunch=node, data=False))[0]]['dr1_0']+1
					G.edges[list(G.out_edges(nbunch=node, data=False))[0]]['dr0_1']=G.edges[list(G.in_edges(nbunch=node, data=False))[0]]['dr0_1']+1
					
		print  list_predecessor_1
		print  list_drivibility1_0
		print  list_drivibility0_1
		
	elif(G.nodes[node]['type']=='fanout'):
			for i in  list(G.out_edges(nbunch=node, data=False)):
					G.edges[i]['dr1_0']= G.edges[list(G.in_edges(nbunch=node, data=False))[0]]['dr1_0']
					G.edges[i]['dr0_1']= G.edges[list(G.in_edges(nbunch=node, data=False))[0]]['dr0_1']

	elif(G.nodes[node]['type']=='FF'):
			G.edges[list(G.out_edges(nbunch=node, data=False))[0]]['dr1_0']= G.edges[list(G.in_edges(nbunch=node, data=False))[0]]['dr1_0'] +100
			G.edges[list(G.out_edges(nbunch=node, data=False))[0]]['dr0_1']= G.edges[list(G.in_edges(nbunch=node, data=False))[0]]['dr0_1'] +100
#~ def observabiltiy(node):
		#~ global G
		#~ #Predeccesor are the input of the gate and node is the gate itself.	
		#~ if(G.nodes[node]['type']=='gate'):		
				#~ print "%%%%%%%%%%%%%%%%%%%%%%%%%%Gate Observability%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
				#~ #print "node in gate",node
				#~ list_predecessorCC0 =[]
				#~ list_predecessorCC1 =[]
				#~ for predecessor in  list(G.in_edges(nbunch=node, data=False)):
						#~ list_predecessorCC0.append(G.edges[predecessor]['cc0'])
						#~ list_predecessorCC1.append(G.edges[predecessor]['cc1'])
						#~ 
				#~ edgeCO= list(G.out_edges(nbunch=node, data=True))[0][2]['co']
				#~ 
				#~ list_predecessorCO =[]
#~ 
				#~ if(G.nodes[node]['gatetype']=='and' or G.nodes[node]['gatetype']=='nand'):
					#~ list_predecessorCO = Gates.AND_NAND_Obser(list_predecessorCC1,edgeCO)
					#~ 
				#~ elif(G.nodes[node]['gatetype']=='or' or G.nodes[node]['gatetype']=='nor'):
					#~ list_predecessorCO = Gates.AND_NAND_Obser(list_predecessorCC0,edgeCO)
					#~ 
				#~ elif(G.nodes[node]['gatetype']=='xor' or G.nodes[node]['gatetype']=='xnor'):
					#~ list_predecessorCO = Gates.XOR_XNOR_Obser(list_predecessorCC1,list_predecessorCC0,edgeCO)
					#~ 
				#~ elif(G.nodes[node]['gatetype']=='not'):
					#~ list_predecessorCO = Gates.NOT_Obser(edgeCO)
				#~ count =0	
				#~ for predecessor in  list(G.in_edges(nbunch=node, data=False)):
					#~ G.edges[predecessor]['co'] = list_predecessorCO[count]
					#~ #print "G.nodes[predecessor]['co']",G.edges[predecessor]['co']
					#~ count +=1
				#~ #print_Graph_edges()
		#~ #Node is fanout itself and branches of it are successor.		
		#~ elif(G.nodes[node]['type']=='fanout'):
				#~ print "$$$$$$$$$$$$$$$$$$$$$$$Fanout Observability$$$$$$$$$$$$$$$$$$$$$$$$"
				#~ edge =list(G.in_edges(nbunch=node, data=False))[0]
				#~ list_successor =[]
				#~ for successor in list(G.out_edges(nbunch=node, data=False)):
					#~ list_successor.append(G.edges[successor]['co'])
				#~ G.edges[edge]['co']  =min(list_successor)
				

					

#1st controlabiliy should be calculated then observability.The controlability is calculated from PI to PO.And the observability is calculated from PO to PI.
for node in list1:	
		controlabilty(node)
		
for node in list1:	
		#print node		
		drivibility(node)
#~ for node in reversed(lis):	
		#~ observabiltiy(node)
print "Result"
print_Graph_edges()
