# -*- coding: utf-8 -*-

import copy
from priodict import priorityDictionary
from itertools import cycle

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
          return
        else:
          print 'Is NOT Eulerian'
          return
      elif v1 == -3:
        o,f = self.check_odd()
        self.optimal_trail(origin=o, final=f)
        return
      elif v1 == -4:
        self.duplicate_edge()
        return


      v2 = int(raw_input())
      peso = int(raw_input())

      self.create(v1, v2, peso)

  def check_odd(self):
    v1 = v2 = None
    for r in self.vertices.keys():
      if self.vertices[r] % 2 != 0:
        if not v1:
          v1 = r
        else:
          v2 = r

    return v1,v2

  def create(self, v1, v2, peso):
    # import pdb; pdb.set_trace()
    if self.check(v1):
      self.records[v1].destinos.append(v2)
      self.records[v1].pesos.append(peso)
    elif self.check(v2):
      self.records[v2].destinos.append(v1)
      self.records[v2].pesos.append(peso)
    elif self.check_deep(v1):
      node = Node()
      node.destinos = [v1]
      node.pesos = [peso]
      self.records[v2] = node
    elif self.check_deep(v2):
      node = Node()
      node.destinos = [v2]
      node.pesos = [peso]
      self.records[v1] = node
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

  def countdown_degree(self, v1, v2):
    self.vertices_degree[v1] -= 1
    self.vertices_degree[v2] -= 1

  def check(self, v1):
    if v1 in self.records:
      return True
    return False

  def check_deep(self, v1):
    if len(self.records) > 0:
      for v in self.records.keys():
        if v1 in self.records[v].destinos:
          return True

    return False

  def is_eulerian(self):
    for r in self.vertices.keys():
      if self.vertices[r] % 2 != 0:
        return False
    return True

  def eu_trail(self, C=[], graph=None, v0=None):
    if not graph:
      graph = copy.deepcopy(self.records)
      v0 = graph.keys()[0]
      C = [v0]
      self.vertices_degree = copy.deepcopy(self.vertices)

    if v0 in graph.keys(): # v0 is between keys
      if len(graph[v0].destinos) == 1:
          print 'Inseriu pq tem apenas um destino'
          v = graph[v0].destinos[0]
          C.append(v)
          index = graph[v0].destinos.index(v)
          graph[v0].destinos.remove(v)
          graph[v0].pesos.pop(index)
          self.countdown_degree(v1=v0, v2=v)
          self.eu_trail(C=C, graph=graph, v0=v)
      else:
        graph_aux = copy.deepcopy(graph) # deep copy to pass graph_aux per params
        for v in graph[v0].destinos:
          #import pdb;pdb.set_trace()
          graph_aux[v0].destinos.remove(v)
          print 'enviou pro not_disconnect [1]'
          graph_d = copy.deepcopy(graph_aux)
          if (v in graph_aux[v0].destinos) or (self.not_disconnect(origem=v0, destino=v, graph_d=graph_d)):
            print 'Inseriu pq nao desconecta'
            C.append(v)
            index = graph[v0].destinos.index(v)
            graph[v0].destinos.remove(v) # remove from Graph only if
            graph[v0].pesos.pop(index)
            self.countdown_degree(v1=v0, v2=v)
            self.eu_trail(C=C, graph=graph, v0=v)
            break
    else: # v0 is on the deep
      for key in graph.keys():
        if v0 in graph[key].destinos:
          if self.vertices_degree[v0] == 1:
            print 'Inseriu no else por 1 destino'
            C.append(key)
            index = graph[key].destinos.index(v0)
            graph[key].destinos.remove(v0)
            graph[key].pesos.pop(index)
            self.countdown_degree(v1=v0, v2=key)
            self.eu_trail(C=C, graph=graph, v0=key)
            break
          else:
            print 'Veio no else'
            graph_aux = copy.deepcopy(graph) # deep copy to pass graph_aux per params
            graph_aux[key].destinos.remove(v0)
            print 'enviou pro not_disconnect [2]'
            if (v0 in graph_aux[key].destinos) or self.not_disconnect(origem=key, destino=v0, graph_d=graph_aux):
              print 'Inseriu no not_disconnect [2]'
              C.append(key)
              index = graph[key].destinos.index(v0)
              graph[key].destinos.remove(v0)
              graph[key].pesos.pop(index)
              self.countdown_degree(v1=v0, v2=key)
              self.eu_trail(C=C, graph=graph, v0=key)
              break

    import pdb;pdb.set_trace()
    return C

  def not_disconnect(self, origem, destino, graph_d):
    # import pdb;pdb.set_trace()
    print 'origem: %s destino %s' % (origem,destino)

    if origem in graph_d.keys():
      if len(graph_d[origem].destinos) == 0:
        print 'entrou false [1]'
        return False

      for v in graph_d[origem].destinos:
        if v == destino:
          print 'entrou true 1'
          return True
        graph_d[origem].destinos.remove(v)
        return self.not_disconnect(origem=v, destino=destino, graph_d=graph_d)
    else:
      for key in graph_d.keys():
        if origem in graph_d[key].destinos:
          if key == destino:
            print 'entrou true 2'
            return True
          graph_d[key].destinos.remove(origem)
          return self.not_disconnect(origem=key, destino=destino, graph_d=graph_d)
  
  def find_value_in_destins(self, value):
    # return a tuple, where first value is the key, and second value is the index
    for r in self.records:
      for d in self.records[r].destinos:
        if value == d:
          index = self.records[r].destinos.index(d)
          return r, index
  
  def dijkstra(self, origin,final=None):
    D = {}  # dictionary of final distances
    P = {}  # dictionary of predecessors
    Q = priorityDictionary()   # est.dist. of non-final vert.
    Q[origin] = 0

    for v in Q:
      D[v] = Q[v]

      if v == final:
        break

      if v in self.records:
        for w in self.records[v].destinos:
          index = self.records[v].destinos.index(w)
          weight = D[v] + self.records[v].pesos[index]

          if w not in Q or weight < Q[w]:
            Q[w] = weight
            P[w] = v
      else:
        for w in self.records:
          if v in self.records[w].destinos:
            index = self.records[w].destinos.index(v)
            weight = D[v] + self.records[w].pesos[index]

            if w not in Q or weight < Q[w]:
              Q[w] = weight
              P[w] = v         

    return P

  def optimal_trail(self, origin, final):
    P = self.dijkstra(origin, final)
    trail = []
    while True:
      trail.append(final)
      if final == origin:
        break
      final = P[final]

    trail.reverse()
    print trail 
    return trail

  def duplicate_edge(self):
    # graph_duplicated = copy.deepcopy(self.records)
    o,f = self.check_odd()
    path = self.optimal_trail(origin=o, final=f)

    for idx, p in enumerate(path):
      if idx+1 == len(path): break
      
      nextelem = path[(idx + 1) % len(path)]
      
      if p in self.records.keys():
        self.records[p].destinos.append(nextelem)
        self.records[p].pesos.append(0)

      else:
        self.records[nextelem].destinos.append(p)
        self.records[nextelem].pesos.append(0)
      
      self.update_degree(p, nextelem)
    
    import pdb;pdb.set_trace()      
    self.eu_trail()


  def printar(self):
    for k in self.records.keys():
      print 'index: %s | destinos: %s | pesos: %s' % (k, self.records[k].destinos, self.records[k].pesos)

    for v in self.vertices.keys():
      print 'vertice: %s | grau: %s' % (v, self.vertices[v])

app = Application()
app.init()
