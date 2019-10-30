#TODO Balacing,Charge,Discharge Werte in GUI, Variablen umbenennen,
#
#

#import serial
import time
import random
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import numpy as np

#Array zum Auflisten der Zeitintervale
t = []
#Startwert der Zeit
t0=0
#Zeitstempel als String
time_call = None
#Arrays zum Auflisten der eingelesenen Werte
arr_volt1 = []
arr_volt2 = []
arr_volt3 = []
arr_curr = []
#Uebergabe-Variable der eingelesenen Werte
ardu_volt1 = None
ardu_volt2 = None
ardu_volt3 = None
ardu_curr = None
#Uebergabevariable der Start-und Stopfunktion
startstop_var=None
balstartstop_var=None
ChargeDischarge_var=None
def volt1():
    global arr_volt1
    global t
    time_call = time.strftime("%Y%m%d-%H%M%S")
    np.savetxt("./export/"+time_call+"-voltage1.txt",np.column_stack((t,arr_volt1)), delimiter=",", fmt='%s', header=time_call+'-Voltage\s,V')
    return
def volt2():
    global arr_volt2
    global t
    time_call = time.strftime("%Y%m%d-%H%M%S")
    np.savetxt("./export/"+time_call+"-voltage2.txt",np.column_stack((t,arr_volt2)), delimiter=",", fmt='%s', header=time_call+'-Voltage\s,V')
    return
def volt3():
    global arr_volt3
    global t
    time_call = time.strftime("%Y%m%d-%H%M%S")
    np.savetxt("./export/"+time_call+"-voltage3.txt",np.column_stack((t,arr_volt3)), delimiter=",", fmt='%s', header=time_call+'-Voltage\s,V')
    return
def curr():
    global arr_curr
    global t
    time_call = time.strftime("%Y%m%d-%H%M%S")
    np.savetxt("./export/"+time_call+"-current.txt",np.column_stack((t,arr_curr)), delimiter=",", fmt='%s', header=time_call+'-Current\s,A')
    return
def allval():
    global arr_volt1
    global arr_volt2
    global arr_volt3
    global arr_curr    
    global t
    time_call = time.strftime("%Y%m%d-%H%M%S")
    np.savetxt("./export/"+time_call+"-BMS.txt",np.column_stack((t,arr_volt1,arr_volt2,arr_volt3,arr_curr)), delimiter=",", fmt='%s', header=time_call+'-t,V1,V2,V3,I')
    return
def ChargeDischarge(value):
    global ChargeDischarge_var
    ChargeDischarge_var = value
    if ChargeDischarge_var == 1:
        label_Ch = None
        label_Dis = Label(root, image=pic_discharge).place(x=800,y=10)
    elif ChargeDischarge_var == 0:
        label_Dis = None
        label_Ch = Label(root, image=pic_charge).place(x=800,y=10)
    return
def balstartstop(value):
    global balstartstop_var
    balstartstop_var = value
    return
def startstop(value):
    global startstop_var
    startstop_var = value
    return
def WarningReset():
    MsgBox = tk.messagebox.askquestion ('Reset Plots','Are you sure you want to reset the plots?',icon = 'warning')
    if MsgBox == 'yes':
       resetlists()


root = tk.Tk()
root.title("Monitoring")
root.config(background='white')
root.geometry("1000x700")


###Menubar##############
menu = Menu(root)
root.config(menu=menu)
exportmenu = Menu(menu)
menu.add_cascade(label="Export", menu=exportmenu)
exportmenu.add_command(label="Voltage1 to CSV", command=lambda:[volt1()])
exportmenu.add_command(label="Voltage2 to CSV", command=lambda:[volt2()])
exportmenu.add_command(label="Voltage3 to CSV", command=lambda:[volt3()])
exportmenu.add_command(label="Current to CSV", command=lambda:[curr()])
balmenu = Menu(menu)
menu.add_cascade(label="Balancing", menu=balmenu)
balmenu.add_command(label="Balancing ON", command=lambda:[print("Balancing ON"),balstartstop(1)])
balmenu.add_command(label="Balancing OFF", command=lambda:[print("Balancing OFF"),balstartstop(0)])
#testmenu = Menu(menu)
#menu.add_cascade(label="test", menu=testmenu)
#testmenu.add_command(label="lol", command=print(arr_volt1))
#########################

