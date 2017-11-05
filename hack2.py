#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 10:56:22 2017

@author: christy
"""

import networkx as nx
import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
plt.interactive(False)

#using csv
def create_graph(index,file):
    G=nx.Graph()

    f = open(file)
    reader = csv.reader(f)
    counter=0
    for edge in reader:
        a=int(edge[0])
        b=int(edge[1])
        c=int(edge[2])
        d=int(edge[3])
        if index==0:
            G.add_edge(a,b,label=counter)
        elif index==1:
            G.add_edge(c,d,label=counter)
        counter=counter+1
    f.close()
    return G

#using txt (with spaces)
def create_graph_txt(index,file):
    G=nx.Graph()
    f = open(file)
    lines=f.readlines()
    counter=0
    for edge in lines:
        edge=edge.split()
        a=int(edge[0])
        b=int(edge[1])
        c=int(edge[2])
        d=int(edge[3])
        if index==0:
            G.add_edge(a,b,label=counter)
        elif index==1:
            G.add_edge(c,d,label=counter)
        counter=counter+1
    f.close()
    return G

#using csv

#edge map is the crosswalk between blue and black(primal paths)
def create_edge_map(index,m_primal,file):
    edge_map=-1*np.ones((m_primal,m_primal),dtype=np.int)
    f = open(file)
    reader = csv.reader(f)
    counter=0
    for edge in reader:
        a=int(edge[0])
        b=int(edge[1])
        c=int(edge[2])
        d=int(edge[3])
        if index==0:
            edge_map[c,d]=a
            edge_map[d,c]=a
        elif index==1:
            edge_map[c,d]=b
            edge_map[d,c]=b
    f.close()
    return edge_map

#using txt
def create_edge_map_txt(index,m_primal,file):
    edge_map=-1*np.ones((m_primal,m_primal),dtype=np.int)

    f = open(file)
    lines=f.readlines()
    counter=0
    for edge in lines:
        edge=edge.split()
        a=int(edge[0])
        b=int(edge[1])
        c=int(edge[2])
        d=int(edge[3])
        if index==0:
            edge_map[c,d]=a
            edge_map[d,c]=a
        elif index==1:
            edge_map[c,d]=b
            edge_map[d,c]=b
    f.close()
    return edge_map

def get_population_data(m,file):
    population_data=np.zeros(m)
    f = open(file)
    reader = csv.reader(f)
    counter=0
    for node in reader:
        pop=int(node[0])
        population_data[counter]=pop
        counter=counter+1
    return population_data

def compute_population_score(m,k,population_ideal,population_data,districting):
    district_populations=np.zeros(k)
    for index in range(m):
        district_populations[int(districting[index])]+=population_data[index]
    pop_score=sum((district_populations-population_ideal)**2)
    return pop_score

def compute_compactness_score(m,k,area_data,perimeter_data,districting,conflicted_edges):
    #ToDo
    for district in districting:
        area = 1
        perimeter = 1
    return 0

def get_area_data(m,file):
    area_data=np.zeros(m)
    f = open(file)
    reader = csv.reader(f)
    counter=0
    for node in reader:
        area=int(node[0])
        area_data[counter]=area
        counter=counter+1
    return area_data

def get_perimeter_data(m_primal,file):
    perimeter_data=np.zeros((m_primal,m_primal))
    f = open(file)
    reader = csv.reader(f)
    for edge in reader:
        a=int(edge[0])
        b=int(edge[1])
        p=int(edge[2])
        perimeter_data[a][b]=p
        perimeter_data[b][a]=p
    return perimeter_data


if __name__ == '__main__':
    k=2
    example_file=r"C:\DATA\Exhaust\exhausting_splits-master\exhausting_splits-master\simple2_graph_edge_map.csv"
    G_dual=create_graph(0,example_file) #adjacency map (blue map)
    G_primal=create_graph(1,example_file) #primal = drawing paths (black map)
    nx.draw(G_dual)
    plt.draw()
    plt.show(block=True)
    nx.draw(G_primal)
    plt.draw()
    plt.show(block=True)
#    example_file="squares_graph_edge_map.txt"
#    G_dual=create_graph_txt(0,example_file)
#    G_primal=create_graph_txt(1,example_file)

    m=len(G_dual.nodes()) # number of dual nodes (or the number of precincts)
    m_primal=len(G_primal.nodes()) #number of nodes in the path graph
    #m_primal=40 #for squares_graph example
    pop_ideal=m/float(k)
#    edge_map_0=create_edge_map(0,m_primal,example_file)
#    edge_map_1=create_edge_map(1,m_primal,example_file)

    edge_map_0=create_edge_map(0,m_primal,example_file)
    edge_map_1=create_edge_map(1,m_primal,example_file)

    #population_data=get_population_data(m,r"C:\DATA\Exhaust\exhausting_splits-master\exhausting_splits-master\simple_graph_population.csv")
    #area_data=get_area_data(m,"C:\DATA\Exhaust\exhausting_splits-master\exhausting_splits-master\simple_graph_area.csv")
    #perimeter_data=get_perimeter_data(m_primal,r"C:\DATA\Exhaust\exhausting_splits-master\exhausting_splits-master\simple_graph_perimeter.csv")
    #population_total=sum(population_data)
    #population_ideal=population_total/float(k)

    #simple boundary nodes
    # boundary_nodes_primal=[0,1,2,3,4] #making a list of nodes - if shape changes, this needs to be hard-coded in - we need to know how many
    #simple2 boundary nodes
    boundary_nodes_primal=[9,15,10,11,13,14,9,5,4,17,16,2,9]


    districtings=[]
    districtings_conflicted_edges=[]
    conflicted_edges=np.zeros((m_primal,m_primal))
    for node1 in boundary_nodes_primal:
        for node2 in boundary_nodes_primal:
            if node1<node2:
                #print('here a')
                #print(node1)
                #print(node2)
                simple_paths=list(nx.all_simple_paths(G_primal,node1,node2))
                for simple_path in simple_paths:
                    #print('here b')
                    #print(simple_path)
                    G2=G_dual.copy() #copy the adjacency map so we can delete edges from it
                    districting=np.zeros(m)
                    for index in range(len(simple_path)-1):
                        edge=(simple_path[index],simple_path[index+1])
                        #print(edge)
                        edge2=(edge_map_0[edge[0],edge[1]],edge_map_1[edge[0],edge[1]])
                        #print(edge2)
                        G2.remove_edge(edge2[0],edge2[1])
                        conflicted_edges[edge2[0],edge2[1]]=1
                        conflicted_edges[edge2[1],edge2[0]]=1
                    G2_districts=list(nx.connected_components(G2)) #returns a graph generator - a list of two graphs: dist 0 and dist 1


                    for index in range(2):
                        for node in G2_districts[index]:
                            districting[node]=index
                    districtings.append(districting)
                    districtings_conflicted_edges.append(conflicted_edges)
                    print('districting:')
                    print(districting)
                    print G2_districts[0]

                    # distgraph = nx.Graph(list(G2_districts[0]))
                    # distgraph2 = nx.Graph(list(G2_districts[1]))
                    # nx.draw(distgraph)
                    # plt.draw()
                    # plt.show(block=True)
                    # nx.draw(distgraph2)
                    # plt.draw()
                    # plt.show(block=True)

    #create metagraph
    G_metagraph=nx.Graph()
    for i in range(len(districtings)):
        print "here"
        for j in range(len(districtings)):
            print "here2"
            districting1=districtings[i]
            print districting1
            districting2=districtings[j]
            print districting2
            if sum(abs(districting1-districting2))==1:
                G_metagraph.add_edge(i,j)

    nx.draw(G_metagraph)
    plt.draw()
    plt.show(block=True)

print "done"

# evaluate score for each districting

    # num_districtings=len(districtings)
    # scores=np.zeros((num_districtings,2))
    # for districting in districtings:
    #     conflicted_edge=districtings_conflicted_edges[index]
    #     scores[index][0]=compute_population_score(m,k,population_ideal,population_data,districting)
    #     scores[index][1]=compute_compactness_score(m,k,area_data,perimeter_data,districting,conflicted_edges)
    #     index+=1
    #
