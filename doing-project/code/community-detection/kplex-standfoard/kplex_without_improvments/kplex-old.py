from snap import *
import copy
import snap
import cProfile
import time
import prun2 as prun2
import sys
import os
import noprun as noprun
import prunconnected as prunconnected
import imp
import csv
import pretty_file

import argparse

parser = argparse.ArgumentParser(description='Arguments for enumerating k-plexes in a graph.')
parser.add_argument('--type',
                    help='What type of k-plexes to print. Can be one of the follwong: all,connected,unconnected.' ,default="connected")
parser.add_argument('--k',type=int,
                    help='How many non neighbors a node is allowed to have.',default=5)
parser.add_argument('--n',type=int,
                    help='Number of nodes in the graph.',default=1000000)
parser.add_argument('--m',type=int,
                    help='Number of edges in the graph.',default=10000000)
parser.add_argument('--num_of_kplex',type=int,help='Number of k-plexes to print.',default=1000)
parser.add_argument('--file',
                    help='Full path to the file where the graph is located.',default="")

parser.add_argument('--experiment',
                    help='Type of experiment to run can be one of the fllowing: comparison, nodes, edges, k, results, connected, non-synthetic. ',default="")
parser.add_argument('--folder',
                    help='Full path to the directory where the files describing the graph are located. Cannot be used together with --file',default="")


parser.add_argument('--output',
                    help='Name of output file for printed k-plexes',default="output_file")

args = parser.parse_args()

def GenG1():
    G1 = TUNGraph.New()
    G1.AddNode(1)
    G1.AddNode(2)
    G1.AddNode(3)
    G1.AddNode(4)
    G1.AddNode(5)
    G1.AddEdge(1,3)
    G1.AddEdge(2,3)
    G1.AddEdge(1,2)
    G1.AddEdge(4,2)
    return G1

def GenG():
    G1 = TUNGraph.New()
    G1.AddNode(1)
    G1.AddNode(2)
    G1.AddNode(3)
    G1.AddNode(4)
    G1.AddNode(5)
    G1.AddNode(6)
    G1.AddNode(7)
    G1.AddEdge(1,5)
    G1.AddEdge(1,2)
    G1.AddEdge(2,3)
    G1.AddEdge(3,6)
    G1.AddEdge(3,4)
    G1.AddEdge(3,7)
    G1.AddEdge(4,7)
    G1.AddEdge(4,6)
    G1.AddEdge(4,5)
    return G1

def TestGraphMinus():
    G1 = GenG1()
    G2 = TUNGraph.New()
    G2.AddNode(1)
    G2.AddNode(2)
    ids = module1.GetIds(G2.Nodes()) 
    for node in module1.GraphMinus(G1,ids):
        print node.GetId()


def TestIsExtendSat():
    return module1.IsExtendedSat(GenG1(),[1,2],3)

def TestIsExtendSatKplex():
    return kplexmodule.IsExtendedSat(GenG1(),[1,2],3)

def TestEnumAlmostSat():
    G1 = GenG1()
    result = module1.EnumAlmostSat(G1,[1,2],4)
    for x in result:
        print "new clique:"
        for y in x:
            print y

def InitNeighbors(G):
    neighbors_dic={}
    for n in G.Nodes():
        neighbors_dic[n.GetId()] = set(n.GetOutEdges())
    return neighbors_dic

def GenerateGraph():
    G1 = TUNGraph.New()
    for i in range(0,50):
        G1.AddNode(i)
    lines = [line.strip() for line in open('graphtemp.txt')]
    for line in lines:
        if(line.startswith("e")):
            leftIndex = line.index("(")
            rightIndex = line.index(")") 
            numbers = line[leftIndex+1:rightIndex]
            l = numbers.split(",")
            G1.AddEdge(int(l[0]),int(l[1]))
    return G1

def BuildGraphFromFile(file_name):
    print "Building graph from file %s..." % file_name
    G1 = TUNGraph.New()
    stack =set()
    lines = [line.strip() for line in open(file_name)]
    for line in lines:
        l = line.split('\t')
        if(int(l[0]) not in stack):
           G1.AddNode(int(l[0]))
           stack.add(int(l[0]))
        if( int(l[1]) not in stack):
           G1.AddNode(int(l[1]))
           stack.add(int(l[1]))
        G1.AddEdge(int(l[0]),int(l[1]))
        G1.AddEdge(int(l[1]),int(l[0]))
    return G1

