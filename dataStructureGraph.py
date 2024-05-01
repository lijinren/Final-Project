#!/usr/bin/env python
# coding: utf-8

# In[17]:


import locationBasedRecommendation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import networkx as nx
import matplotlib.pyplot as plt
import pyvis
from pyvis.network import Network


class Vertex:
  def __init__(self, key):
    self.id = key
    self.connectedTo = {}
    self.degree = 0
  def addNeighbor(self, nbr, weight=0):
    self.connectedTo[nbr] = weight
  def getId(self):
    return self.id
  def getWeight(self, nbr):
    return self.connectedTo[nbr]
  def getConnections(self):
    return self.connectedTo.keys()
  def calcDegree(self):
     self.degree = len(self.connectedTo.keys())
  
  def __str__(self):
    #return str(self.id) + ‘is connected to ‘ + str((x.id, x.weight) for x in self.connectedTo)
    return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])


class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertList

    def addEdge(self,f,t,weight=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], weight)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())


def main():
   df, cityList = locationBasedRecommendation.cleanData() 
   data = df.copy()
   net = Network()
   #add vertex
   name = []
   h = []
   k = 0
   for i in data['name']:
      k+=1
      name.append(i)
      h.append(k)
   net.add_nodes(h,label=name)

# Calculate cosine similarities between users processed input and reviews
   tfidfvec = TfidfVectorizer()
   vec = tfidfvec.fit(data["bag_of_words"])
   features = vec.transform(data["bag_of_words"])
   description_vector =  vec.transform(data['bag_of_words'])
   cos_sim = linear_kernel(description_vector, features)
   similarity = cos_sim

   for i in range(len(cos_sim[1])):
      for j in range(len(cos_sim[1])):
         similarity[i][j] = round(cos_sim[i][j]*10)

    
   #add edge
   a = 1
   edge = []
   for i in range(len(similarity[1])):
      for j in range(a,len(similarity[1])):
        a += 1
        if similarity[i][j] >= 1:
           temp = [i+1,j+1,similarity[i][j]]
           edge.append(temp)
   net.add_edges(edge) 

   net.show('dataStructure.html')
   net.save_graph('dataStructure.html')
   plt.show()


# In[ ]:




