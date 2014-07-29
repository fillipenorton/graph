# -*- coding: utf-8 -*-

import copy
from priodict import priorityDictionary
import itertools
from heapq import nsmallest


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

      elif v1 == -5:
        self.step3()
        return


      v2 = int(raw_input())
      peso = int(raw_input())

      self.create(v1, v2, peso)


  def odd_vertex_set(self): # retorna quantidade de nós que tem grau ímpar
    a=[]
    for r in self.vertices.keys():
      if self.vertices[r] % 2 != 0:
        a.append(r)
    return a

  def check_odd(self): # retorna vértices que tem grau ímpar. Nesse caso só podem ter 2
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
      if len(graph[v0].destinos) == 0:
        graph.pop(v0, None)
        self.eu_trail(C=C, graph=graph, v0=v0)

      if len(graph[v0].destinos) == 1:
          # import pdb;pdb.set_trace()
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
          graph_aux[v0].destinos.append(v)
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


  def into_deep_side(self, value, graph_d):
    import pdb;pdb.set_trace()
    for key in graph_d.keys():
      if value in graph_d[key].destinos:
        return True

    return False

  def not_disconnect(self, origem, destino, graph_d):
    # import pdb;pdb.set_trace()
    print 'origem: %s destino %s' % (origem,destino)

    if origem in graph_d.keys():
      if len(graph_d[origem].destinos) == 0:
        if not self.into_deep_side(origem, graph_d):
          print 'entrou false [1]'
          return False
        else:
          graph_d.pop(origem, None)
          return self.not_disconnect(origem=origem, destino=destino, graph_d=graph_d)

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

  def transform_dict(self):
    graph_aux = {}

    for v in self.vertices:
      graph_aux[v] = []
      if v in self.records:
        for idx, x in enumerate(self.records[v].destinos):
          obj_dict = (x, self.records[v].pesos[idx])
          graph_aux[v].append(obj_dict)

    for r in self.records:
      for idx, d in enumerate(self.records[r].destinos):
        obj_dict = (r, self.records[r].pesos[idx])
        graph_aux[d].append(obj_dict)

    return graph_aux

  def dijkstra(self, start, target):
    graph = self.transform_dict()

    inf = 0
    for u in graph:
      for v ,w in graph[u]:
       inf = inf + w
    dist = dict([(u, inf) for u in graph])
    prev = dict([(u, None) for u in graph])
    q = graph.keys()
    dist[start] = 0

    def _distance(v):
      return dist[v]

    while q != []:
      u = min(q, key=_distance)
      q.remove(u)
      for v,w in graph[u]:
        alt = dist[u] + w
        if alt < dist[v]:
          dist[v] = alt
          prev[v] = u

    trav = []
    temp = target
    while temp != start:
      trav.append(prev[temp])
      temp = prev[temp]
    trav.reverse()
    trav.append(target)
    print trav
    return trav

  def optimal_trail(self, origin, final, weight=None):
    trail = self.dijkstra(origin, final)

    return trail

  def duplicate_edge(self, path=None):
    # graph_duplicated = copy.deepcopy(self.records)
    if not path:
      print 'nao tem path'
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


  def step3(self):
    odd_array = self.odd_vertex_set()
    trails = []
    tuples = itertools.combinations(odd_array, 2)

    # odd_array agora tem tuplas combinadads com os vértices ímpares

    for l in list(tuples):
      path, weight = self.optimal_trail(l[0], l[1], weight=True)
      obj = {
        weight: path
      }
      trails.append(obj)
    smallers = nsmallest(len(odd_array)-1, trails)

    for m in smallers:
      self.duplicate_edge(path=m.values()[0])

    import pdb;pdb.set_trace()
    self.eu_trail()


  def printar(self):
    for k in self.records.keys():
      print 'index: %s | destinos: %s | pesos: %s' % (k, self.records[k].destinos, self.records[k].pesos)

    for v in self.vertices.keys():
      print 'vertice: %s | grau: %s' % (v, self.vertices[v])

app = Application()
app.init()