def BuildGraphFromFiles(folder):
    #import os
    #folder = os.path.dirname(os.path.abspath(__file__))+'/'+folder
    print "Building graph from files in folder %s..." % folder
    G1 = TUNGraph.New()
    import os
    results=[]
    results += [each for each in os.listdir(folder) if each.endswith('.edges')]
    stack =set()
    for file_name in results:
        lines = [line.strip() for line in open(folder+'/'+file_name)]
        for line in lines:
            l = line.split(" ")
            if(int(l[0]) not in stack):
                G1.AddNode(int(l[0]))
                stack.add(int(l[0]))
            if( int(l[1]) not in stack):
                G1.AddNode(int(l[1]))
                stack.add(int(l[1]))
            G1.AddEdge(int(l[0]),int(l[1]))
    return G1




def TestRecursiveGen():
    Graph =  snap.GenRndGnm(snap.PUNGraph, 50, 100)
    for EI in Graph.Edges():
        print "edge (%d, %d)" % (EI.GetSrcNId(), EI.GetDstNId())
    module1.RecursiveGenClique(Graph,[1],0)


def comparisionWithStateOfArt():
    print "Graph is ready"
    
    b = open('comarisionWithStateOfArt.csv', 'w')
    a = csv.writer(b)
    data = [['Nodes', 'Edges', "k = 1", "k = 2", "k = 3", "k = 4"]]
    import all
    for n,m in [(1000, 14432), (2000, 28709), (4000, 58063), (8000, 116276 ),(16000, 231622) ]:
        print "Generating a random graph with %s nodes and %s edges" % (n, m)
        #G1 = BuildGraphFromFile('%sn_%sm' % (n,m))
        G1 = snap.GenRndGnm(snap.PUNGraph, n, m)
        neighbors_dic = InitNeighbors(G1)
        times = [n,m]
        for i in (1,2,3, 4):
            imp.reload(all)
            all.k = i
            time = all.run(G1, 100000, neighbors_dic, "")
            times.append(time)
        data.append(times)
    a.writerows(data)
    b.close()

    pretty_file.pretty_file("comarisionWithStateOfArt.csv", header=True, border=True, delimiter=",", new_filename ="comparisionWithStateOfArt.txt")

def differentNumberOfNodes():
    b = open('diffrent_number_of_nodes.csv', 'w')
    a = csv.writer(b)
    data = [["Number of nodes", "EnumIncExc", "enum"]]
    for i in (1,10, 100,1000,10000):
        times = []
        num_of_nodes = i*1000
        times.append(num_of_nodes)
        print "Building a random graph with %s nodes and %s edges." % (num_of_nodes, 10*num_of_nodes)
        G1 = snap.GenRndGnm(snap.PUNGraph, num_of_nodes, 10*num_of_nodes)
        neighbors_dic = InitNeighbors(G1)
        prunconnected.k=5
        time = prunconnected.run(G1, 1000, neighbors_dic, "")[0]
        times.append(time)
        noprun.k = 5
        time = noprun.run(G1, 1000, neighbors_dic)
        times.append(time)
        data.append(times)

    a.writerows(data)
    b.close()
    pretty_file.pretty_file("diffrent_number_of_nodes.csv", header=True, border=True, delimiter=",", new_filename ="diffrent_number_of_nodes.txt")
    print "Results can be found in: diffrent_number_of_nodes.csv"


def differentNumberOfEdges():
    b = open('diffrent_number_of_edges.csv', 'w')
    a = csv.writer(b)
    data = [["Number of edges", "EnumIncExc", "Enum"]]
    for i in (1000,10000,100000):
        times = []
        num_of_edges = i*1000
        print "Building a random graph with 1000000 nodes and %s edges." % num_of_edges
        G1 = snap.GenRndGnm(snap.PUNGraph, 1000000, num_of_edges)
        neighbors_dic = InitNeighbors(G1)
        print "Graph is ready"
        prunconnected.k=5
        time1 = prunconnected.run(G1, 1000, neighbors_dic, "")[0]
        noprun.k = 5
        time2 = noprun.run(G1, 10000, neighbors_dic)
        data.append([num_of_edges, time1,time2])
    a.writerows(data)
    b.close()
    pretty_file.pretty_file("diffrent_number_of_edges.csv", header=True, border=True, delimiter=",", new_filename ="diffrent_number_of_edges.txt")

def differentNumberOfResults():
    b = open('diffrent_number_of_results.csv', 'w')
    a = csv.writer(b)
    data = [["Number of results", "EnumIncExc", "Enum"]]
    print "Building a random graph with 1000000 nodes and 10000000 edges."
    G1 = snap.GenRndGnm(snap.PUNGraph, 1000000, 10*1000000)
    neighbors_dic = InitNeighbors(G1)
    for i in (1,10,100,1000,10000):
        times = []
        num_of_nodes = 1000000
        
        prunconnected.k=5
        time1 = prunconnected.run(G1, i, neighbors_dic, "")[0]
        noprun.k = 5
        time2 = noprun.run(G1, i, neighbors_dic)
        data.append([i, time1,time2])
    a.writerows(data)
    b.close()
    pretty_file.pretty_file("diffrent_number_of_results.csv", header=True, border=True, delimiter=",", new_filename ="diffrent_number_of_results.txt")