###Picture###############
pic_discharge = PhotoImage(file='./images/Discharge.png')
pic_charge = PhotoImage(file='./images/Charge.png')
pic_eet= PhotoImage(file='./images/eet-logo.png')
pic_tu = PhotoImage(file='./images/tu-logo.png')
label_eet = Label(root, image=pic_eet).pack(anchor="n")
#TODO Automatische Abfrage
#ser = serial.Serial('/dev/ttyUSB1', 9600)  # Linux

plt.ion()
fig = plt.figure()
plt.close()

sub1 = fig.add_subplot(221)
#sub1.set_xlabel('Time')
sub1.set_ylabel('Voltage Zelle 3')
sub1.plot(t, arr_volt1, 'b.-' , markersize = 5 )
sub1.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)
#sub1.set_ylim(2.8,3.4)

sub2 = fig.add_subplot(222)
#sub2.set_xlabel('Time')
sub2.set_ylabel('Voltage Zelle 2')
sub2.plot(t, arr_volt2, 'r.-' , markersize = 5 )
sub2.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)
#sub2.set_ylim(2.8,3.4)

sub3 = fig.add_subplot(223)
sub3.set_xlabel('Time')
sub3.set_ylabel('Voltage Zelle 1')
sub3.plot(t, arr_volt3, 'k.-' , markersize = 5 )
sub3.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)
#sub3.set_ylim(2.8,3.4)
#TODO ylim für Strom definieren
sub4 = fig.add_subplot(224)
sub4.set_xlabel('Time')
sub4.set_ylabel('Current')
sub4.plot(t, arr_curr, 'g.-' , markersize = 5 )
sub4.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)
#sub4.set_ylim(2.4,3.8)

v = StringVar()
T = Label(root,textvariable=v,justify=LEFT, height=5, width=16,borderwidth=2, relief="groove",background='white')#.place(x=400, y=10)
T.pack(anchor="n", fill='both', expand=True)

graph = FigureCanvasTkAgg(fig, master=root)
graph.get_tk_widget().pack(side="top", fill='both', expand=True)

startbutton = Button(root, text='Start', width=3, command=lambda:[startstop(1),run()]).place(x=10,y=10)
stopbutton = Button(root, text='Stop', width=3, command=lambda:[startstop(0)]).place(x=70,y=10)
resetbutton = Button(root, text='Reset', width=3, command=lambda:[startstop(0),WarningReset()]).place(x=130,y=10)
chargebutton = Button(root, text='Charge', width=4, command=lambda:[print("Charge"),ChargeDischarge(1)]).place(x=190,y=10)#ser.write("c".encode()),
dischargebutton = Button(root, text='Discharge', width=6, command=lambda:[print("Discharge"),ChargeDischarge(0)]).place(x=260,y=10)#ser.write("d".encode()),
#startbalancebutton = Button(root, text='Start Balancing', width=10, command=lambda:[ser.write("b".encode()),print("b")]).place(x=10,y=47)
#stopbalancebutton = Button(root, text='Stop Balancing', width=10, command=lambda:[ser.write("s".encode()),print("s")]).place(x=125,y=47)


def zeroresults():
    v.set("Power: " + str(0) + "W\n"\
    "Voltage Z1: " + str(0) + "V\n"\
    "Voltage Z2: " + str(0) + "V\n"\
    "Voltage Z3: " + str(0) + "V\n"\
    "Current: " + str(0) + "V\n"\
    "Balancing: " + str(balstartstop_var))
    return
