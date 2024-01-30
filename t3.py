from tkinter import *
from time import strftime
import time
import threading
import sys
import os


win=Tk()
win.geometry("700x350")
condition = 1
zeroTime = 0
run = True
Lb1 = True
Rb1 = False
LedList = [False for i in range(15)]
class bcolors:
    _B = '\033[94m'
    _Y = '\033[93m'
    _G = '\033[92m'
    _R = '\033[91m'
    ENDC = '\033[0m'

def my_start():
    #print("myStart")
    
    LedList[0] = True
    
    PrintLigths()
    xc = time.time_ns()/1000000
    counter = 0
    while run:
        counter += 1
        global condition
        global zeroTime
        mil = time.time_ns()/1000000
        if((mil - xc) > 1000):
            #SSprint(counter)
            counter = 0
            xc = mil
        if condition == 1:
            #print("Print")
            myLabel.config(text="print")
            for val in LedList:
                val = False
            PrintLigths()
        elif condition == 2:
            #print("Stage")
            myLabel.config(text="Stage")
            LedList[1] = True
            LedList[2] = True 
            PrintLigths()
            
            time.sleep(1)
            LedList[3] = True
            LedList[4] = True 
            PrintLigths()
        elif condition == 3:
            #print("CountDown")
            myLabel.config(text="CountDown")
            
            now = time.time_ns()/1000000
            
            time.sleep(2)
            LedList[5] = True
            LedList[6] = True 
            PrintLigths()
            
            time.sleep(0.5)
            LedList[5] = False
            LedList[6] = False 
            LedList[7] = True
            LedList[8] = True 
            PrintLigths()            
            time.sleep(0.5)
            LedList[7] = False
            LedList[8] = False 
            LedList[9] = True
            LedList[10] = True 
            PrintLigths()                 
            time.sleep(0.5)
            LedList[9] = False
            LedList[10] = False
            LedList[11] = True
            LedList[12] = True
            PrintLigths()    
            time.sleep(0.5)
            condition = 4
        elif condition == 4:
            myLabel.config(text="Results")

        
            

def PrintLigths():
    os.system('clear')
    
    global LedList
    lb1Text = 'X' if LedList[1] else ' '
    rb1Text = 'X' if LedList[2] else ' '
    lb2Text = 'X' if LedList[3] else ' '
    rb2Text = 'X' if LedList[4] else ' '
    
    ly1Text = 'X' if LedList[5] else ' '
    ry1Text = 'X' if LedList[6] else ' '
    ly2Text = 'X' if LedList[7] else ' '
    ry2Text = 'X' if LedList[8] else ' '
    ly3Text = 'X' if LedList[9] else ' '
    ry3Text = 'X' if LedList[10] else ' '
    
    lg1Text = 'X' if LedList[11] else ' '
    rg1Text = 'X' if LedList[12] else ' '
    lr1Text = 'X' if LedList[13] else ' '
    rr1Text = 'X' if LedList[14] else ' '
    
    print(f"{bcolors._B}------({lb1Text})-----------({rb1Text})------{bcolors.ENDC}")
    print(f"{bcolors._B}------({lb2Text})-----------({rb2Text})------{bcolors.ENDC}")
    print(f"{bcolors._Y}------({ly1Text})-----------({ry1Text})------{bcolors.ENDC}")
    print(f"{bcolors._Y}------({ly2Text})-----------({ry2Text})------{bcolors.ENDC}")
    print(f"{bcolors._Y}------({ly3Text})-----------({ry3Text})------{bcolors.ENDC}")
    print(f"{bcolors._G}------({lg1Text})-----------({rg1Text})------{bcolors.ENDC}")
    print(f"{bcolors._R}------({lr1Text})-----------({rr1Text})------{bcolors.ENDC}")
    


   
def next():
    global condition
    global zeroTime
    condition += 1
    if(condition > 4):
        condition = 1
    if(condition == 3):
        zeroTime = time.time_ns()/1000000

def prev():
    global condition
    condition -= 1
    if(condition < 1):
        condition = 4

def quitx():
    win.destroy()
    

BtnNext = Button(win, text="next", font="Arial, 12", command=next).pack()
BtnPrev = Button(win, text="prev", font="Arial, 12", command=prev).pack()
quitbtn = Button(win, text="quit", font="Arial, 12", command=quitx).pack()

myLabel = Label(win, text="")
myLabel.pack(pady=2)


Yellow1Label = Label(win, text="y1")
Yellow1Label.pack(pady=1)

Yellow2Label = Label(win, text="y2")
Yellow2Label.pack(pady=1)
Yellow3Label = Label(win, text="y3")
Yellow3Label.pack(pady=1)

GreenLabel = Label(win, text="g")
GreenLabel.pack(pady=1)



threading.Thread(target=my_start, daemon=True).start()

win.mainloop()