#TODO 
import serial#Input/Output via Serieller Schnittstelle
import serial.tools.list_ports#Input/Output via Serieller Schnittstelle
import time#Zeiterfassung zur chronologischen Ablage von Exportdaten
import random#Darstellung von Zufallsdaten bei entferntem BMS-Board
import matplotlib#Plotten der Daten
matplotlib.use('TkAgg')#Plotten der Daten
import matplotlib.pyplot as plt#Plotten der Daten
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#Plotten der Daten
import tkinter as tk#GUI-Toolkit
from tkinter import *#GUI-Toolkit
from tkinter import messagebox
import numpy as np#Export
import sys #Serielle Verbindung, entscheide ob Linux oder Windows 
import glob#Filename pattern matching

root = tk.Tk()#Erzeugt ein Fenster
root.title("Monitoring")#Benennt das Fenster
root.config(background='white')#Setzt den Hintergrund weiss
root.geometry("1000x700")#Bestimmt die Größe des Fensters

#Automatische Abfrage der seriellen Schnittstelle 
def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
serial_ports()
#DebugModus
debug=1
if debug==1:
    print("Debug-Modus ON")
elif debug==0:
    print("Debug-Modus OFF")
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

def export(value):
    global arr_volt1
    global arr_volt2
    global arr_volt3
    global arr_curr
    global t
    time_call = time.strftime("%Y%m%d-%H%M%S")
    if value == "volt1":
        np.savetxt("./export/"+time_call+"-voltage1.txt",np.column_stack((t,arr_volt1)), delimiter=",", fmt='%s', header=time_call+'-Voltage\s,V')
    elif value == "volt2":
        np.savetxt("./export/"+time_call+"-voltage2.txt",np.column_stack((t,arr_volt2)), delimiter=",", fmt='%s', header=time_call+'-Voltage\s,V')
    elif value == "volt3":
        np.savetxt("./export/"+time_call+"-voltage3.txt",np.column_stack((t,arr_volt3)), delimiter=",", fmt='%s', header=time_call+'-Voltage\s,V')
    elif value == "curr":  
        np.savetxt("./export/"+time_call+"-current.txt",np.column_stack((t,arr_curr)), delimiter=",", fmt='%s', header=time_call+'-Current\s,A')
    elif value == "allval": 
        np.savetxt("./export/"+time_call+"-BMS.txt",np.column_stack((t,arr_volt1,arr_volt2,arr_volt3,arr_curr)), delimiter=",", fmt='%s', header=time_call+'-t,V1,V2,V3,I') 
    return
def ChargeDischarge(value):
    global ChargeDischarge_var
    ChargeDischarge_var = value
    if ChargeDischarge_var == 0:
        ser.write("d".encode())#Sendet einen char
        label_Dis = Label(root, image=pic_discharge).place(x=800,y=10)
    elif ChargeDischarge_var == 1:
        ser.write("c".encode())#Sendet einen char        
        label_Ch = Label(root, image=pic_charge).place(x=800,y=10)
    elif ChargeDischarge_var == 2:
        ser.write("e".encode())#Sendet einen char 
        label_StCh = Label(root, image=pic_stopcharge).place(x=800,y=10)
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

###Menubar##############
menu = Menu(root)
root.config(menu=menu)
menu.add_command(label="Start", command=lambda:[startstop(1),run(),zeroresults()])
menu.add_command(label="Stop", command=lambda:[startstop(0)])
menu.add_command(label="Reset", command=lambda:[startstop(0),WarningReset()])
if serial_ports() != []:
    menu.add_command(label="Error Reset", command=lambda:[ser.write("y".encode()),print("Reset Error")])
#
exportmenu = Menu(menu)
menu.add_cascade(label="Export", menu=exportmenu)
exportmenu.add_command(label="Voltage1 to CSV", command=lambda:[export("volt1")])
exportmenu.add_command(label="Voltage2 to CSV", command=lambda:[export("volt2")])
exportmenu.add_command(label="Voltage3 to CSV", command=lambda:[export("volt3")])
exportmenu.add_command(label="Current to CSV", command=lambda:[export("curr")])
exportmenu.add_command(label="All Values to CSV", command=lambda:[export("allval")])
#
if serial_ports() != []:
    balmenu = Menu(menu)
    menu.add_cascade(label="Balancing", menu=balmenu)
    balmenu.add_command(label="Balancing ON", command=lambda:[print("Balancing ON"),balstartstop(1)])
    balmenu.add_command(label="Balancing OFF", command=lambda:[print("Balancing OFF"),balstartstop(0)])
    #
    modusmenu = Menu(menu)
    menu.add_cascade(label="Modus", menu=modusmenu)
    modusmenu.add_command(label="Charge", command=lambda:[print("Charge"),ChargeDischarge(1)])
    modusmenu.add_command(label="Discharge", command=lambda:[print("Discharge"),ChargeDischarge(0)])
    modusmenu.add_command(label="Stop Charge", command=lambda:[print("Stop charge"),ChargeDischarge(2)])
    ######################

