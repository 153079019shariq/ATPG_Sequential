class Impl_Stack:
	def __init__(self):
         self.items1 = []
         self.items2 = []

	def isEmpty(self):
         return (self.items1  == []  and self.items2 == [])

	def push(self, key,value):
		self.items1.append(key)
		self.items2.append(value)
		
	def pop(self):
         return (self.items1.pop(),self.items2.pop())

	def peek(self):
         return (self.items1[len(self.items1)-1],self.items2[len(self.items2)-1])

	def complement_top_stack(self):
		self.items2[len(self.items2)-1]	=str(int (not int(self.items2[len(self.items2)-1])))
		
	def display_stack(self):
		for i in range(len(self.items1)):
				print self.items1[i],self.items2[i]
		
	
	def size(self):
         return len(self.items1)


#~ s=Impl_Stack()
#~ 
#~ s.push(('G4', 'G9'),'1')
#~ s.push(('G1', 'G2'),'0')
#~ 
#~ [edge,val]=s.peek()
#~ print edge 
#~ print val
#~ 
#~ s.complement_top_stack()
#~ print s.peek()
#~ 
#~ s.display_stack()

#~ s.push(True)
#~ print(s.size())
#~ print(s.isEmpty())
#~ s.push(8.4)
#~ print(s.pop())
#~ print(s.pop())
#~ print(s.size())
