import sys
faulty_edge_list =[sys.argv[1],sys.argv[2],sys.argv[3]]
#faulty_edge_list =['fanout1' ,'G6' ,'sa0']
input_list =[]
output_list=[]
wire_list =[]
nodes_list =[]
edges_list =[]


output_of_gates =[]
input_of_gates =[]
input_of_gates =[]
input2_of_gates =[]

output_FF =[]
input_FF  =[]


dic_gate_types ={}

with open ('s27.v','r') as f:
	lines = f.read().splitlines()
	for i in lines:
		list1= i.split()
		if(list1[0]=='wire'):
			wire_list=list1[1].split(',')
		if(list1[0]=='input'):
			#print "input_list",list1[1].split(',')
			for i in list1[1].split(','):
				if(i !="GND" and i!='VDD' and i!='CK'):
					input_list.append(i)
		if(list1[0]=='output'):
			output_list=list1[1].split(',')
		if(list1[0]=='nand' or list1[0]=='nor' or list1[0]=='or' or list1[0]=='and' or list1[0]=='not' or list1[0]=='xor' or list1[0]=='xnor'):
			list2 = list1[3].split(',')
			output_of_gates.append(list2[0])
			input_of_gates.append(list2[1:])
			dic_gate_types[list2[0]]=list1[0]
		if(list1[0]=='dff'):
			 list2 = list1[3].split(',')
			 output_FF.append(list2[1])
			 input_FF.append(list2[2])
			
			
print "output_FF",output_FF
print "input_FF",input_FF		


#fanout_list------------------------------
fanout1_dic ={}
output_dic	={}
fanout2_list =[]
temp_list=[]
print "input_of_gates",input_of_gates
temp_list =[j for i in input_of_gates for j in i]

for i in temp_list:
	if (temp_list.count(i)>1 and (i not in fanout2_list)):
		fanout2_list.append(i)
print "fanout2_list",fanout2_list

for i in range(len(fanout2_list)):
	check	= "fanout" + str(i+1)
	fanout1_dic[fanout2_list[i]]=check
print "fanout1_dic",fanout1_dic

#Output_list-------------------------------------
for i in range(len(output_list)):
	check2	= "output" + str(i+1)
	output_dic[output_list[i]]=check2
print "output_dic",output_dic


print "dic_gate_types",dic_gate_types
print type(dic_gate_types[output_of_gates[0]])
nodes_list =	input_list	+	output_of_gates + output_dic.values() +fanout1_dic.values() +output_FF	

print "input_of_gates",input_of_gates



#---Insert the fanout node in input1_of_g
#lis[lis.index('one')] = 'replaced!'
for i in input_of_gates:
	for j in i:
		if(j in fanout1_dic.keys()):
			print j
			input_of_gates[input_of_gates.index(i)][i.index(j)]=fanout1_dic[j]

print "input_of_gates",input_of_gates


#----------------------FF_ip replacement with fanout(if there is fanout)
print "fanout1_dic.keys()",fanout1_dic
for i in input_FF:
		if(i in fanout1_dic.keys()):
			print "FF_replCEMENT*****************************"
			print "FF",i,fanout1_dic[i]
			input_FF[input_FF.index(i)]=fanout1_dic[i]

print "input_of_gates",input_of_gates
print "input_FF",input_FF		


#------------------------------------------
print "fanout1_dic",fanout1_dic
for key, value in fanout1_dic.iteritems():
	 edges_list.append((key,value))
	 #print "(fanout1_dic.keys(),fanout1_dic.values())",type((key,value))

for key, value in output_dic.iteritems():
	 edges_list.append((key,value))
	 print "output",(key,value)


for i in range(len(output_of_gates)):
	for j in range(len(input_of_gates[i])):
		edges_list.append((input_of_gates[i][j],output_of_gates[i]))
		
		