#zeroresults()
def resetlists():
    del t[:]
    del arr_volt1[:]
    del arr_volt2[:]
    del arr_volt3[:]
    del arr_curr[:]
    print(t0)
    print(time.time())
    sub1.lines[0].set_data( [],[] )
    sub2.lines[0].set_data( [],[] )
    sub3.lines[0].set_data( [],[] )
    sub4.lines[0].set_data( [],[] )
    zeroresults()
    print("Measurement reseted at " + str(time.strftime("%Y%m%d-%H%M%S")))
    return
def run():
    print("Measurement started at " + str(time.strftime("%Y%m%d-%H%M%S")))
    t0 = time.time()
    while True:
        #if ser.readline().decode().replace('\r', '').replace('\n', '') == "start":
        #  ardu_volt1 = float(ser.readline().decode().replace('\r', '').replace('\n', ''))
       #   ardu_volt2 = float(ser.readline().decode().replace('\r', '').replace('\n', ''))
      #    ardu_volt3 = float(ser.readline().decode().replace('\r', '').replace('\n', ''))
     #     ardu_curr  = float(ser.readline().decode().replace('\r', '').replace('\n', ''))
    #      t.append( time.time()-t0 )  # add new x data value
   #       arr_volt1.append( ardu_volt1*0.000382 )        # add new y data value
  #        arr_volt2.append( ardu_volt2*0.000382 )        # add new y data value
 #         arr_volt3.append( ardu_volt3*0.000382 )        # add new y data value
#          arr_curr.append( ardu_curr )        # add new y data value
        ardu_volt1 = 1*random.random()#float(ser.readline().decode().replace('\r', '').replace('\n', ''))
        ardu_volt2 = 2*random.random()#float(ser.readline().decode().replace('\r', '').replace('\n', ''))
        ardu_volt3 = 3*random.random()#float(ser.readline().decode().replace('\r', '').replace('\n', ''))
        ardu_curr  = 4*random.random()#float(ser.readline().decode().replace('\r', '').replace('\n', ''))
        t.append( time.time()-t0 )  # add new x data value
        arr_volt1.append( ardu_volt1)#*0.000382 )        # add new y data value
        arr_volt2.append( ardu_volt2)#*0.000382 )        # add new y data value
        arr_volt3.append( ardu_volt3)#*0.000382 )        # add new y data value
        arr_curr.append( ardu_curr )        # add new y data value
        if startstop_var == 0:
          print("Measurement stopped at " + str(time.strftime("%Y%m%d-%H%M%S")))
          break
    
        sub1.lines[0].set_data( t,arr_volt1 ) # set plot voltage
        sub1.relim()                  # recompute the data limits
        sub1.autoscale_view()         # automatic axis scaling
        sub2.lines[0].set_data( t,arr_volt2 ) # set plot data
        sub2.relim()                  # recompute the data limits
        sub2.autoscale_view()         # automatic axis scaling
        sub3.lines[0].set_data( t,arr_volt3 ) # set plot data
        sub3.relim()                  # recompute the data limits
        sub3.autoscale_view()         # automatic axis scaling
        sub4.lines[0].set_data( t,arr_curr ) # set plot data
        sub4.relim()                  # recompute the data limits
        sub4.autoscale_view()         # automatic axis scaling

        fig.canvas.flush_events()   # update the plot and take care of window events (like resizing etc.)
        v.set("Power: " + str(round(arr_volt1[-1]*0,2)) + "W\n"\
              "Voltage Z1: " + str(round(arr_volt3[-1],3)) + "V\n"\
              "Voltage Z2: " + str(round(arr_volt2[-1],3)) + "V\n"\
              "Voltage Z3: " + str(round(arr_volt1[-1],3)) + "V\n"\
              "Current: " + str(round(arr_curr[-1],3)) + "A\n"\
              "Balancing: " + str(balstartstop_var))


    return
root.mainloop()
