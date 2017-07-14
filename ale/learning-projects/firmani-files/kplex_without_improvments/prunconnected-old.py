from snap import *
import copy
import sets
import itertools
from itertools import chain
import time
import cPickle
start = 0

k=3
neighbors_dic={}
def InitNeighbors(G):
    global neighbors_dic
    neighbors_dic={}
    for n in G.Nodes():
        neighbors_dic[n.GetId()] = set(n.GetOutEdges())

def my_copy(d):
    return cPickle.loads(cPickle.dumps(d, -1))


def findsubsets(S,m):
    return set(itertools.combinations(S, m))


def GrapMinusNodes(G1,nodes1,nodes2):
    return (item.GetId() for item in G1.Nodes() if item.GetId() not in chain(nodes1,nodes2))

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



#def EnumAlmostSat(G, G_curr,u):
#    if SatClique(G,G_curr)
#     yield G_curr

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

def _IsConnected(G,U):
    return True
    G1 =GetInducedGraph(G,U)
    return IsConnected(G1)


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
    if(G_curr.__len__()==0):
        local_ng_dic = {}
        local_ng_dic[u] = (set(),set())
        yield ([u] ,local_ng_dic)
        return
    neighbors = GetOnlyNeighbors(G,G_curr,u)
    if neighbors.__len__()==0:
        yield (G_curr ,local_ng_dic)
        local_ng_dic[u] = (set(),set())
        yield ([u] ,local_ng_dic)
        return
    if k == 1:
        neighbors.append(u)
        yield neighbors
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
    if k == 1:
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
    # Build a queue with this node in it.
    queue = H[:]
    result = H[:]
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
                # check only common neighbors
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



def GraphToString(nodes):
    nodes.sort()
    return ','.join(str(x) for x in nodes)

num=0
partial_set =set()
def Init():
    global num
    num =0

stack =[]
count =0
start
initiated = False
def run(G, num_of_kplex, neighbors, output_file):
    global neighbors_dic
    neighbors_dic = neighbors
    
    nodes = (node.GetId() for node in G.Nodes())
    print "Starts enumerating connected k-plexes.."
    global stack
    stack =[]
    global count
    count =0
    global partial_set
    partial_set =set()
    global clique_set
    clique_set = set()
    global start
    start=time.time()
    result = RecursiveGen(G,nodes, [], 0,[],num_of_kplex, output_file)
    end = time.time()
    #print "num of duplication %d" % (num)
    #print "Running time for enumerating %d kplexes: %f" % (clique_set.__len__(),(end - start))
    times = [end-start]
    times.extend(result)
    #print "===================================================================="
    return times
#print "num of k-plexes %d" % (clique_set.__len__())


def RecursiveGen(G,nodes, G_curr1, i,E1,num_of_kplex, output_file):
    if output_file!= "":
        f = open(output_file, 'w')
        print "Output will be found at %s" % (f.name)
    stack.append((G_curr1,E1,{}))
    i = num_of_kplex
    printed ={}
    result = []
    while(i>=1):
        printed[i] =False
        i =i/10
    while stack.__len__()>0 :
        G_curr,E ,local_ng_dic = stack.pop()
        for u in GrapMinusNodes(G,G_curr,E):
            for H,ng_dic in EnumAlmostSat(G, G_curr[:],u,my_copy(local_ng_dic)):
                H_s = GraphToString(H)
                if(H_s in partial_set):
                    continue
                partial_set.add(H_s)
                h = ExtendMax(G,H,ng_dic)
                #if isMaximal(G,h)!=True:
                #continue
                #gs_start = time.time()
                h_s = GraphToString(h)
                if(h_s not in clique_set):
                    #global count
                    #count = count +1
                    #print("%d : %s "% (count,h_s))
                    if output_file!= "":
                        f.write("%s\n"%h_s)
                    clique_set.add(h_s)
                    #I_new = I[:]
                    #I_new.append(u)
                    i = num_of_kplex
                    while(i>=1):
                        if(printed[i] ==True):
                            break
                        if(clique_set.__len__()>=i):
                            end = time.time()
                            print "Running time for enumerating %d kplexes: %f" % (i,(end - start))
                            printed[i] =True
                            result.append(end - start)
                            if(i>=num_of_kplex):
                                return result
                        else:
                            i =i/10
                    stack.append((h[:],E[:],my_copy(ng_dic)))
                #RecursiveGen(G,h,i,E)
                else:
                    global num
                    num =num+1
            E.append(u)