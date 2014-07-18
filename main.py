
class Node(object):
	destinos = []
	pesos = []
	
class Application(object):
	records = {}
	vertices = {}
	
	def init(self):
		while True:
			v1 = int(raw_input())
			if v1 == -1:
				self.printar()
				break
			elif v1 == -2:
				self.is_eulerian_trail()
			v2 = int(raw_input())
			peso = int(raw_input())
			
			self.create(v1, v2, peso)
		
	def create(self, v1, v2, peso):
		# import pdb; pdb.set_trace()
		if self.check(v1):
			self.records[v1].destinos.append(v2)
			self.records[v1].pesos.append(peso)
		else:
			node = Node()
			node.destinos = [v2]
			node.pesos = [peso]
			self.records[v1] = node
		self.update_degree(v1, v2)
			
	def update_degree(self, v1, v2):
		degree = None
		if v1 in self.vertices:
			degree = self.vertices[v1]
			degree += 1
		else:
			degree = 1
		self.vertices[v1] = degree
		
		degree = None
		if v2 in self.vertices:
			degree = self.vertices[v2]
			degree += 1
		else:
			degree = 1
		self.vertices[v2] = degree					

	def check(self, v1):
		if v1 in self.records:
			return True
		return False
	
	def is_eulerian_trail(self):
		odd_count = 0
		for r in self.vertices.keys():
			if self.vertices[r] % 2 != 0:
				odd_count += 1
			if odd_count >= 1:
				print 'Nao eh euleriano'
				return False
		print 'Eh euleriano'
		return True
	
	def printar(self):
		for k in self.records.keys():
			print 'index: %s | destinos: %s | pesos: %s' % (k, self.records[k].destinos, self.records[k].pesos)
		
		for v in self.vertices.keys():
			print 'vertice: %s | grau: %s' % (v, self.vertices[v])
	
app = Application()
app.init()
