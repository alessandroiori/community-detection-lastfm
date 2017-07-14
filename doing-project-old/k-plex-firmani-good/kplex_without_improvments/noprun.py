from snap import *
import copy
import sets
import itertools
from itertools import chain
import time
import cPickle
start = 0

k=10
def InitNeighbors(G):
    global neighbors_dic
    neighbors_dic={}
    for n in G.Nodes():
        neighbors_dic[n.GetId()] = set(n.GetOutEdges())

def my_copy(d):
    return cPickle.loads(cPickle.dumps(d, -1))
#print neighbors_dic

#def Minus(s1,s2):
#    return set(s1)-set(s2)

#def Substract(x,y):
#    ids = GetIds(y)
#    return (item for item in x if item.GetId() not in ids)


def findsubsets(S,m):
    return set(itertools.combinations(S, m))



#def GetIds(nodes):
#    return (NI.GetId() for NI in nodes)

def GrapMinusNodes(nodes,nodes1,nodes2):
    return (item for item in nodes if item.GetId() not in chain(nodes1,nodes2))

def GraphMinus(nodes,nodeIds):
    return (item for item in nodes if item.GetId() not in nodeIds)


def GetInducedGraph(G1,nodeIds):
    vectorOfInts = TIntV()
    for nodeId in nodeIds:
        vectorOfInts.Add(nodeId)
    return GetSubGraph(G1, vectorOfInts)


# return list of ints
# get an integer
def GetNeighbors(G,node):
    global neighbors_dic
    return neighbors_dic[node]
    if(type(node) is int):
        node = G.GetNI(node)
    return node.GetOutEdges()


def AddNode(H,u):
    result = my_copy(H)
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


# u is a TUNGraphNodeI or an int
def GetOnlyNeighbors(G, nodes ,u):
    global neighbors_dic
    v =   list(neighbors_dic[u].intersection(set(nodes)))
    #v.append(u.GetId())
    return v

def counter_value(counter):
    import re
    return int(re.search('\d+', repr(counter)).group(0))




# Check if by adding u to the kplex it remains a kplex
def IsExtendedSat(G,kplex,u,neighbors,nonneighbors,ng_dic):
    #print ",".join(str(x) for x in nonneighbors)
    n = nonneighbors.__len__()
    if(n>k-1):
        return False
    for v in nonneighbors:
        try:
            if ng_dic[v][1].__len__()==k-1:
                return False
        except KeyError:
            print u
            print "length %d: " % (ng_dic.__len__())
            print ",".join(str(x) for x in nonneighbors)
            print ",".join(str(x) for x in kplex)
            for x in ng_dic:
                print x
            b =l
    return True
#h1 = kplex[:]
#   h1.append(u)
#   return all(GetNonNeighbors(G,h1,v).__len__()<=k-1 for v in nonneighbors)

def IsExtendedSatAndConnected(G,kplex,u):
    #return IsExtendedSat(G,kplex,u)
    neighbors = GetOnlyNeighbors(G, kplex ,u)
    return neighbors.__len__()>1 and IsExtendedSat(G,kplex,u)

def GetNonNeighborsIfNotIn(G,nodes,u, no):
    neighbors = GetOnlyNeighbors(G, nodes ,u)
    return [n for n in nodes if n not in neighbors and n not in no]

def GetNonNeighbors(G,nodes,u):
    neighbors = GetOnlyNeighbors(G, nodes ,u)
    return [n for n in nodes if n not in neighbors and n != u]



# The function to look for connected components.
def connected_components(nodes, ng_dic):
    
    # List of connected components found. The order is random.
    result = []
    
    # Make a copy of the set, so we can modify it.
    nodes = set(nodes)
    # Iterate while we still have nodes to process.
    while nodes:
        
        # Get a random node and remove it from the global set.
        n = nodes.pop()
        
        # This set will contain the next group of nodes connected to each other.
        group = {n}
        
        # Build a queue with this node in it.
        queue = [n]
        
        # Iterate the queue.
        # When it's empty, we finished visiting a group of connected nodes.
        while queue:
            
            # Consume the next item from the queue.
            n = queue.pop(0)
            # Fetch the neighbors.
            neighbors = ng_dic[n][0]
            
            # Remove the neighbors we already visited.
            neighbors.difference_update(group)
            
            # Remove the remaining nodes from the global set.
            nodes.difference_update(neighbors)
            
            # Add them to the group of connected nodes.
            group.update(neighbors)
            
            # Add them to the queue, so we visit them in the next iterations.
            queue.extend(neighbors)
        
        # Add the group to the list of groups.
        result.append(group)
    
    # Return the list of groups.
    return result.__len__() == 1