###Picture###############
pic_discharge = PhotoImage(file='./images/Discharge.png')
pic_charge = PhotoImage(file='./images/Charge.png')
pic_stopcharge = PhotoImage(file='./images/StopCharge.png')
pic_eet= PhotoImage(file='./images/eet-logo.png')
pic_tu = PhotoImage(file='./images/tu-logo.png')
label_eet = Label(root, image=pic_eet).pack(anchor="n")

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



if serial_ports() == []:
    print("No Arduino connected!")
    MsgBox = tk.messagebox.showwarning('Serial connection','No Arduino connected!',icon = 'warning')
else:
    port = serial_ports()[0]
    print("Arduino connected to port "+port)
    ser = serial.Serial(serial_ports()[0], 9600, timeout=0)

def zeroresults():
    v.set("Power: " + str(0) + "W\n"\
    "Voltage Z1: " + str(0) + "V\n"\
    "Voltage Z2: " + str(0) + "V\n"\
    "Voltage Z3: " + str(0) + "V\n"\
    "Current: " + str(0) + "V")
    return
zeroresults()
def resetlists():
    del t[:]
    del arr_volt1[:]
    del arr_volt2[:]
    del arr_volt3[:]
    del arr_curr[:]
    #print(t0)
    #print(time.time())
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
        if debug==0:
            if ser.readline().decode().replace('\r', '').replace('\n', '') == "start":
                ardu_volt1 = float(ser.readline().decode().replace('\r', '').replace('\n', ''))
                ardu_volt2 = float(ser.readline().decode().replace('\r', '').replace('\n', ''))
                ardu_volt3 = float(ser.readline().decode().replace('\r', '').replace('\n', ''))
                ardu_curr  = float(ser.readline().decode().replace('\r', '').replace('\n', ''))
                t.append( time.time()-t0 )  # add new x data value
                arr_volt1.append( ardu_volt1*0.000382 )        # add new y data value
                arr_volt2.append( ardu_volt2*0.000382 )        # add new y data value
                arr_volt3.append( ardu_volt3*0.000382 )        # add new y data value
                arr_curr.append( ardu_curr )        # add new y data value """
        elif debug==1:
            ardu_volt1 = 1*random.random()#float(ser.readline().decode().replace('\r', '').replace('\n', ''))
            ardu_volt2 = 2*random.random()#float(ser.readline().decode().replace('\r', '').replace('\n', ''))
            ardu_volt3 = 3*random.random()#float(ser.readline().decode().replace('\r', '').replace('\n', ''))
            ardu_curr  = 4*random.random()#float(ser.readline().decode().replace('\r', '').replace('\n', ''))
            t.append( time.time()-t0 )  # add new x data value
            arr_volt1.append( ardu_volt1)        # add new y data value
            arr_volt2.append( ardu_volt2)        # add new y data value
            arr_volt3.append( ardu_volt3)        # add new y data value
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
              "Current: " + str(round(arr_curr[-1],3)) + "A")

        #time.sleep(1)
        
    return

root.mainloop()

# startbutton = Button(root, text='Start', width=4, command=lambda:[startstop(1),run(),zeroresults()]).place(x=10,y=10)
# stopbutton = Button(root, text='Stop', width=4, command=lambda:[startstop(0)]).place(x=70,y=10)
# resetbutton = Button(root, text='Reset', width=4, command=lambda:[startstop(0),WarningReset()]).place(x=130,y=10)
# chargebutton = Button(root, text='Charge', width=5, command=lambda:[ser.write("c".encode()),print("Charge"),ChargeDischarge(1)]).place(x=190,y=10)
# dischargebutton = Button(root, text='Discharge', width=7, command=lambda:[ser.write("d".encode()),print("Discharge"),ChargeDischarge(0)]).place(x=260,y=10)#
# stopchargebutton = Button(root, text='Stop Charge', width=7, command=lambda:[print("Stop charge"),ChargeDischarge(2)]).place(x=350,y=10)#
# startbalancebutton = Button(root, text='Start Balancing', width=10, command=lambda:[ser.write("b".encode()),print("b"),balstartstop(1)]).place(x=10,y=47)
# stopbalancebutton = Button(root, text='Stop Balancing', width=10, command=lambda:[ser.write("s".encode()),print("s"),balstartstop(0)]).place(x=125,y=47)
# DeleteErrorButton = Button(root, text='Delete Error', width=10, command=lambda:[ser.write("y".encode()),print("y")]).place(x=260,y=47)
#w = Scale(root, from_=0, to=1, orient=HORIZONTAL,width=20,background='white',borderwidth=0,tik='Blub').place(x=500,y=47)