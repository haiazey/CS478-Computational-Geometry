import tkinter as tk
from tkinter import ttk
from tkinter import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import convex 

LARGE_FONT= ("Verdana", 12)
style.use("ggplot")

clustered = False
no_of_points = 1000
is_start = True

class Project(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        tk.Tk.wm_title(self, "The Convex Family")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = StartPage(container, self)
        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
 
def is_clustered(is_clustered):
	global clustered
	clustered = is_clustered
	
def create_pts(no):
	global no_of_points
	no_of_points = no
	global is_start
	is_start = False
	print("here")
	
def g_s():
	convex.main_gui(no_of_points,clustered,1,0)
def j_m():
	convex.main_gui(no_of_points,clustered,1,1)
def q_h():
	convex.main_gui(no_of_points,clustered,1,2)
def m_s():
	convex.main_gui(no_of_points,clustered,1,3)
	
class StartPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		
		w = Scale(self, from_=1000, to=1000000,orient=HORIZONTAL)
		w.pack()
		
		check = ttk.Checkbutton(self, text="clustered",command=lambda: is_clustered(True))
		check.pack()
		
		check2 = ttk.Checkbutton(self, text="uniform",command=lambda: is_clustered(False))
		check2.pack()
		
		#print(w.get())
		b1 = tk.Button(self, text ="Create Points", command=lambda: create_pts(w.get()), bg="red")  
		b1.pack()
		
		button = ttk.Button(self, text="GRAHAM SCAN",command=lambda: g_s())
		button.pack()
		
		button2 = ttk.Button(self, text="JARVIS MARCH",command=lambda: j_m())
		button2.pack()
		
		
		button3 = ttk.Button(self, text="QUICK HULL",command=lambda: q_h())
		button3.pack()

		button4 = ttk.Button(self, text="MERGE HULL",command=lambda: m_s())
		button4.pack()
		
		
"""
class Graham(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graham Scan", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
        #f = Figure(figsize=(5,5), dpi=100)
        #a = f.add_subplot(111)
        #a.clf()
        global no_of_points
        print("graham")
        pts = no_of_points
        global clustered
        c = clustered
        print(c)
        #a.clear()
        convex.main_gui(pts,c,1,0)
        #if is_start == False:
        #	convex.main_method(clustered, 1, 0, no_of_points,10000,0,a)
        

        #canvas = FigureCanvasTkAgg(f, self)
        #f.canvas.draw()
        #canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        #toolbar = NavigationToolbar2TkAgg(canvas, self)
        #toolbar.update()
        #canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

class Jarvis(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Jarvis Mno_of_pointsarch", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
        
        
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.clear
        #convex.main_method(clustered, 1, 1, no_of_points,10000,0,a)
        

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
class Quick(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Quick Hull", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        if is_start == False:
        	convex.main_method(clustered, 1, 2, no_of_points,10000,0,a)
        

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
class Merge(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Merge Hull", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        f = Figure(figsize=(5,5), dpi=200)
        a = f.add_subplot(111)
        
        #convex.main_method(clustered, 1, 3, no_of_points,10000,0,a)
        #a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
"""
app = Project()
#ani = animation.FuncAnimation(f, animate, interval=2000)
app.mainloop()
