#imports
from matplotlib import pyplot as plt
from random import randint
from math import atan2 
from math import pi
import numpy as np 
import time
from matplotlib.figure import Figure
import sys
sys.setrecursionlimit(50000)

MAX_AXIS = 10000000
MIN_AXIS = 0

def create_points(count,min_ax=MIN_AXIS, max_ax=MAX_AXIS):
    points = []
    for i in range(count):
        points.append( [randint(min_ax,max_ax),randint(min_ax,max_ax)])
    return points

def plot_result(a, time_res, points, color,hull = None,hull2 = None,merge =None):
    # plotting code https://pythonspot.com/matplotlib-scatterplot/
    x,y = [],[]
    x,y = zip(*points)
    #f = Figure(figsize=(5,5), dpi=100)
    #a = f.add_subplot(111)
    a.scatter(x,y,s = 2, c= color)

    #if convexhull
    if hull != None:
        for i in range(len(hull)):
            a.plot((hull[i][0],hull[(i+1)%len(hull)][0]),(hull[i][1],hull[(i+1)%len(hull)][1]), 'r')

    if hull2 !=None:
        for i in range(len(hull2)):
            a.plot((hull2[i][0],hull2[(i+1)%len(hull2)][0]),(hull2[i][1],hull2[(i+1)%len(hull2)][1]), 'b')

    if merge !=None:
        for i in range(len(merge)):
            a.plot((merge[i][0],merge[(i+1)%len(merge)][0]),(merge[i][1],merge[(i+1)%len(merge)][1]), 'g')
            
    #mng = a.get_current_fig_manager()
    #mng.full_screen_toggle()
    time_res= "time = "+str(time_res)
    a.title(time_res)
    a.show()
    


def calculatePolar(center,point):
    ys = point[1]-center[1] 	
    xs = point[0]-center[0]
    """
    if ( xs<0 and ys>0):
        xs = -xs
        angle = atan2(ys,xs)	
        angle += pi/2
    elif ( xs<0 and ys<0):
        xs = -xs
        ys = -ys
        angle = atan2(ys,xs)	
        angle += pi
    elif ( xs>0 and ys<0):
        ys = -ys
        angle = atan2(ys,xs)	
        angle += 3*pi/2
    else:"""
    angle = atan2(ys,xs)

    #angle= atan2(ys,xs)	
    #print( "angle: ", angle)

    distance =  ((xs)**2)+((ys)**2) 
    return angle,distance, point

def sort_angle(value):
    return value[0]
def sort_distance(value):
    return value[1]


def sort_coor(s):
    min_y = MAX_AXIS
    index = 0
    #print(s[0][1])
    for i in range(len(s)):

        if s[i][1] < min_y:
            min_y = s[i][1]
            index = i

    center = s.pop(index)
    #print("center " , center)
    polar_points = []

    for i in range(len(s)):
        polar_points.append(calculatePolar(center, s[i]))

    x = sorted(polar_points, key=sort_distance)
    y = sorted(x, key=sort_angle)

    points = []
    for i in range (len(y)):
        points.append(y[i][2])
    return points,center

def left_test( p0, p1, p2):
    det = p0[0]*p1[1]+p2[0]*p0[1]+p1[0]*p2[1]-p2[0]*p1[1]-p0[0]*p2[1]-p1[0]*p0[1]
    if det >= 0:
        return True
    else:
        return False

def deter( p0, p1, p2):
    det = p0[0]*p1[1]+p2[0]*p0[1]+p1[0]*p2[1]-p2[0]*p1[1]-p0[0]*p2[1]-p1[0]*p0[1]
    return det

def graham_scan(coords):
    sorted_list,center = sort_coor(coords)

    convex = [center, sorted_list[0]]

    for point in sorted_list[1:]:
        while left_test(convex[-2], convex[-1],point)== False:
            convex.pop(-1)
        convex.append(point)


    #plot_result(coords, '#d62728',convex)	

    return convex


