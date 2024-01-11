#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import igraph
import os.path
import sys
from os import path
from igraph import *
from PIL import Image, ImageDraw, ImageFont


weights = []
weights.append("") #0
weights.append("💔") #1
weights.append("💣") #2
weights.append("😡") #3
weights.append("🤮") #4
weights.append("🐍") #5
weights.append("🍌") #6
weights.append("🌱") #7
weights.append("😀") #8
weights.append("💖") #9
#
n_emojis = len(weights)


day = int(sys.argv[1])

def getEdgeColor(w):
	if(w==0):
		return "black"
	if(w==1):
		return "#9d24ea"
	if(w==2):
		return "#383838"
	if(w==3):
		return "#f03a17"
	if(w==4):
		return "#12970f"
	if(w==5):
		return "#bbd90a"
	if(w==6):
		return "#e19a00"
	if(w==7):
		return "#7caf1f"
	if(w==8):
		return "#ffc83d"
	if(w==9):
		return "#f34788"


def getEdgeWeight(w):
	if(w==0):
		return 0.01
	if(w==1):
		return 5
	if(w==2):
		return 5
	if(w==3):
		return 5
	if(w==4):
		return 5
	if(w==5):
		return 5
	if(w==6):
		return 2
	if(w==7):
		return 2
	if(w==8):
		return 2
	if(w==9):
		return 0.5


def getEdgePositiveness(w):
	if(w==0):
		return 0.0
	if(w==1):
		return -1.0
	if(w==2):
		return -1.0
	if(w==3):
		return -1.0
	if(w==4):
		return -1.0
	if(w==5):
		return -0.5
	if(w==6):
		return -0.25
	if(w==7):
		return 0.0
	if(w==8):
		return 0.5
	if(w==9):
		return 1.0

###############################################################################################

N_participantes = 0
Participantes_0 = []

output_statsTo = open("statsTo_participantes.dat","w+") ## como o participante é visto
output_statsFrom = open("statsFrom_participantes.dat","w+") ## como o participante ve a casa
output_statsNetwork = open("statsNetwork_alldays.dat", "w+") ## stats da rede no tempo




filename = "./data/BBB Stats - "+str(day)+".csv"
if path.exists(filename):
	input_data = open(filename,"r",encoding="utf8")

	line = input_data.readline()
	col = line.split(",")

	date = col[0]
	Participantes = col[1:]

	N_participantes = len(Participantes)

	print("Dia: "+date+" "+"| Participantes: "+str(N_participantes))

	# remove linebreak from last name
	Participantes[-1]=Participantes[-1].rstrip()

	# adjancy matrix array-type
	A = np.zeros((N_participantes,N_participantes))

	# get adjancy matrix FULL
	for i in range(0,N_participantes): #from	
		line = input_data.readline()	
		col = line.split(",")		
		for j in range(1,N_participantes+1): #to					
			for k in range(0,n_emojis): ## emoji to number (weights list)			
				if col[j].rstrip()==weights[k]:								
					A[i][j-1]=k #adjust to linewidth. use k for state-dependent							
	
	#### SAVE STATS IN TIME (network)
	# save temperature: mais alta mais tenso
	temp = 0.0	
	for i in range(0,N_participantes):
		for j in range(0,N_participantes):
			temp = temp + (-getEdgePositiveness(A[i][j])+1.0)/2.0 ## goes from 0 (bads) to 1 (goods)			
	
	#normalize temp (max happiness)
	temp = temp/(N_participantes*(N_participantes - 1))
	output_statsNetwork.write(str(day) + "\t" + str(temp) + "\t")

	# get adjancy matrix sub - <3
	A_sub = np.zeros((N_participantes,N_participantes))
	#
	input_data.seek(0)	
	lines = input_data.readlines()[1:]		
	for i in range(0,N_participantes): #from-to			
		for j in range(1,N_participantes+1): #to-from					
			line1 = lines[i]				
			col1 = line1.split(",") # lista de conexoes de i
			line2 = lines[j-1]				
			col2 = line2.split(",") # lista de conexoes de j
			if col1[j].rstrip()=="💖" and col1[i+1].rstrip()==col2[j].rstrip(): # match <3
				A_sub[i][j-1]=1

	### create igraph

	# get igraph from adjancy matrix
	# Create a directed graph
	gs = Graph(directed=True)
	# Add 5 vertices
	gs.add_vertices(N_participantes)

	# Add ids and labels to vertices
	for i in range(len(gs.vs)):
		gs.vs[i]["id"]= i
		gs.vs[i]["label"]= str(Participantes[i])
	# Add edges
	for i in range(0,N_participantes):	#from
		for j in range(0,N_participantes):	#to	
			if(A_sub[i][j]==1):
				gs.add_edge(gs.vs.find(label=Participantes[i]), gs.vs.find(label=Participantes[j]), weight=1.0, color=getEdgeColor(A_sub[i][j]) )
			#print(i,j,A[i][j])
	output_statsNetwork.write(str(gs.transitivity_undirected()) + "\n")	

	# get igraph from adjancy matrix
	# Create a directed graph
	g = Graph(directed=True)
	# Add 5 vertices
	g.add_vertices(N_participantes)

	# Add ids and labels to vertices
	for i in range(len(g.vs)):
		g.vs[i]["id"]= i
		g.vs[i]["label"]= str(Participantes[i])
	# Add edges
	for i in range(0,N_participantes):	#from
		for j in range(0,N_participantes):	#to	
			g.add_edge(g.vs.find(label=Participantes[i]), g.vs.find(label=Participantes[j]), weight=getEdgeWeight(A[i][j]), color=getEdgeColor(A[i][j]) )
			#print(i,j,A[i][j])

	#check weights
	# for e in g.es:
	# 	print("weight %f\n" % e['weight'])

	visual_style = {}
	out_name = "plot/queridometro_dia_"+str(day)+".png"
	# bbox and margin
	h=1200
	w=1200
	m=30
	visual_style["bbox"] = (h,w)
	# Dynamic graph margin
	min_margin=100
	max_margin=300
	visual_style["margin"] = min_margin + (max_margin-min_margin)*float(day-3)/97
	# vertex
	visual_style["vertex_color"] = 'white'
	visual_style["vertex_size"] = 100
	visual_style["vertex_label_size"] = 22
	# edges
	visual_style["edge_curved"] = True
	visual_style["edge_width"] = g.es['weight']
	visual_style["edge_color"] = g.es['color']
	visual_style["edge_arrow_size"] = 1.5
	# layout
	my_layout = g.layout_fruchterman_reingold(weights=g.es['weight'])
	#my_layout = g.layout_kamada_kawai()
	visual_style["layout"] = my_layout
	
	# Plot graph
	plot(g, out_name, **visual_style)
	
	# Overlay
	font = ImageFont.truetype("DejaVuSans.ttf", 25)
	img = Image.open(out_name)			
	d1 = ImageDraw.Draw(img)
	d1.text((m, m), "Dia "+str(day) + " | " + date, anchor="lt", fill=(0, 0, 0),font=font)	
	d1.text((h-m, w-m), "@analisebbb21", anchor="rb", fill=(0, 0, 0),font=font)	
	img.save(out_name)
	img = Image.open(out_name)
	img_lgd = Image.open("./legend.png")		
	img.paste(img_lgd, (1100, 0))
	img.save(out_name)
