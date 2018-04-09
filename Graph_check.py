class Vertex:
	def __init__(self, n):
		self.name = n
		self.neighbors = list()
	
	def add_neighbor(self, v):
		if v not in self.neighbors:
			self.neighbors.append(v)
			self.neighbors.sort()

class Graph:
	vertices = {}
	edges1	=[]
	
	def add_vertex(self, vertex):
		if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
			self.vertices[vertex.name] = vertex
			#print self.vertices[vertex.name].neighbors 
			return True
		else:
			return False
	
	def add_edge(self, u, v):
		if u in self.vertices and v in self.vertices:
			# my YouTube video shows a silly for loop here, but this is a much faster way to do it
			self.vertices[u].add_neighbor(v)
			self.vertices[v].add_neighbor(u)
			return True
		else:
			return False
			
	#~ def vertices_edges(self):
		#~ print "self.vertices.keys()"
		#~ A_list =self.vertices.keys()
		#~ 
		#~ print A_list
		#~ for i in A_list:
			#~ print i
			#~ print self.vertices[i].neighbors
			#~ in_edge_list =[] 
			#~ for j in self.vertices[i].neighbors:
				#~ 
					#~ in_edge_list.append(i)
			#~ print "in_edge_list" ,in_edge_list
		
		
	
	def print_graph(self):
		
		for key in sorted(list(self.vertices.keys())):
			for val in self.vertices[key].neighbors:
				print(key,val )
				self.edges1.append((key,val))
		
			#break

	def out_edge(self,k):
			list_out_edge=[]
			print self.edges1
			for j in self.edges1:
				if(k in j[0]):
					if(j[1] not in list_out_edge):
						list_out_edge.append((k,j[1]))
			print list_out_edge
	
	
	def in_edge(self,k):
			list_in_edge=[]
		
			for j in self.edges1:
				if(k in j[1]):
					if (j[0] not in list_in_edge):
						list_in_edge.append((j[0],k))
			print list_in_edge
	
			
g = Graph()
# print(str(len(g.vertices)))
a = Vertex('A')
g.add_vertex(a)
g.add_vertex(Vertex('B'))


for i in range(ord('A'), ord('K')):
	g.add_vertex(Vertex(chr(i)))

edges = ['AB', 'AE', 'BF', 'CG', 'DE', 'DH', 'EH', 'FG', 'FI', 'FJ', 'GJ', 'HI']
for edge in edges:
	g.add_edge(edge[:1], edge[1:])
	
#g.vertices_edges()

g.print_graph()
g.out_edge('A')
g.in_edge('H')