def sort_jarvis(s,center,reverse):

    #print("center " , center)
    polar_points = []

    if reverse == False:
        for i in range(len(s)):
            if  s[i][1]-center[1] >= 0:
                polar_points.append(calculatePolar(center, s[i]))

    else:
        for i in range(len(s)):
            if  s[i][1]-center[1] <= 0:
                polar_points.append(calculatePolar(center, s[i]))

    x = sorted(polar_points, key=sort_distance)

    y = sorted(x, key=sort_angle, reverse = False)
    """if reverse == True:
        print("here")
        y = sorted(x, key=sort_angle, reverse = False)
    else: 
        z =[]
        for xs in x:
            if xs[0]>0:
                z.append(xs)
        y = sorted(z, key=sort_angle, reverse = False)"""
    points = []
    for i in range (len(y)):
        points.append(y[i][2])
        #print(y[i])
    return points	

def jarvis_march(coords):

    s = coords


    max_y = MIN_AXIS
    min_y = MAX_AXIS
    min_index = 0
    for i in range(len(s)):
        if s[i][1] <= min_y:
            min_y = s[i][1]
            min_index = i
        if s[i][1] >= max_y:
            max_y = s[i][1]
            max_index = i

    bottom = s[min_index]
    top = s[max_index]

    convex = [bottom]

    #print("pop", s.pop(min_index))
    #print("before while")

    while( np.array_equal(convex[-1],top) == False):
        s = sort_jarvis(s,convex[-1],False)
        convex.append(s.pop(0))
    s = coords

    while( np.array_equal(convex[-1],bottom) == False):
        s = sort_jarvis(s,convex[-1],True)
        convex.append(s.pop(0))
    #plot_result(coords, '#d62728',convex)	

    return convex

def create_subset(l,h,s):
    subset = []
    for p in s:
        if( left_test(l,h,p) == True):
            subset.append(p)
    return subset

def quickhull(s,l,r):
    if len(s) <= 2:
        return s

    index = 0
    convex = []
    h_dist = -1
    h = s[0]
    for i in range(len(s)):
        #print(index)
        dist = deter(l,r,s[i])
        #print(dist)
        if dist > h_dist:
            h_dist = dist
            h = s[i]
            index = i

    s_1 = create_subset(l,h,s)
    s_2 = create_subset(h,r,s)
    #print ( "s1:",len(s_1),"\n",s_1)
    #print ( "s2:",len(s_2),"\n",s_2)

    convex = convex + quickhull(s_1,l,h)
    res =  quickhull(s_2,h,r)
    res.remove(h)
    convex = convex+res

    return convex


def initialize_quickhull(coords,eps):
    s = sorted(coords, key = sort_angle)
    l0 = s[0]
    r0 = [s[0][0],s[0][1]-eps]


    result = quickhull(s,l0,r0)
    for i in result:
        if i == r0:
            result.remove(r0)

    #plot_result(coords, '#d62728',result)	

    return result

def diff(l1,l2):
    diff = [i for i in l1 if i not in l2]
    return diff	

def is_internal(p,hull):

    for i in range(len(hull)-1):
        if left_test(hull[i], hull[(i+1)%len(hull)], p) == False: 
            return False
    return True
def sort_coor_polar(s,center):

    #print("center " , center)
    polar_points = []

    for i in range(len(s)):
        polar_points.append(calculatePolar(center, s[i]))

    x = sorted(polar_points, key=sort_distance)
    y = sorted(x, key=sort_angle)

    points = []
    for i in range (len(y)):
        points.append(y[i][2])
    return points

def support_line(hull, p):
    u,v = None,None
    inc = []
    dec = []

    s = sort_coor_polar(hull,p)
    v = s.pop(0)
    u = s.pop(-1)


    for i in range(len(s)-1):
        if left_test(u,v,s[i])==True:
            inc.append(s[i])
        else: 
            dec.append(s[i])
    inc.append(u)
    inc.append(v)
    return inc

def step4(hull,hull2,p):
    inc = support_line(hull2,p)
    s = inc+ hull

    return s

def step3(hull,hull2,p):
    s = hull+hull2

    return s

