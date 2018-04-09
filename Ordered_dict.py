from collections import OrderedDict
dct = OrderedDict()
dct['a'] = 1
dct['b'] = 2
dct['c'] = 3



def pop(dct):
	dct.popitem()
	
	for i in dct:
		print i
		
pop(dct)
