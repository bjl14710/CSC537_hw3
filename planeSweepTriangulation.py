from RedBlackTree import *
import math 
import random
from tkinter import *
from DCEL import *
import time
import matplotlib.pyplot as plt



YSIZE = 1000
PSIZE = 4
colors = ['red', 'green', 'blue', 'yellow']
color_idx = 0


# implementar la línea de barrido

# triangulatar cuando recibimos un vertice de merge

def makeMonotone(P):
    return



def connect(p):
    s = []
    for i in range(len(p)-1):
        s.append([p[i],p[i+1]])
    s.append([p[len(p)-1],p[0]])
    return s

def drawSegments(S):
    for s in S:
        drawLine(s[0], s[1], 'black')

def drawFaces(dcel):
    global color_idx
    for f in dcel.faces:
        print('polygon')
        verts = []
        h = f.halfEdge
        while (h.next != f.halfEdge):
            print((h.tail.x, h.tail.y), end="->")
            verts.append(h.tail.x)
            verts.append(YSIZE - h.tail.y)
            h = h.next
        verts.append(h.tail.x)
        verts.append(YSIZE - h.tail.y)
        print('\nverts ', verts)
        canvas.create_polygon(verts, outline='black', fill=colors[color_idx], width=2)    
        color_idx = (color_idx + 1) % 4
        print('\n')

def drawLine(p1, p2, color):
    p1 = (p1[0], YSIZE - p1[1])
    p2 = (p2[0], YSIZE - p2[1])
    canvas.create_line(p1, p2, fill=color)

def drawPoint(point):
    p = (point[0], YSIZE - point[1])
    canvas.create_oval(p[0] - PSIZE, p[1] - PSIZE, p[0] + PSIZE, p[1] + PSIZE, fill='red', w=2)

def drawpoints(points):
    for i in points:
        drawPoint(i)
    

root = Tk()
root.title("DCEL Test")
root.geometry(str(YSIZE)+'x'+str(YSIZE)) #("800x800")


test = ([0,0],[5,0],[5,5],[0,5])

S = connect(test)    


canvas = Canvas(root, width=YSIZE, height=YSIZE, bg='#FFF', highlightbackground="#999")
canvas.bind("<Button-1>", drawpoints(test))
canvas.grid(row=0, column=0)


myDCEL = DCEL()
myDCEL.build_dcel(test,S)
drawFaces(myDCEL)

root.mainloop()