# u is a actual node
def EnumAlmostSat(G, G_curr,u,local_ng_dic):
    #print "ng dic is %s len is %d" % (','.join(str(x) for x in local_ng_dic),local_ng_dic.__len__())
    #if(isinstance(u,TUNGraphNodeI)):
    u = u.GetId()
    if(G_curr.__len__()==0):
        local_ng_dic[u] = (set(),set())
        yield ([u] ,local_ng_dic)
        return
    neighbors = GetOnlyNeighbors(G,G_curr,u)
    if neighbors.__len__()==0:
        yield (G_curr ,local_ng_dic)
        local_ng_dic ={}
        local_ng_dic[u] = (set(),set())
        yield ([u] ,local_ng_dic)
        return
    nonneighbors = [n for n in G_curr if n not in neighbors]
    if(IsExtendedSat(G,G_curr,u,neighbors,nonneighbors,local_ng_dic)):
        new_list = G_curr[:]
        new_list.append(u)
        local_ng_dic[u] = (set(neighbors),set(nonneighbors))
        for v in neighbors:
            local_ng_dic[v][0].add(u)
        for v in nonneighbors:
            local_ng_dic[v][1].add(u)
        yield  (new_list,local_ng_dic)
        return
    yield (G_curr ,local_ng_dic)
    len = nonneighbors.__len__()
    s = min(k-1,len-1)
    for nnI in  findsubsets(nonneighbors,s):
        nnE = set(nonneighbors)-set(nnI)
        nn_nnI = list(nonneighbors)
        for n in nnI:
            nn_nnI.extend(GetNonNeighbors(G,G_curr,n))
        for i in range(1,s+1):
            for fix in findsubsets(nn_nnI,i):
                U = [n for n in G_curr if n not in fix and n not in nnE]
                neighbors_in_U = [n for n in U if n in neighbors]
                nonneighbors_in_U = [n for n in U if n in nonneighbors]
                if neighbors_in_U.__len__()==0:
                    return
                local_ng_dic_copy ={}
                for x in U:
                    x_ng = [y for y in local_ng_dic[x][0] if y in U]
                    x_nonng = [y for y in local_ng_dic[x][1] if y in U]
                    local_ng_dic_copy[x] = (set(x_ng),set(x_nonng))
                if(IsExtendedSat(G,U,u,neighbors_in_U,nonneighbors_in_U,local_ng_dic_copy)):
                    U.append(u)
                    local_ng_dic_copy[u] = (set(neighbors_in_U),set(nonneighbors_in_U))
                    #print "ng local_ng_dic_copy is %s len is %d" % (','.join(str(x) for x in local_ng_dic_copy),local_ng_dic_copy.__len__())
                    for v in neighbors_in_U:
                        local_ng_dic_copy[v][0].add(u)
                    for v in nonneighbors_in_U:
                        local_ng_dic_copy[v][1].add(u)
                    if(connected_components(U,local_ng_dic_copy)):
                        yield (U,local_ng_dic_copy)
#return [G_curr , RemoveNonNeighbors(G_curr,u)]

