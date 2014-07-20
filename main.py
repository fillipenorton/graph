import copy

class Node(object):
  destinos = []
  pesos = []

class Application(object):
  records = {}
  vertices = {}
  vertices_degree = {}

  def init(self):
    while True:
      v1 = int(raw_input())
      if v1 == -1:
        self.printar()
        break
      elif v1 == -2:
        if self.is_eulerian():
          self.eu_trail()
        else:
          print 'Is NOT Eulerian'
          return 
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

  def is_eulerian(self):
    for r in self.vertices.keys():
      if self.vertices[r] % 2 != 0:
        return False
    return True

  # if not self.is_eulerian()
  #   return False

  def eu_trail(self, C=[], graph=None, v0=None):
    if not graph:
      graph = copy.deepcopy(self.records)
      v0 = graph.keys()[0]
      C = [v0]
      self.vertices_degree = copy.deepcopy(self.vertices)

    if v0 in graph.keys():
      for v in graph[v0].destinos:
        # import pdb;pdb.set_trace()
        graph_aux = copy.deepcopy(graph)
        graph_aux[v0].destinos.remove(v)
        if v0 == 4 and v == 3:
          import pdb;pdb.set_trace()

        if len(graph[v0].destinos) == 1:
          print 'Inseriu por causa do length'
          C.append(v)
          index = graph[v0].destinos.index(v)
          graph[v0].destinos.remove(v)
          graph[v0].pesos.pop(index)
          self.eu_trail(C=C, graph=graph, v0=v)
          break

        if not self.disconnect(origem=v0, destino=v, graph=graph_aux):
          print 'Inseriu pq nao desconecta'
          C.append(v)
          index = graph[v0].destinos.index(v)
          graph[v0].destinos.remove(v)
          graph[v0].pesos.pop(index)
          self.eu_trail(C=C, graph=graph, v0=v)
          break
    else:
      for key in graph.keys():
        if v0 in graph[key].destinos:
          for i in graph[key].destinos:
            graph_aux = copy.deepcopy(graph)
            graph_aux = graph_aux[key].destinos.remove(v0)
            if (self.vertices_degree[v0] == 1 or not self.disconnect(i, key, graph_aux)):
              C.append(key)
              index = graph[key].destinos.index(v0)
              graph[key].destinos.remove(v0)
              graph[key].pesos.pop(index)
              self.eu_trail(C=C, graph=graph, v0=key)
              break

    import pdb;pdb.set_trace()
    return C

  def disconnect(self, origem, destino, graph, past=None, start=None):
    # import pdb;pdb.set_trace()
    print 'origem: %s destino %s' % (origem,destino)
    if not graph:
      if origem == destino:
        print 'return true'
        return True
      else:
        print 'return false'
        return False

    if origem in graph.keys():
      for g in graph[origem].destinos:
        if g == destino:
          return False
        else:
          if len(graph[origem].destinos) == 1:
            graph[origem].destinos.remove(g)
            self.vertices_degree[origem] -= 1
          elif len(graph[origem].destinos) == 0:
            return True
          self.disconnect(g, destino, graph, past=origem)
    else: # elemento nao faz parte do nivel 1
      for key in graph.keys():
        if key != past:
          if origem in graph[key].destinos:
            if key == destino:
              return False
            else:
              self.vertices_degree[key] -= 1
              print '(3) origem %s key %s' % (origem, key)
              graph[key].destinos.remove(origem)
              self.disconnect(key, destino, graph)

  def printar(self):
    for k in self.records.keys():
      print 'index: %s | destinos: %s | pesos: %s' % (k, self.records[k].destinos, self.records[k].pesos)

    for v in self.vertices.keys():
      print 'vertice: %s | grau: %s' % (v, self.vertices[v])

app = Application()
app.init()
