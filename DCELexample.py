from RedBlackTree import *
# from dcel1 import *
import math 
import random
from tkinter import *
from DCEL import *
import time
import matplotlib.pyplot as plt
import math
 


YSIZE = 1000
PSIZE = 4
colors = ['red', 'green', 'blue', 'yellow']
color_idx = 0


####
def getAngle(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang
 

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


def connect(p):
    s = []
    for i in range(len(p)-1):
        s.append([p[i],p[i+1]])
    s.append([p[len(p)-1],p[0]])
    return s

def makeMonotone(P):
    D = DCEL( )
    segments = connect(P)
    D.build_dcel(P, segments)
    hedges = D.hedges
    Q = RedBlackTree()
    label = 0
    sortedPoints = sorted(P, key = lambda x: x[0]) #sorting by x, so we can just use sorted like this.
    for p in sortedPoints: # points in polygon
        Q.insert(p) #insert the vertecies from left to right
    while not Q.is_empty():
        min_node = Q.minimum()
        Q.delete(min_node) 
        handleVertex(min_node) #geometric primative to decide what to do for the type of vertex
    return D


def computeAngle(V,left,right):
    xDiffLeft = (left[0]-V[0])
    yDiffLeft = (left[1]-V[1])
    xDiffRight = (right[0]-V[0])
    yDiffRight = (right[1]-V[1])
    a_mag = math.sqrt(xDiffLeft^2+yDiffLeft^2)
    b_mag = math.sqrt(xDiffRight^2+yDiffRight^2)
    a_b_dot = xDiffLeft*xDiffRight + yDiffLeft*yDiffRight
    theta = a_b_dot/(a_mag*b_mag)
    return theta

def izquierdaODerecha(seg):
    # for finding if a point is on the left or right
    # based on the next and previous segments of the polygon 
    if 1:
        return "LEFT"
    elif 2:
        return "RIGHT"
    return 

def vertexType(hedge):
    # if computeAngle(v, left, right) < 180 and dir == "LEFT":
    #     return "START"     #less than 180 and on left side
    # elif computeAngle(v, left, right) > 180 and dir == "LEFT":
    #     return "SPLIT"   
    # elif computeAngle(v, left, right) < 180 and dir == "RIGHT":
    #     return "END"
    # elif computeAngle(v, left, right) > 180 and dir == "RIGHT":
    #     return "MERGE"
    # else:
    #     return "REGULAR"
    if hedge.prev[0] > hedge.tail[0] and hedge.next[0] > hedge.tail[0]:
        return "MERGE"
    elif hedge.prev[0] < hedge.tail[0] and hedge.next[0] < hedge.tail[0]:
        return "END"
    else:
        if computeAngle(hedge.tail, hedge.prev, hedge.next) > math.pi:
            return "MERGE"
    return


    
def handleVertex(P):
    # if, else, etc. por los vertecies diferencias.
    # check left and right neighbors. Pass Vertex. 
    # Each thing is a node
    print(P)
    
    # tipo = vertexType(P, P.left, P.right, dir)    
    # We are moving left to right, sorted by x.
    # So the node will have a left and right if it is 

    return

def merge(Up,Bottom):
    # Sort upper and bottom halfs according to x. 
    sortedUp = sorted(Up, key = lambda x: x[0]) #sorting by x, so we can just use sorted like this.
    sortedDown = sorted(Bottom, key = lambda x: x[0]) #sorting by x, so we can just use sorted like this.
    sortedDown.reverse()
    return sortedUp + sortedDown
    # actual merging
    
def createUpperHull():
    return

def createLowerHull():
    return

def createHalf(pts,UorL):
    pointsOfHalfUpper = []
    pointsOfHalfLower = []
    firstHalf = []
    secondHalf = []
    # concatenate so we can cycle through at minimum number
    ptsTraverse = pts + pts
    minNumber = min(pts, key = lambda t:t[0])  #minimum x value point
    minNumberPos = pts.index(minNumber) # where that point is
    i = minNumberPos
    # keep following the ptsTraverse until we start going back
    while ptsTraverse[i][0] < ptsTraverse[i+1][0]:
        i = i + 1
        firstHalf.append(ptsTraverse[i])
    while not(ptsTraverse[i] == ptsTraverse[minNumberPos]):
        i = i + 1
        secondHalf.append(ptsTraverse[i])
    # finding which one has the smallest y.
    if min(firstHalf,key = lambda t:t[1]) > min(secondHalf,key = lambda t:t[1]):
        # first half is upper half
        pointsOfHalfUpper = firstHalf
        pointsOfHalfLower = secondHalf
    else:
        pointsOfHalfUpper = secondHalf
        pointsOfHalfLower = firstHalf

    if UorL == 'U':
        return pointsOfHalfUpper
    elif UorL == 'L':
        return pointsOfHalfLower



def tmp_ps(P,seg,vt):
#     merge(Up,Bottom) #into x sorted order
    PDcel = DCEL()
    upperPts = createHalf(P,'U')
    lowerPts = createHalf(P,'L')
    
    # sortedPoints = sorted(P, key = lambda x: x) #sorting by x, so we can just use sorted like this.
    n = len(P)
    PDcel.build_dcel(P, seg)

    # Vt = Vt(:n//2,)
    # vt = P
    # VtDcel = Vt.build_dcel
    RC = []
    # RC.build_dcel((0,0),[(0,0),(0,0)])
    RC.append(P[0])
    RC.append(P[1])
    for i in range(1,n):
        # j = i
        if vt[i] in upperPts:
            if not (P[i] in upperPts):
                while len(RC) > 1:
                    drawLine(P[i], vt[i], 'black')
                    RC.pop()
                    # j = j + 1
                RC.pop()
                RC.append(vt[i])
                RC.append(P[i])
            else:
                while len(RC) > 1 and getAngle(vt[i-2],vt[i-1],vt[i]) > 180:
                     drawLine(P[i], vt[i-1], 'black')
                     RC.pop()
                RC.append(P[i]) 
        else:
            if not (P[i] in lowerPts):
                while len(RC) > 1:
                    drawLine(P[i], vt[i], 'black')
                    RC.pop()
                    # j = j + 1
                RC.pop()
                RC.append(vt[i])
                RC.append(P[i])
            else:
                while len(RC) > 1 and getAngle(vt[i-2],vt[i-1],vt[i]) > 180:
                     drawLine(P[i], vt[i-1], 'black')
                     RC.pop()
                RC.append(P[i])


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

test = ([100,300],[500,100],[600,500],[200,700],[150,600])

S = connect(test)    

makeMonotone(test)

# find_inters(S3)

# canvas.create_line(x, y, x+1, y, fill="#ff0000")
sortedPts = []
for i in test:
    sortedPts.append(i)

sortedPoints = sorted(test, key = lambda x: x)
# sortedPts.sorted(sortedPts, key = lambda x: x)
myDCEL = DCEL()
tmp_ps(test,S,sortedPoints)
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