def ExtendMax(G,H,ng_dic):
    result = H[:]
    #return result
    # Build a queue with this node in it.
    queue = H[:]
    # Iterate the queue.
    while queue:
        # Consume the next item from the queue.
        n = queue.pop(0)
        # Fetch the neighbors.
        neighbors = set(neighbors_dic[n])
        # Remove the neighbors we already visited.
        neighbors.difference_update(result)
        for u in neighbors:
            neighbors = GetOnlyNeighbors(G,result,u)
            nonneighbors = [n for n in result if n not in neighbors]
            if(result.__len__()<k):
                result.append(u)
                # Add them to the queue, so we visit them in the next iterations.
                queue.append(u)
                ng_dic[u] = (set(neighbors),set(nonneighbors))
                for v in neighbors:
                    ng_dic[v][0].add(u)
                for v in nonneighbors:
                    ng_dic[v][1].add(u)
            elif(IsExtendedSat(G,result,u,neighbors,nonneighbors,ng_dic)):
                result.append(u)
                # Add them to the queue, so we visit them in the next iterations.
                queue.append(u)
                ng_dic[u] = (set(neighbors),set(nonneighbors))
                for v in neighbors:
                    ng_dic[v][0].add(u)
                for v in nonneighbors:
                    ng_dic[v][1].add(u)
            if all(ng_dic[v][1].__len__()==k-1 for v in result):
                # chack only common neighbors
                candidate = result[0]
                for neighbor_of_candidate in GetNode(G,candidate).GetOutEdges():
                    if neighbor_of_candidate in ng_dic[candidate][0]:
                        continue
                    neighbors = GetOnlyNeighbors(G,result,neighbor_of_candidate)
                    nonneighbors = [n for n in result if n not in neighbors]
                    if(nonneighbors.__len__()>0):
                        continue
                    result.append(neighbor_of_candidate)
                    ng_dic[neighbor_of_candidate] = (set(neighbors),set(nonneighbors))
                    for v in neighbors:
                        ng_dic[v][0].add(neighbor_of_candidate)
                return result
    return result

clique_set = set()

def GraphToString(nodes):
    nodes.sort()
    return ','.join(str(x) for x in nodes)

#f = open('workfile', 'w')
def Init():
    global num
    num =0

stack =[]
count =0
initiated = False

def run(G, num_of_kplex, neighbors):
    Init()
    global neighbors_dic
    neighbors_dic = neighbors
    global stack
    stack =[]
    global partial_set
    partial_set =set()
    global clique_set
    clique_set = set()
    global count
    count =0
    global start
    start=time.time()
    num = RecursiveGen(G, [], 0,[],num_of_kplex)
    end = time.time()
    return end-start
    # print "num of duplication %d" % (num)
#print "running time: %f" % (end - start)
#print "num of k-plexes %d" % (clique_set.__len__())


def RecursiveGen(G, G_curr1, i,E1,num_of_kplex):
    i = num_of_kplex
    printed ={}
    while(i>=1):
        printed[i] =False
        i =i/10
    num =0
    partial_set =set()
    stack.append((G_curr1,{}))
    while stack.__len__()>0 :
        G_curr ,local_ng_dic = stack.pop()
        for u in GraphMinus(G.Nodes(),G_curr):
            for H,ng_dic in EnumAlmostSat(G.Nodes(), G_curr[:],u,my_copy(local_ng_dic)):
                H_s = GraphToString(H)
                if(H_s in partial_set):
                    num =num+1
                    continue
                partial_set.add(H_s)
                h = ExtendMax(G,H,ng_dic)
                #if isMaximal(G,h)!=True:
                #continue
                #gs_start = time.time()
                h_s = GraphToString(h)
                #gs_end =time.time()
                #print "to string took %f" % (gs_end - gs_start)
                if(h_s not in clique_set):
                    #global count
                    #count = count +1
                    #print("%d : %s "% (count,h_s))
                    #f.write("%s\n"%h_s)
                    clique_set.add(h_s)
                    #I_new = I[:]
                    #I_new.append(u)
                    i = num_of_kplex
                    while(i>=1):
                        if(printed[i] ==True):
                            break
                        if(clique_set.__len__()>=i):
                            end = time.time()
                            printed[i] =True
                            if(i>=num_of_kplex):
                                # print "running time for %f: %f" % (i,(end - start))
                                return num
                        else:
                            i =i/10
                    stack.append((h[:],my_copy(ng_dic)))
                else:
                    num =num+1
    return 5