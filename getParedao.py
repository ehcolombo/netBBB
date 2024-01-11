#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import igraph
import os.path
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
		return 0.0
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
		return 1
	if(w==7):
		return 1
	if(w==8):
		return 0.5
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


###################################################33
N_participantes = 0
Participantes_0 = []
Participantes = []


filename = "./data/BBB Stats - paredao-atual"+".csv"

data = open(filename,"r",encoding="utf8")


for line in data:
	col = line.split(",")
	Participantes.append(col[0])

N_participantes = len(Participantes)


print(Participantes)

### create igraph

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
data.seek(0)
for line in data:
	col = line.split(",")
	g.add_edge(g.vs.find(label=col[0].rstrip()), g.vs.find(label=col[1].rstrip()), weight=5.0, color="#b10026" )
		#print(i,j,A[i][j])

visual_style = {}
out_name = "plot/paredao_atual.png"
# Set bbox and margin
h=1200
w=1200
m=30
visual_style["bbox"] = (h,w)
visual_style["margin"] = 200
# Set vertex
visual_style["vertex_color"] = 'white'
visual_style["vertex_size"] = 100
visual_style["vertex_label_size"] = 22
# Set edges
visual_style["edge_curved"] = True
visual_style["edge_width"] = g.es['weight']
visual_style["edge_color"] = g.es['color']
visual_style["edge_arrow_size"] = 1.5
# Set the layout
my_layout = g.layout_kamada_kawai()
visual_style["layout"] = my_layout
# Plot the graph
plot(g, out_name, **visual_style)

# Overlay
font = ImageFont.truetype("DejaVuSans.ttf", 25)
img = Image.open(out_name)			
d1 = ImageDraw.Draw(img)
d1.text((m, m), "Paredão 14 (22 de Março)",anchor="lt", fill=(0, 0, 0),font=font)	
d1.text((h-m, w-m), "@analisebbb21", anchor="rb", fill=(0, 0, 0),font=font)	
img.save(out_name)
#img = Image.open(out_name)
#img_lgd = Image.open("./legend.png")		
#img.paste(img_lgd, (1100,0))
#img.save(paredao.png)

