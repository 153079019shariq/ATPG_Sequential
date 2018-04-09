
import copy

def AND_gate(list_input):
	flag =0
	
	for input1 in list_input:
			if(input1=='0'):			#Controlling_value
				return '0'					
			else:
				if(input1=='x'):
					flag =1
					
	if(flag==1):
		return 'x'
	else:
		return '1' 						#All input is '1'
		
		
def OR_gate(list_input):
	flag =0
	
	for input1 in list_input:
			if(input1=='1'):
				return '1'
			else:
				if(input1=='x'):
					flag =1
					
	if(flag==1):
		return 'x'
	else:
		return '0' 


def NAND_gate(list_input):
	flag =0
	
	for input1 in list_input:
			if(input1=='0'):
				return '1'
			else:
				if(input1=='x'):
					flag =1
					
	if(flag==1):
		return 'x'
	else:
		return '0' 
		
		
def NOR_gate(list_input):
	flag =0
	
	for input1 in list_input:
			if(input1=='1'):
				return '0'
			else:
				if(input1=='x'):
					flag =1
					
	if(flag==1):
		return 'x'
	else:
		return '1' 
		
		

def XOR_gate(list_input):
	flag =0
	count =0
	for input1 in list_input:
			if(input1=='x'):
				return 'x'
			else:
				if(input1=='1'):
					count =count +1
					
	if(count % 2 !=0):					#Odd no of 1
		return '1'
	else:
		return '0' 
		

def XNOR_gate(list_input):
	flag =0
	count =0
	for input1 in list_input:
			if(input1=='x'):
				return 'x'
			else:
				if(input1=='1'):
					count =count +1
					
	if(count % 2 ==0):			#Even no of 1
		return '1'
	else:
		return '0' 



			
def NOT_gate(a):
	return {
			'0':'1',
			'1':'0',
			'x':'x'
			}[a]	

def BUFFER_gate(a):
	return {
			'0':'0',
			'1':'1',
			'x':'x'
			}[a]	
			
def stuck_at_0(a):
	return AND_gate(a,'0')

def stuck_at_1(a):
	return OR_gate(a,'1')
	
	
def AND_Control(list_predecessorCC0,list_predecessorCC1):
	return (min(list_predecessorCC0)+1),(sum(list_predecessorCC1)+1)

def OR_Control(list_predecessorCC0,list_predecessorCC1):
	return (sum(list_predecessorCC0)+1),(min(list_predecessorCC1)+1)


def NAND_Control(list_predecessorCC0,list_predecessorCC1):
	return (sum(list_predecessorCC1)+1),(min(list_predecessorCC0)+1)

def NOR_Control(list_predecessorCC0,list_predecessorCC1):
	return (min(list_predecessorCC1)+1),(sum(list_predecessorCC0)+1)
	
def NOT_Control(list_predecessorCC0,list_predecessorCC1):
	return (list_predecessorCC1[0]+1),(list_predecessorCC0[0]+1)
	
def XOR_Control(list_predecessorCC0,list_predecessorCC1):
	return (min(sum(list_predecessorCC0),sum(list_predecessorCC1))+1,
			min((list_predecessorCC0[0]+list_predecessorCC1[1]),(list_predecessorCC0[1]+list_predecessorCC1[0]))+1)
	
def XNOR_Control(list_predecessorCC0,list_predecessorCC1):
	return (min((list_predecessorCC0[0]+list_predecessorCC1[1]),(list_predecessorCC0[1]+list_predecessorCC1[0]))+1,
			min(sum(list_predecessorCC0),sum(list_predecessorCC1))+1)


	
def AND_NAND_Obser(list_predecessorCC0,edgeCO):
	Observability_list=[]
	for i in list_predecessorCC0:
		list_temp =copy.deepcopy(list_predecessorCC0)
		list_temp.remove(i)
		sum1=sum(list_temp) + edgeCO +1
		Observability_list.append(sum1)
	return Observability_list
	

def OR_NOR_Obser(list_predecessorCC1,edgeCO):
	Observability_list=[]
	for i in list_predecessorCC1:
		list_temp =copy.deepcopy(list_predecessorCC1)
		list_temp.remove(i)
		sum1=sum(list_temp) + edgeCO +1
		Observability_list.append(sum1)
	return Observability_list


def XOR_XNOR_Obser(list_predecessorCC1,list_predecessorCC0,edgeCO):
	Observability_list=[]
	for i in range(len(list_predecessorCC1)):
		list_temp1 =copy.deepcopy(list_predecessorCC1)
		list_temp2 =copy.deepcopy(list_predecessorCC0)
		del list_temp1[i]
		del list_temp2[i]
		sum1=min(sum(list_temp1),sum(list_temp2)) + edgeCO +1
		Observability_list.append(sum1)
	return Observability_list

def NOT_Obser(edgeCO):
	list_temp=[]
	list_temp.append(edgeCO +1)
	return list_temp

list_predecessorCC0	=[1,2]	
list_predecessorCC1 =[3,4]


#print AND_Control(list_predecessorCC0,list_predecessorCC1)
#print AND_NAND_Obser([1,2,3],1)
#print OR_NOR_Obser([1,10,20],5)
#print NOT_Obser(10)
#output =stuck_at_1('0')
#print output
#print type(output)
