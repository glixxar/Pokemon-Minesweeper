import tkinter as tk
from tkinter import Tk, Canvas, Frame, Button
from tkinter import BOTH, W, NW, SUNKEN, TOP, X, FLAT, LEFT
from PIL import Image, ImageTk
import tkinter.font as tkFont

""" POKEBALL_P = 'a3_images/full_pokeball.png'    
STOPWATCH = 'a3_images/clock.png'
GRASS = 'a3_images/unrevealed.png'





def create_grid(event=None):
    w = c.winfo_width() # Get current width of canvas
    h = c.winfo_height() # Get current height of canvas
    c.delete('grid_line') # Will only remove the grid_line
    
     # Creates all vertical lines at intevals of 100
    for i in range(0, w, 60): #this means 0 to 500 in
        c.create_line([(i, 0), (i, h)], tag='grid_line')
        

    # Creates all horizontal lines at intevals of 100
    for i in range(0, h, 60):
        c.create_line([(0, i), (w, i)], tag='grid_line')
    
    pos_x = 0
    pos_y = 0
    for i in range(0,600,60):
        for x in range(0,600,60):
            rec_tag = (pos_x,pos_y)
            #c.create_rectangle([x,i],[x+60,i+60],fill="dark green",tags=rec_tag)
            c.create_image(x+30,i+30,image=im,tags=rec_tag) 
            pos_x += 1
        pos_y += 1
        pos_x = 0

def press1(event):
    item = c.find_closest(event.x, event.y)[0]
    tags = c.gettags(item)
    tup= (tags[0],tags[1])
    print(tup)




root = tk.Tk()
fontStyle = tkFont.Font(family="Courier New", size=26,weight="bold")
banner = tk.Label(root,text="Pokemon: Got 2 Find Them All!",font=fontStyle,bg="light coral",fg="white")
banner.pack(side=tk.TOP)

c = tk.Canvas(root, height=600, width=600, bg='white')
c.pack()
d = tk.Canvas(root,height=120,width=600,bg='white')
d.pack(side=tk.BOTTOM)

button1 = Button(d, text = "Quit",anchor = W)
button1.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
button1_window = d.create_window(10, 10, anchor=NW, window=button1)



im = ImageTk.PhotoImage(Image.open(GRASS))
selection = tk.Frame(root,width=600, height=150,bg='white')

up = tk.Button(selection, text="New Game",width=8)
up.place(relx=0.9, rely=   0.4, anchor='s')

down = tk.Button(selection, text="Restart Game",width=10)
down.place(relx=0.9, rely=   0.7, anchor='s')

pokeball = ImageTk.PhotoImage(Image.open(POKEBALL_P ))
label = tk.Label(selection, image=pokeball)
label.place(relx=0.2, rely=   0.5, anchor='e')

timer = ImageTk.PhotoImage(Image.open(STOPWATCH))
t_label = tk.Label(selection, image=timer)
t_label.place(relx=0.6, rely=   0.5, anchor='e') 

selection.pack(side=tk.BOTTOM)

c.bind("<Button-1>", press1)

c.bind('<Configure>', create_grid)

root.mainloop() """

GRASS_R_0 = 'a3_images/zero_adjacent.png'
GRASS_R_1 = 'a3_images/one_adjacent.png'
GRASS_R_2 = 'a3_images/two_adjacent.png'
GRASS_R_3 = 'a3_images/three_adjacent.png'
GRASS_R_4 = 'a3_images/four_adjacent.png'
GRASS_R_5 = 'a3_images/five_adjacent.png'
GRASS_R_6 = 'a3_images/six_adjacent.png'
GRASS_R_7 = 'a3_images/seven_adjacent.png'
GRASS_R_8 = 'a3_images/eight_adjacent.png'

GRASS_DICT = {0:GRASS_R_0, 1:GRASS_R_1, 2:GRASS_R_2, 3:GRASS_R_3, 
4:GRASS_R_4, 5:GRASS_R_5, 6:GRASS_R_6, 7:GRASS_R_7, 8:GRASS_R_8}

print(GRASS_DICT[0])