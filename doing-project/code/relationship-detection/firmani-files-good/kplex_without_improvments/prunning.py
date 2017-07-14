from snap import *
import copy
import sets
import itertools
from itertools import chain
import cPickle
import time
start = 0

k=3
neighbors_dic={}
def InitNeighbors(G):
    global neighbors_dic
    for n in G.Nodes():
        neighbors_dic[n.GetId()] = set(n.GetOutEdges())

def my_copy(d):
    return cPickle.loads(cPickle.dumps(d, -1))

def findsubsets(S,m):
    return set(itertools.combinations(S, m))

def GrapMinusNodes(G1,nodes1,nodes2):
    return (item.GetId() for item in G1.Nodes() if item.GetId() not in chain(nodes1,nodes2))

def GrapMinusNodes(G1,nodes1):
    comb = set(nodes1)
    return (item.GetId() for item in G1.Nodes() if item.GetId() not in comb)

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
    return IsExtendedSat(G,kplex,u)
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


# u is a actual node
def EnumAlmostSat(G, G_curr,u,local_ng_dic):
    #print "ng dic is %s len is %d" % (','.join(str(x) for x in local_ng_dic),local_ng_dic.__len__())
    if(G_curr.__len__()==0):
        local_ng_dic[u] = (set(),set())
        yield ([u] ,local_ng_dic)
        return
    neighbors = GetOnlyNeighbors(G,G_curr,u)
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
                local_ng_dic_copy ={}
                for x in U:
                    x_ng = [y for y in local_ng_dic[x][0] if y in U]
                    x_nonng = [y for y in local_ng_dic[x][1] if y in U]
                    local_ng_dic_copy[x] = (set(x_ng),set(x_nonng))
                if(IsExtendedSat(G,U,u,neighbors_in_U,nonneighbors_in_U,local_ng_dic_copy)):
                    U.append(u)
                    if(_IsConnected(G,U)):
                        local_ng_dic_copy[u] = (set(neighbors_in_U),set(nonneighbors_in_U))
                        #print "ng local_ng_dic_copy is %s len is %d" % (','.join(str(x) for x in local_ng_dic_copy),local_ng_dic_copy.__len__())
                        for v in neighbors_in_U:
                            local_ng_dic_copy[v][0].add(u)
                        for v in nonneighbors_in_U:
                            local_ng_dic_copy[v][1].add(u)
                        yield (U,local_ng_dic_copy)
#return [G_curr , RemoveNonNeighbors(G_curr,u)]

def ExtendMax(G,H,ng_dic):
    result = H[:]
    for u in GraphMinus(G,H):
        u= u.GetId()
        neighbors = GetOnlyNeighbors(G,result,u)
        nonneighbors = [n for n in result if n not in neighbors]
        if(result.__len__()<k):
            result.append(u)
            ng_dic[u] = (set(neighbors),set(nonneighbors))
            for v in neighbors:
                ng_dic[v][0].add(u)
            for v in nonneighbors:
                ng_dic[v][1].add(u)
        elif(IsExtendedSat(G,result,u,neighbors,nonneighbors,ng_dic)):
            result.append(u)
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

num=0
partial_set =set()
#f = open('workfile', 'w')
def Init():
    global num
    num =0

stack =[]
count =0
start
initiated= False
def run(G, num_of_kplex, neighbors, output_file):
    global neighbors_dic
    neighbors_dic = neighbors
    nodes = (node.GetId() for node in G.Nodes())
    print "Starts enumerating unconnected k-plexes..."
    global stack
    stack =[]
    global count
    count =0
    global partial_set
    partial_set =set()
    start=time.time()
    result = RecursiveGen(G,nodes, [], 0,num_of_kplex, output_file)
    end = time.time()
   
    times = [end-start]
    times.extend(result)
    #print "Running time for enumerating kplexes: %f" % (end - start)
    print "=========================================================="
    return times
#print "=========================================================="

def RecursiveGen2(G, G_curr, i,E,num_of_kplex):
    for u in GrapMinusNodes(G,G_curr,E):
        for H in EnumAlmostSat(G, G_curr[:],u):
            H_s = GraphToString(H)
            if(H_s in partial_set):
                continue
            partial_set.add(H_s)
            h = ExtendMax(G,H)
                #if isMaximal(G,h)!=True:
                #print "Error!!!!\n"
            #if(h.__len__() <=k):
            #   continue
            h_s = GraphToString(h)
            if(h_s not in clique_set):
                #print(h_s)
                #f.write("%s\n"%h_s)
                clique_set.add(h_s)
                if(clique_set.__len__()>=num_of_kplex):
                   end = time.time()
                   global start
                   print end - start
                # print num
                #sys.exit()
                RecursiveGen(G,h,i,E[:])
            else:
                global num
                num =num+1
        E.append(u.GetId())

def isMaximal(G,h):
    for w in h:
        nonneighbors = GetNonNeighbors(G,h,w)
        n = nonneighbors.__len__()
        if(n>k-1):
            return False
    for u in GraphMinus(G,h):
        u= u.GetId()
        nonneighbors = GetNonNeighbors(G,h,u)
        n = nonneighbors.__len__()
        #print "%d : %s" % (u, ",".join(str(x) for x in nonneighbors))
        if(n>k-1):
            continue
        h1 = h[:]
        h1.append(u)
        is_kplex = False
        for v in h:
            nonneighbors = GetNonNeighbors(G,h1,v)
            n = nonneighbors.__len__()
            if(n>k-1):
                is_kplex =True
                break
        if is_kplex == False:
            return False
    return True


def RecursiveGen(G,nodes, G_curr1, i,num_of_kplex, output_file):
    result = []
    if output_file != "":
        f = open(output_file, 'w')
        print "Output will be found at %s" % (f.name)
    stack.append((G_curr1,{}))
    count = 0
    printed ={}
    i = num_of_kplex
    while(i>=1):
        printed[i] =False
        i =i/10
    start=time.time()
    while stack.__len__()>0 :
        G_curr ,local_ng_dic = stack.pop()
        for u in GrapMinusNodes(G,G_curr):
            for H,ng_dic in EnumAlmostSat(G, G_curr[:],u,my_copy(local_ng_dic)):
                H_s = GraphToString(H)
                if H_s in partial_set:
                    continue
                partial_set.add(H_s)
                h = ExtendMax(G, H, ng_dic)
                h_s = GraphToString(h)
                if h_s not in clique_set:
                    clique_set.add(h_s)
                    if len(h) > k:
                        count = count + 1
                        if output_file != "":
                            f.write("%s\n" % h_s)
                        i = num_of_kplex
                        while i >= 1:
                            if printed[i] == True:
                                break
                            if count >= i:
                                end = time.time()
                                print "Running time for enumerating %d kplexes: %f" % (i,(end - start))
                                printed[i] =True
                                result.append(end - start)
                                if i >= num_of_kplex:
                                    return result
                            else:
                                i =i/10
                    stack.append((H[:],my_copy(ng_dic)))
                else:
                    global num
                    num =num+1
    end = time.time()
    print "Running time for enumerating %d kplexes: %f" % (count,(end - start))
    return result