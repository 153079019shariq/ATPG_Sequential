from Graph_Sequential import GUZ as G
import Gates
import networkx as nx
from collections import OrderedDict

		
def print_Graph_edges():
	global G	
	for item in G.edges(data=True):
			print item[0],item[1], item[2]['cc0'],item[2]['cc1'],item[2]['co']
					

def controlabilty(node):
	global G
	list_predecessorCC0 =[]
	list_predecessorCC1 =[]
	print G.nodes[node]['type']
	if(G.nodes[node]['type']=='gates' or G.nodes[node]['type']=='fanout'):
		
		for predecessor in  list(G.in_edges(nbunch=node, data=False)):
			list_predecessorCC0.append(G.edges[predecessor]['cc0'])
			list_predecessorCC1.append(G.edges[predecessor]['cc1'])
		if(G.nodes[node]['type']=='gate'):
				i= list(G.out_edges(nbunch=node, data=False))[0]
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
		
		elif(G.nodes[node]['type']=='fanout'):
				for i in  list(G.out_edges(nbunch=node, data=False)):
					G.edges[i]['cc0'],G.edges[i]['cc1']= list_predecessorCC0[0],list_predecessorCC1[0]
					
		#print_Graph_edges()
		
def observabiltiy(node):
		global G
		#Predeccesor are the input of the gate and node is the gate itself.	
		if(G.nodes[node]['type']=='gate'):		
				print "%%%%%%%%%%%%%%%%%%%%%%%%%%Gate Observability%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
				#print "node in gate",node
				list_predecessorCC0 =[]
				list_predecessorCC1 =[]
				for predecessor in  list(G.in_edges(nbunch=node, data=False)):
						list_predecessorCC0.append(G.edges[predecessor]['cc0'])
						list_predecessorCC1.append(G.edges[predecessor]['cc1'])
						
				edgeCO= list(G.out_edges(nbunch=node, data=True))[0][2]['co']
				
				list_predecessorCO =[]

				if(G.nodes[node]['gatetype']=='and' or G.nodes[node]['gatetype']=='nand'):
					list_predecessorCO = Gates.AND_NAND_Obser(list_predecessorCC1,edgeCO)
					
				elif(G.nodes[node]['gatetype']=='or' or G.nodes[node]['gatetype']=='nor'):
					list_predecessorCO = Gates.AND_NAND_Obser(list_predecessorCC0,edgeCO)
					
				elif(G.nodes[node]['gatetype']=='xor' or G.nodes[node]['gatetype']=='xnor'):
					list_predecessorCO = Gates.XOR_XNOR_Obser(list_predecessorCC1,list_predecessorCC0,edgeCO)
					
				elif(G.nodes[node]['gatetype']=='not'):
					list_predecessorCO = Gates.NOT_Obser(edgeCO)
				count =0	
				for predecessor in  list(G.in_edges(nbunch=node, data=False)):
					G.edges[predecessor]['co'] = list_predecessorCO[count]
					#print "G.nodes[predecessor]['co']",G.edges[predecessor]['co']
					count +=1
				#print_Graph_edges()
		#Node is fanout itself and branches of it are successor.		
		elif(G.nodes[node]['type']=='fanout'):
				print "$$$$$$$$$$$$$$$$$$$$$$$Fanout Observability$$$$$$$$$$$$$$$$$$$$$$$$"
				edge =list(G.in_edges(nbunch=node, data=False))[0]
				list_successor =[]
				for successor in list(G.out_edges(nbunch=node, data=False)):
					list_successor.append(G.edges[successor]['co'])
				G.edges[edge]['co']  =min(list_successor)
				

					
lis =['A','B','fanout1','1','fanout2','fanout3','2','fanout4','3','4','fanout6','5','fanout5','7','9','6','8','X','Y','Z']	
#1st controlabiliy should be calculated then observability.The controlability is calculated from PI to PO.And the observability is calculated from PO to PI.
for node in lis:	
		controlabilty(node)

for node in reversed(lis):	
		observabiltiy(node)
print "Result"
print_Graph_edges()
print list(G.out_edges(nbunch='fanout3', data=False))[0]