def differentNumberOfK():
    import noprun
    #import noprunun2
    b = open('diffrent_number_of_k.csv', 'w')
    a = csv.writer(b)
    data = [["k", "EnumIncExc", "Enum"]]
    print "Building a random graph with 1000000 nodes and 10000000 edges."
    G1 = snap.GenRndGnm(snap.PUNGraph, 1000000, 10*1000000)
    neighbors_dic = InitNeighbors(G1)
    for i in (1,5,25,100,1000):
        times = []
        num_of_nodes = 1000000
        prunconnected.k=5
        time1 = prunconnected.run(G1, 1000, neighbors_dic, "")[0]
        noprun.k = 5
        time2 = noprun.run(G1, 1000, neighbors_dic)
        data.append(["k = %s" % i, time1,time2])
    a.writerows(data)
    b.close()
    pretty_file.pretty_file("diffrent_number_of_k.csv", header=True, border=True, delimiter=",", new_filename ="diffrent_number_of_k.txt")


def synthetic():
    b = open('synthetic.csv', 'w')
    a = csv.writer(b)
    data = [["Data", "k=1", "k=5", "k=25", "k=100"]]
    for file_name in ("web-Stanford.txt", "ca-AstroPh.txt", "soc-LiveJournal1.txt", "cit-Patents.txt"):
        file = os.path.dirname(os.path.abspath(__file__))+'/graphs/'+file_name
        G1 = BuildGraphFromFile(file)
        neighbors_dic = InitNeighbors(G1)
        times = []
        times.append(file_name)
        for i in (1,5,25, 100):
            prun2.k= i
            time = prun2.run(G1, 1000, neighbors_dic, "")
            times.append(time)
        data.append(times)
    G1 = BuildGraphFromFiles("./graphs/twitter")
    neighbors_dic = InitNeighbors(G1)
    times = []
    times.append("twitter")
    for i in (1,5,25, 100):
        prun2.k= i
        time = prun2.run(G1, 1000, neighbors_dic, "")
        times.append(time)
    data.append(times)
    a.writerows(data)
    b.close()
    pretty_file.pretty_file("synthetic.csv", header=True, border=True, delimiter=",", new_filename ="synthetic.txt")


def find_kplex(G1):
    import prunning
    neighbors_dic = InitNeighbors(G1)
    print "Graph is ready"
    if(args.type=="unconnected" or args.type=="all"):
        prunning.k=args.k
        prunning.run(G1, args.num_of_kplex, neighbors_dic, args.output+"_unconnected")
    if(args.type=="connected" or args.type=="all"):
        prunconnected.k= args.k
        result = prunconnected.run(G1,args.num_of_kplex, neighbors_dic, args.output+"_connected")
        


def run():
    # Make usre the number of nodes and edges is valid.
    assert((args.n *(args.n -1))/2 >args.m)
    # Generate a random graph with n nodes and m edges.
    print "Generating a random graph with %s nodes and %s edges" % (args.n, args.m)
    G1 = snap.GenRndGnm(snap.PUNGraph, args.n, args.m)
    find_kplex(G1)


def runFromFile(file_name):
    G1 = BuildGraphFromFile(file_name)
    find_kplex(G1)


def runFromFolder(folder_name):
    G1 = BuildGraphFromFiles(folder_name)
    find_kplex(G1)


def createGraphAndWriteToFile():
    for n,m in [(1000, 14432), (2000, 28709), (4000, 58063), (8000, 116276 ),(16000, 131622) ]:
        G1 =  snap.GenRndGnm(snap.PUNGraph, n, m)
        f1 = open('%sn_%sm' % (n,m), 'w')
        for EI in G1.Edges():
            f1.write( "%d\t%d\n" % (EI.GetSrcNId(), EI.GetDstNId()))
#createGraphAndWriteToFile()
#exit()
if args.experiment == "comparison":
    comparisionWithStateOfArt()
    exit()
if args.experiment == "edges":
    differentNumberOfEdges()
    exit()
if args.experiment == "nodes":
    differentNumberOfNodes()
    exit()
if args.experiment == "results":
    differentNumberOfResults()
    exit()
if args.experiment == "connected":
    differentNumberOfResultsWithAllTypes()
    exit()

if args.experiment == "k":
    differentNumberOfK()
    exit()

if args.experiment == "non-synthetic":
    synthetic()
    exit()
if args.file != "":
    runFromFile(args.file)
elif args.folder != "":
    runFromFolder(args.folder)
else:
    run()