for i in range(len(output_FF)):
	print "FF_DFSFF.KNJF",input_FF[i],output_FF[i]
	edges_list.append((input_FF[i],output_FF[i]))


print "edges_list",edges_list



		
#--------------------------------Contorllability 1 for Primary input -------------------------------------------
list_ip_SCOAP =[]
for ip in input_list:
	
	for i in edges_list:
		if (ip == i[0]):
				print ip
				print i[0]
				list_ip_SCOAP.append(i)
print "list_ip_SCOAP",list_ip_SCOAP



#------------------------------------------------------------------------------------------------------------------		

print "input_list",input_list
print "fanout1_dic",fanout1_dic
print "output_of_gates",output_of_gates
print "output_list",output_list

#print "wire_list",wire_list

print "**************************************"

#print "nodes_list",nodes_list
#print "edges_list",edges_list 

#*****************************Constructing a graph*************************************************************************
output = """import networkx as nx 
G = nx.DiGraph()""" + "\n"

add_node =""
add_edges_from= "G.add_edges_from(["
add_faulty_edges_check="G.add_edge('fanout3','G17', value_non_fault='x',value_faulty='x',fault='sa1')"
add_faulty_edges	="G.add_edge" +"(" + "\'"+ faulty_edge_list[0] + "\'" + "," + "\'"+ faulty_edge_list[1] + "\'" + ", value_non_fault='x',value_faulty='x',fault=" +"\'"+ faulty_edge_list[2] +"\'"+ ")"

print "add_f",add_faulty_edges

for  i in nodes_list:
	
	if(i in input_list):
		add_node  += "G.add_node" +"(" + "\'"+ i + "\'"+ "," + "type" + "=" + "\'"+ "input" + "\'" +"," + "op_type" + "=" + "\'"+ "Primary_ip" + "\'"+ ")" + "\n"
	if(i in fanout1_dic.values()):
		add_node  += "G.add_node" +"(" + "\'"+ i + "\'"+ "," + "type" + "=" + "\'" + "fanout" + "\'" + ")" + "\n"
	if(i in output_of_gates):
		add_node  += "G.add_node" +"(" + "\'"+ i + "\'"+ "," + "type" + "=" + "\'" + "gate" + "\'" + ","+"gatetype" + "=" + "\'" + dic_gate_types[i] + "\'" + ")" + "\n"
	if(i in output_dic.values()):
		add_node  += "G.add_node" +"(" + "\'"+ i + "\'"+ "," + "type" + "=" + "\'" + "output" + "\'"  +"," + "op_type" + "=" + "\'"+ "Primary_op" + "\'"+")" + "\n"
	if(i in output_FF ):
		add_node  += "G.add_node" +"(" + "\'"+ i + "\'"+ "," + "type" + "=" + "\'" + "FF" + "\'" + ")" + "\n"
print add_node 




for i in range(len(edges_list)):
	if(i==len(edges_list)-1):
		add_edges_from += str(edges_list[i])
	else:
		add_edges_from += str(edges_list[i])+","
	
	
add_edges_from	+= "], value_non_fault='x',value_faulty='x', fault='',cc0=0,cc1=0,co=0)" 
print add_edges_from

#--------------------------------Contorllability 1 for Primary input -------------------------------------------
print "list_ip_SCOAP",list_ip_SCOAP
add_ip_SCOAP =''
for i in list_ip_SCOAP:
	add_ip_SCOAP	+="G.add_edge" +"(" + "\'"+ i[0] + "\'" + "," + "\'"+ i[1] + "\'" + ", value_non_fault='x',value_faulty='x', fault='',cc0=1,cc1=1,co=0)" + "\n"
print "add_ip_SCOAP",add_ip_SCOAP





output += add_node + add_edges_from  + "\n" + add_ip_SCOAP  +  "\n" + "\n" +  add_faulty_edges+ "\n"


#print output 
f = open("Graph_build.py", 'w')
f.write(output)
f.close()



