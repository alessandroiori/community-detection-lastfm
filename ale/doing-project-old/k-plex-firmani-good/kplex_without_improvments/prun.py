from snap import *
import copy
import sets
import itertools
from itertools import chain
import time
start = 0

k=3
#def Minus(s1,s2):
#    return set(s1)-set(s2)

#def Substract(x,y): 
#    ids = GetIds(y) 
#    return (item for item in x if item.GetId() not in ids)


def findsubsets(S,m):
    return set(itertools.combinations(S, m))



#def GetIds(nodes):
#    return (NI.GetId() for NI in nodes)

def GrapMinusNodes(G1,nodes1,nodes2):
    return (item for item in G1.Nodes() if item.GetId() not in chain(nodes1,nodes2))

def GraphMinus(G1,nodeIds):
    return (item for item in G1.Nodes() if item.GetId() not in nodeIds)


def GetInducedGraph(G1,nodeIds):
    vectorOfInts = TIntV()
    for nodeId in nodeIds:
        vectorOfInts.Add(nodeId)
    return GetSubGraph(G1, vectorOfInts)


# return list of ints 
# get an integer
def GetNeighbors(G,node):
    if(type(node) is int):
        node = G.GetNI(node)
    return node.GetOutEdges()


def AddNode(H,u):
    result = copy.deepcopy(H)
    result.AddNode(u.GetId())
    for node in H.Nodes():
        if(u.IsNbrNId(node.GetId())):
            result.AddEdge(u.GetId(),node.GetId())
    return result


def GetNode(G,id):
    return G.GetNI(id)


#G_curr is a list of nodes ids!
def SatKplex(G,G_curr,node):
    d = G_curr.len()-1
    for id in G_curr:
        N = G.GetNI(id)
        if(d>N.GetOutDeg()+k-1):
            return False
    return True 



#def EnumAlmostSat(G, G_curr,u):
#    if SatClique(G,G_curr)
#     yield G_curr

# u is a TUNGraphNodeI or an int
def GetOnlyNeighbors(G, nodes ,u):
    if(type(u) is int):
        u = GetNode(G,u) 
    v =   list(set(u.GetOutEdges()).intersection(set(nodes)))
    v.append(u.GetId())
    return v
  
def counter_value(counter):
    import re
    return int(re.search('\d+', repr(counter)).group(0))




# Check if by adding u to the kplex it remains a kplex
def IsExtendedSat(G,kplex,u):
    nonneighbors = GetNonNeighbors(G,kplex,u)
    n = nonneighbors.__len__()
    if(n>k-1):
        return False
    return all(GetNonNeighbors(G,kplex,v).__len__()<k-1 for v in nonneighbors)

def IsExtendedSatAndConnected(G,kplex,u):
    return IsExtendedSat(G,kplex,u)
    neighbors = GetOnlyNeighbors(G, kplex ,u)
    return neighbors.__len__()>1 and IsExtendedSat(G,kplex,u)


def GetNonNeighbors(G,nodes,u):
    neighbors = GetOnlyNeighbors(G, nodes ,u)
    return [n for n in nodes if n not in neighbors]

def _IsConnected(G,U):
    return True
    G1 =GetInducedGraph(G,U)
    return IsConnected(G1)
    

# u is a actual node
def EnumAlmostSat(G, G_curr,u):
    if(isinstance(u,TUNGraphNodeI)):
        u = u.GetId()
    if(G_curr.__len__()==0):
        yield [u]
        return
    if(IsExtendedSat(G,G_curr,u)):
        new_list = G_curr[:]
        new_list.append(u)
        if(_IsConnected(G,new_list)):
            yield  new_list
            return
#yield G_curr
    neighbors = GetOnlyNeighbors(G,G_curr,u)
    nonneighbors = [n for n in G_curr if n not in neighbors]
    len = nonneighbors.__len__()
    s = min(k-1,len)
    if s ==1: #there is only one node that is a non neighbor
        n = nonneighbors[0]
        nn_nnI = GetNonNeighbors(G,G_curr,n)
        # choose node to fix n. n has exactly k-1 non neighbors
        for fix in nn_nnI:
            U = G_curr[:]
            U.remove(fix)
            U.append(u)
            yield U
        return
    st=time.time()
    for nnI in  findsubsets(nonneighbors,s):
        nnE = set(nonneighbors)-set(nnI)
        nn_nnI = list(nonneighbors)
        for n in nnI:
            nn_nnI.extend(GetNonNeighbors(G,G_curr,n))
        for i in range(1,s+1):
            for fix in findsubsets(nn_nnI,i):
                U = [n for n in G_curr if n not in fix and n not in nnE]
                if(IsExtendedSat(G,U,u)):
                    U.append(u)
                    if(_IsConnected(G,U)):
                        en = time.time()
                        global time_choose
                        time_choose = time_choose + en - st
                        yield U
                        st = time.time()
    #return [G_curr , RemoveNonNeighbors(G_curr,u)]
    
def ExtendMax(G,H):
    result = H[:]
    for u in GraphMinus(G,H):
        u= u.GetId()
        if(IsExtendedSatAndConnected(G,result,u)):
            result.append(u)
    return result

clique_set = set()

def GraphToString(nodes):
    nodes.sort()
    return ','.join(str(x) for x in nodes)

num=0
time_choose = 0
partial_set =set()
#f = open('workfile', 'w')
def Init():
    global num
    num =0

def run(G):
    start=time.time()
    RecursiveGen(G, [], 0,[])
    end = time.time()
    print end - start
    #print num
    #print clique_set.__len__()
    #print time_choose
    
def RecursiveGen(G, G_curr, i,E):
    for u in GrapMinusNodes(G,G_curr,E):
        for H in EnumAlmostSat(G, G_curr[:],u):
            H_s = GraphToString(H)
            if(H_s in partial_set):
                continue
            partial_set.add(H_s)
            h = ExtendMax(G,H)
            #if(h.__len__() <=k):
             #   continue
            h_s = GraphToString(h)
            if(h_s not in clique_set): 
                #print(h_s)
                #f.write("%s\n"%h_s)
                clique_set.add(h_s)
                #if(clique_set.__len__()>10):
                 #   end = time.time()
                  #  print end - start
                   # print num
                    #sys.exit()
                RecursiveGen(G,h,i,E)
        E.append(u.GetId())              

