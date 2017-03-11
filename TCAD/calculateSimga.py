from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile
#histoxy=TH2D("xy","xy",1000,-500,500,1000,-500,500)
#histoxz=TH2D("xy","xy",300,-150,150,1000,-500,500)
#histoyz=TH2D("xy","xy",300,-150,150,1000,-500,500)
import scipy.integrate as noe
import os
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.optimize import curve_fit
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


def gaus(x,a,sigma):
    return a*exp(-x**2/(2*sigma**2))



for line in open(sys.argv[1]):
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



print "time",len(time)
time=np.asarray(time)

pi=np.pi

print "central pixel",(noe.simps(P1Current,time))*3.6/1.6*10**16
print "pixel1",(noe.simps(P2Current,time))/(2.0*pi)*3.6/1.6*10**16
print "pixel2",(noe.simps(P3Current,time))/(4.0*pi)*3.6/1.6*10**16
print "pixel3",(noe.simps(P4Current,time))/(6.0*pi)*3.6/1.6*10**16
print "pixel4",(noe.simps(P5Current,time))/(8.0*pi)*3.6/1.6*10**16
print "pixel5",(noe.simps(P6Current,time))/(10.0*pi)*3.6/1.6*10**16
print "totalIntagral",((noe.simps(P1Current,time))+(noe.simps(P2Current,time))+(noe.simps(P3Current,time))+(noe.simps(P4Current,time))+(noe.simps(P5Current,time))+(noe.simps(P6Current,time))+(noe.simps(P7Current,time))+(noe.simps(P8Current,time))+(noe.simps(P9Current,time)))*3.6/1.6*10**16

numberOfSteps=int(sys.argv[2])
timeSmall=time[0:numberOfSteps]
BackCurrentSmall=BackCurrent[0:numberOfSteps]
P1CurrentSmall=P1Current[0:numberOfSteps]
P2CurrentSmall=P2Current[0:numberOfSteps]
P3CurrentSmall=P3Current[0:numberOfSteps]
P4CurrentSmall=P4Current[0:numberOfSteps]
P5CurrentSmall=P5Current[0:numberOfSteps]
P6CurrentSmall=P6Current[0:numberOfSteps]
P7CurrentSmall=P7Current[0:numberOfSteps]
P8CurrentSmall=P8Current[0:numberOfSteps]
P9CurrentSmall=P9Current[0:numberOfSteps]


print "totalIntagral",((noe.simps(P1CurrentSmall,timeSmall))+(noe.simps(P2CurrentSmall,timeSmall))+(noe.simps(P3CurrentSmall,timeSmall))+(noe.simps(P4CurrentSmall,timeSmall))+(noe.simps(P5CurrentSmall,timeSmall))+(noe.simps(P6CurrentSmall,timeSmall))+(noe.simps(P7CurrentSmall,timeSmall))+(noe.simps(P8CurrentSmall,timeSmall))+(noe.simps(P9CurrentSmall,timeSmall)))*3.6/1.6*10**16



print "central pixel",(4*noe.simps(P1CurrentSmall,timeSmall))/(pi)*3.6/1.6*10**16
print "pixel1",(noe.simps(P2CurrentSmall,timeSmall))/(2.0*pi)*3.6/1.6*10**16
print "pixel2",(noe.simps(P3CurrentSmall,timeSmall))/(4.0*pi)*3.6/1.6*10**16
print "pixel3",(noe.simps(P4CurrentSmall,timeSmall))/(6.0*pi)*3.6/1.6*10**16
print "pixel4",(noe.simps(P5CurrentSmall,timeSmall))/(8.0*pi)*3.6/1.6*10**16
print "pixel5",(noe.simps(P6CurrentSmall,timeSmall))/(10.0*pi)*3.6/1.6*10**16
pixel8=(noe.simps(P9CurrentSmall,timeSmall))/(16.0*pi)*3.6/1.6*10**16
pixel0=(noe.simps(P1CurrentSmall,timeSmall))*3.6/1.6*10**16-pixel8
pixel1=(noe.simps(P2CurrentSmall,timeSmall))/(2.0*pi)*3.6/1.6*10**16-pixel8
pixel2=(noe.simps(P3CurrentSmall,timeSmall))/(4.0*pi)*3.6/1.6*10**16-pixel8
pixel3=(noe.simps(P4CurrentSmall,timeSmall))/(6.0*pi)*3.6/1.6*10**16-pixel8
pixel4=(noe.simps(P5CurrentSmall,timeSmall))/(8.0*pi)*3.6/1.6*10**16-pixel8
pixel5=(noe.simps(P6CurrentSmall,timeSmall))/(10.0*pi)*3.6/1.6*10**16-pixel8
pixel6=(noe.simps(P7CurrentSmall,timeSmall))/(12.0*pi)*3.6/1.6*10**16-pixel8
pixel7=(noe.simps(P8CurrentSmall,timeSmall))/(14.0*pi)*3.6/1.6*10**16-pixel8
pixel8=0


variance=(pixel1*1+pixel2*4+pixel3*9+pixel4*16+pixel5*25+pixel6*36+pixel7*49+pixel8*64)/(pixel0+pixel1+pixel2+pixel3+pixel4+pixel5+pixel6+pixel7+pixel8)
rms=np.sqrt(variance)*55.5
print "sigma",rms
print "totalIntagral",((noe.simps(P1CurrentSmall,timeSmall))+(noe.simps(P2CurrentSmall,timeSmall))+(noe.simps(P3CurrentSmall,timeSmall))+(noe.simps(P4CurrentSmall,timeSmall))+(noe.simps(P5CurrentSmall,timeSmall))+(noe.simps(P6CurrentSmall,timeSmall))+(noe.simps(P7CurrentSmall,timeSmall))+(noe.simps(P8CurrentSmall,timeSmall))+(noe.simps(P9CurrentSmall,timeSmall)))*3.6/1.6*10**16

popt,pcov = curve_fit(Gauss, x, y, p0=[max(y), rms])

timeSmall=1000000000*timeSmall
pi=3.141
#plt.figure(0)
plt.ylim(-10*pow(10,-7),pow(10,-7))
plt.plot(timeSmall,P1CurrentSmall,'red',label="Pixel 0")
plt.plot(timeSmall,np.asarray(P2CurrentSmall)/(2*pi),'blue',label="Pixel 1")
plt.plot(timeSmall,np.asarray(P3CurrentSmall)/(4*pi),'green',label="Pixel 2")
plt.plot(timeSmall,np.asarray(P4CurrentSmall)/(6*pi),'cyan',label="Pixel 3")
plt.plot(timeSmall,np.asarray(P5CurrentSmall)/(8*pi),'magenta',label="Pixel 4")
plt.plot(timeSmall,np.asarray(P6CurrentSmall)/(10*pi),'yellow',label="Pixel 5")
plt.plot(timeSmall,np.asarray(P7CurrentSmall)/(12*pi),'black',label="Pixel  6")
plt.plot(timeSmall,np.asarray(P8CurrentSmall)/(14*pi),'lightblue',label="Pixel 7")
plt.show()