def merge_hull( pts, pts2, hull, hull2):
    #step1
    differ = diff(pts,hull)
    p = differ[0]
    #step2
    sorted_list = []

    if is_internal(p,hull2) ==True:
        sorted_list = step3(hull,hull2,p)

    else:
        sorted_list = step4(hull,hull2,p)
        print("here")

    #step5
    convex = graham_scan(sorted_list)

    #plot_result(sorted_list, '#d62728',hull,hull2,convex)	

    return convex


def main_gui(NUMBER_COUNT,CLUSTERED,EPSILON,METHOD):
	hull = None
	hull2 = None
	merge = None
	time_res=0.0

	if METHOD != 3:
		if CLUSTERED == False:
		    coord = create_points(NUMBER_COUNT)
		else:
		    count = int(NUMBER_COUNT/2)
		    inter = int(MAX_AXIS/2)
		    pts = create_points(count, MIN_AXIS, inter)
		    pts2 = create_points(count, inter, MAX_AXIS)
		    coord = pts + pts2

		# graham	
		if METHOD == 0:
		    start = time.time()
		    hull=graham_scan(coord)
		    end = time.time()
		    time_res = (end-start)
		elif METHOD == 1: 
			start = time.time()
			hull=jarvis_march(coord)
			end = time.time()
			time_res = (end-start)
		elif METHOD == 2:
			start = time.time()		
			hull=initialize_quickhull(coord,EPSILON)
			end = time.time()
			time_res = (end-start)

		plot_result(plt,time_res,coord, '#d62728',hull)
	else:
		count = int(NUMBER_COUNT/2)

		if CLUSTERED == False:
		    pts = create_points(count)
		    pts2 = create_points(count)
		else:
		    pts = create_points(count, 0, 5000)
		    pts2 = create_points(count, 5000, 10000)
		start = time.time()
		hull=initialize_quickhull(pts,EPSILON)
		hull2=initialize_quickhull(pts2,EPSILON)
		merge=merge_hull( pts, pts2, hull, hull2)
		end = time.time()
		time_res = (end-start)
		coord = pts+pts2
		plot_result(plt, time_res,coord, '#d62728',hull,hull2,merge)
	#return a
	
def main():
    #####################   MAIN  ######################
	
	NUMBER_COUNT = 1000
	CLUSTERED = False
	#epsilon for quickhull
	EPSILON = 1
	# 0 = Graham 
	# 1 = Jarvis
	# 2 = Quick
	# 3 = Merge
	METHOD = 3
	hull = None
	hull2 = None
	merge = None
	time_res=0.0

	if METHOD != 3:
		if CLUSTERED == False:
		    coord = create_points(NUMBER_COUNT)
		else:
		    count = int(NUMBER_COUNT/2)
		    inter = int(MAX_AXIS/2)
		    pts = create_points(count, MIN_AXIS, inter)
		    pts2 = create_points(count, inter, MAX_AXIS)
		    coord = pts + pts2

		# graham	
		if METHOD == 0:
		    start = time.time()
		    hull=graham_scan(coord)
		    end = time.time()
		    time_res = (end-start)
		elif METHOD == 1: 
			start = time.time()
			hull=jarvis_march(coord)
			end = time.time()
			time_res = (end-start)
		elif METHOD == 2:
			start = time.time()		
			hull=initialize_quickhull(coord,EPSILON)
			end = time.time()
			time_res = (end-start)

		plot_result(plt,time_res,coord, '#d62728',hull)
	else:
		count = int(NUMBER_COUNT/2)

		if CLUSTERED == False:
		    pts = create_points(count)
		    pts2 = create_points(count)
		else:
		    pts = create_points(count, 0, 5000)
		    pts2 = create_points(count, 5000, 10000)
		start = time.time()
		hull=initialize_quickhull(pts,EPSILON)
		hull2=initialize_quickhull(pts2,EPSILON)
		merge=merge_hull( pts, pts2, hull, hull2)
		end = time.time()
		time_res = (end-start)
		coord = pts+pts2
		plot_result(plt, time_res,coord, '#d62728',hull,hull2,merge)

if __name__ == "__main__":
    main()
