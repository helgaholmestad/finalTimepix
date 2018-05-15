#from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile
#histoxy=TH2D("xy","xy",1000,-500,500,1000,-500,500)
#histoxz=TH2D("xy","xy",300,-150,150,1000,-500,500)
#histoyz=TH2D("xy","xy",300,-150,150,1000,-500,500)
import scipy.integrate as noe
import os
import numpy as np
import matplotlib.pyplot as plt
import sys
import math
hasNotStarted=True
inData=False
event=0
temp=[]
time=[]
BackCurrent=[]
P1Current=[]
P2Current=[]
P3Current=[]
P4Current=[]
P5Current=[]
P6Current=[]
P7Current=[]
P8Current=[]
P9Current=[]

for line in open("../200Bias/BLET/10MeV/1D_plots_PARTICLE_des.plt"):
#for line in open(sys.argv[1]):
    columns=line.split()
    if(len(columns)>0 and str(columns[0])=="Data"):
        hasNotStarted=False
    if hasNotStarted:
        continue
    if(len(columns)==5):
        inData=True
        for i in columns:
            temp.append(i)
    elif(len(columns)==1 and inData and columns[0]!="}"):
        time.append(float(columns[0]))
        P7Current.append(float(temp[6]))
        BackCurrent.append(float(temp[6+1*8]))
        P8Current.append(float(temp[6+2*8]))
        P9Current.append(float(temp[6+3*8]))
        P1Current.append(float(temp[6+4*8]))
        P2Current.append(float(temp[6+5*8]))
        P3Current.append(float(temp[6+6*8]))
        P4Current.append(float(temp[6+7*8]))
        P5Current.append(float(temp[6+8*8]))
        P6Current.append(float(temp[6+9*8]))  
        temp=[]        
 
pi=3.141
plt.figure(0)
timeRaw=np.asarray(time)
print(type(time))
time=timeRaw*1000000000
print(time)
#plt.plot(time,P1Current,'red',label="Pixel 0")
#plt.plot(time,np.asarray(P2Current)/(2*pi),'blue',label="Pixel 1")
#plt.plot(time,np.asarray(P3Current)/(4*pi),'green',label="Pixel 2")
#plt.plot(time,np.asarray(P4Current)/(6*pi),'cyan',label="Pixel 3")
#plt.plot(time,np.asarray(P5Current)/(8*pi),'magenta',label="Pixel 4")
#plt.plot(time,np.asarray(P6Current)/(10*pi),'magenta',label="Pixel 5")
plt.plot(time,np.asarray(P7Current)/(12*pi),'k--',label="330 mu ",linewidth=3)
#plt.plot(time,np.asarray(P8Current)/(14*pi),'magenta',label="385 mu",linewidth=3)
plt.legend()
#plt.yscale('log')

P1CurrentNp=np.asarray(P1Current)
P2CurrentNp=np.asarray(P2Current)
P3CurrentNp=np.asarray(P3Current)
P4CurrentNp=np.asarray(P4Current)
P5CurrentNp=np.asarray(P5Current)
P6CurrentNp=np.asarray(P6Current)
P7CurrentNp=np.asarray(P7Current)
P8CurrentNp=np.asarray(P8Current)
P9CurrentNp=np.asarray(P9Current)

print("pixel 1",np.trapz(P1CurrentNp,timeRaw))
print("pixel 2",np.trapz(P2CurrentNp,timeRaw)/(2*pi))
print("pixel 3",np.trapz(P3CurrentNp,timeRaw)/(4*pi))
print("pixel 4",np.trapz(P4CurrentNp,timeRaw)/(6*pi))
print("pixel 5",np.trapz(P5CurrentNp,timeRaw)/(8*pi))
print("pixel 6",np.trapz(P6CurrentNp,timeRaw)/(10*pi))

totalCharge=np.trapz(P8CurrentNp,timeRaw)#+np.trapz(P2CurrentNp,timeRaw)+np.trapz(P3CurrentNp,timeRaw)+np.trapz(P4CurrentNp,timeRaw)+np.trapz(P5CurrentNp,timeRaw)+np.trapz(P6CurrentNp,timeRaw)+np.trapz(P7CurrentNp,timeRaw)+np.trapz(P8CurrentNp,timeRaw)
#totalCharge=np.trapz(P8CurrentNp/(14*pi),timeRaw)
print("total deposited energy",totalCharge/(1000*1.6*math.pow(10,-19))*3.6/(14*pi),"keV")
plt.ylim(-3*pow(10,-10),1.5*pow(10,-10))
plt.xlim(0,3.5*pow(10,3))
plt.xlabel("time (ns)",fontsize=18)
plt.ylabel("current (A)",fontsize=18)
ax=plt.gca()
ax.tick_params(axis='both', which='major', labelsize=16)
plt.savefig("../../../fig/currents.pdf")

plt.figure()
plt.plot(time,np.asarray(P8Current)/(14*pi),'b',label="Measured current 385 um from \n an 10 MeV energy deposition ",linewidth=1)
plt.legend()
plt.ylim(-1.0*pow(10,-10),0.5*pow(10,-10))
plt.xlim(0,4.0*pow(10,3))
plt.xlabel("time (ns)",fontsize=10)
plt.ylabel("current (A)",fontsize=10)
plt.plot([0,4000],[0,0],"grey")
ax=plt.gca()
ax.tick_params(axis='both', which='major', labelsize=10)
plt.savefig("/home/helga/gitThesis/thesis/Annihilation/fig/current.pdf")





