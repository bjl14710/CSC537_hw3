from RedBlackTree import *
# from dcel1 import *
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


####

class Event:
    def __init__(self, x, y, is_left=True, is_intersection=False, other_end=None, label=None, pl=None, ps=None, sl = None, ss=None):
        self.x = x
        self.y = y
        self.is_left = is_left
        self.is_intersection = is_intersection
        self.other_end = other_end
        self.label = label
        # fields for intersection events
        self.plabel=pl
        self.psegment=ps
        self.slabel=sl
        self.ssegment=ss
    def __str__(self):
        return str(self.label) + ' ' + str(self.plabel) + ' ' + str(self.slabel)



####
    
def find_intersections(event):
    global myDCEL
    segs = []
    for i in range(0,len(myDCEL.faces),2):  # only take inner or outer face, not both
        h = myDCEL.faces[i].halfEdge
        while (h.next != myDCEL.faces[i].halfEdge):
            segs.append(((h.tail.x, h.tail.y),(h.next.tail.x, h.next.tail.y)))
            h = h.next
        segs.append(((h.tail.x, h.tail.y),(h.next.tail.x, h.next.tail.y)))
            
    print(segs)
    drawSegments(segs)
    # find_inters(segs)



def makeMonotone(P):
    D = DCEL( )
    Q = RedBlackTree()
    label = 0
    sortedPoints = sorted(P, key = lambda x: x[0]) #sorting by x, so we can just use sorted like this.
    for p in sortedPoints: # points in polygon
        Q.insert(p) #insert the vertecies from left to right
    while not Q.is_empty():
        min_node = Q.minimum()
        Q.delete(min_node) 
        handleVertex(min_node) #geometric primative to decide what to do for the type of vertex
    return Q


def computeAngle(V,left,right):
    xDiffLeft = (left[0]-V[0])
    yDiffLeft = (left[1]-V[1])
    xDiffRight = (right[0]-V[0])
    yDiffRight = (right[1]-V[1])
    a_mag = sqrt(xDiffLeft^2+yDiffLeft^2)
    b_mag = sqrt(xDiffRight^2+yDiffRight^2)
    a_b_dot = xDiffLeft*xDiffRight + yDiffLeft*yDiffRight
    theta = a_b_dot/(a_mag*b_mag)

    return theta

def vertexType(v, mid):
    if computeAngle(v, left, right) < 180 and v[1] < mid:
        return START     #less than 180 and on left side
    elif computeAngle(v, left, right) > 180 and v[1] < mid:
        return SPLIT   
    elif computeAngle(v, left, right) < 180 and v[1] > mid:
        return END
    elif computeAngle(v, left, right) > 180 and v[1] > mid:
        return MERGE
    else:
        return REGULAR

def handleVertex(v):
    # if, else, etc. por los vertecies diferencias.
    # check left and right neighbors

    return


def intersect(p1, p2, p3, p4, xlow, xhigh):
    # *** need to implement *** 
    # 
    # Is this the code for when we hit an intersection?
    # or for finding it?   
    m1 = slopeOf((p1,p2))
    m2 = slopeOf((p3,p4))

    B1 = find_B(p1, m1)
    B2 = find_B(p3, m2)

    if m1 == None or m2 == None or B1 == None or B2 == None:
        return 
    if(m1-m2 == 0):
        return 
    x = (B2-B1)/(m1-m2)
    y = m1*((B2-B1)/(m1-m2))+B1
    if x < xhigh and x>xlow:
        return x,y
    return



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






# =========================================
root = Tk()
root.title("DCEL Test")
root.geometry(str(YSIZE)+'x'+str(YSIZE)) #("800x800")

canvas = Canvas(root, width=YSIZE, height=YSIZE, bg='#FFF', highlightbackground="#999")
canvas.bind("<Button-1>", find_intersections)
canvas.grid(row=0, column=0)


def timeSegmentIntersections():
    times = []
    
    for x in range(0,300,10):
        start_time = time.time()
        list2 = find_intersections(randomSegments[0:x])
        elapsed_time = time.time()-start_time
        times.append(elapsed_time)
    return times

P1 = [(100, 500), (400, 800), (600, 200), (100, 100)]
    
S1 = [[ P1[0], P1[1]],
     [ P1[1], P1[2]],
     [ P1[2], P1[3]],
     [ P1[3], P1[0]],
    ]
    
# myDCEL = DCEL()
# myDCEL.build_dcel(P1, S1)
# drawFaces(myDCEL)



    
#myDCEL = DCEL()
#myDCEL.build_dcel(P2, S2)
#drawFaces(myDCEL)
def connect(p):
    s = []
    for i in range(len(p)-1):
        s.append([p[i],p[i+1]])
    s.append([p[len(p)-1],p[0]])
    return s
test = ([100,300],[500,100],[600,500],[200,700],[100,600])

S = connect(test)    

makeMonotone(test)

# find_inters(S3)

# canvas.create_line(x, y, x+1, y, fill="#ff0000")

myDCEL = DCEL()
myDCEL.build_dcel(test, S)
#drawFaces(myDCEL)




# randomSegments = [((random.randint(100, 300), random.randint(100, 300)),(random.randint(100, 300), random.randint(100, 300))) for _ in range(300)]

# complexityPoints = []
# complexityPoints = timeSegmentIntersections()
# plt.plot(range(0,300,10),complexityPoints)
# #plt.plot(range(2),complexityPoints)
# plt.xlabel('size: N')
# plt.ylabel('time(S)')
# plt.title('Run Time for DCEL Intersections')
# plt.show()



root.mainloop()
