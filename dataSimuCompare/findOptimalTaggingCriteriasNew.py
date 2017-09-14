from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile,gStyle,gPad,TLegend
gROOT.Reset()
import numpy as np
import sys
print sys.argv
import os
import matplotlib.pyplot as plt

PAGEWIDTH_INCH = 430.20639/72.27
GOLDEN=(1.0+np.sqrt(5.0))/2
ratio=1.0
FIGSIZE=(ratio*PAGEWIDTH_INCH,ratio*PAGEWIDTH_INCH*1.0)

from matplotlib import rcParams,rc
rcParams.update({'text.usetex':True})
#rc('font',**{'family':'serif','serif':['Times'],'size':11})
rc('font',**{'family':'serif','serif':['Times'],'size':10})

def tagging (data,background,simu,size,energy,clusterCharge,prong):
    taggedData=0
    taggedBackground=0
    taggedSimu=0
    taggedClusterNumber=-1
    for point in background:
        if point[0]>size and point[1]>energy and point[2]>clusterCharge and point[3]>=prong:
            taggedBackground+=1
    for point in data:
        if point[0]>size and point[1]>energy and point[2]>clusterCharge and point[3]>=prong:
            taggedData+=1
    isNotTagged=True
    for point in simu:
        if taggedClusterNumber==point[4]:
            #print "er vi her"
            continue
        if point[0]>size and point[1]>energy and point[2]>clusterCharge and point[3]>=prong:
            if point[0]<10:
                print "to low",point[0]
            taggedClusterNumber=point[4]
            taggedSimu+=1
    return taggedData,taggedBackground,taggedSimu 
            

data=[]    
hasBegin=False
e=1.0
for line in open("../dataAnalysis/datafiles/meta.txt"):
#for line in open("../houghTransform/meta.txt"):
    columns=line.split()    
    if columns[0]=="pixels":
        hasBegin=True
        size=float(columns[1])
    if columns[0]=="energy":
        energy=float(columns[1])
    if columns[0]=="clusterCharge":
        clusterCharge=float(columns[1])
    if columns[0]=="prong":
        prong= int(columns[1])
    if columns[0]=="error":
        error=float(columns[1])
        if error<e:
            prong=0
    if columns[0]=="newCluster" and hasBegin:
        data.append([size,energy,clusterCharge,prong])



background=[]
hasBegin=False
for line in open("../dataAnalysis/reversedDatafiles/meta.txt"):
    columns=line.split()    
    if columns[0]=="pixels":
        hasBegin=True
        size=float(columns[1])
    if columns[0]=="energy":
        energy=float(columns[1])
    if columns[0]=="clusterCharge":
        clusterCharge=float(columns[1])
    if columns[0]=="prong":
        prong= int(columns[1])
    if columns[0]=="error":
        error=float(columns[1])
        if error<e:
            prong=0
    if columns[0]=="newCluster" and hasBegin:
        background.append([size,energy,clusterCharge,prong])


simu=[]
simuvolcano=[]
simuoptimal=[]
hasBegin=False
for line in open("../simu/datafiles/meta.txt"):
    columns=line.split()    
    if columns[0]=="pixels":
        hasBegin=True
        size=float(columns[1])
    if columns[0]=="energy":
        energy=float(columns[1])
    if columns[0]=="clusterCharge":
        clusterCharge=float(columns[1])
    if columns[0]=="prong":
        prong= int(columns[1])
    if columns[0]=="error":
        error=float(columns[1])
        if error<e:
            prong=0
    if columns[0]=="clusterNumber":
        clusterNumber=int(columns[1])
    if columns[0]=="newCluster" and hasBegin:
        simu.append([size,energy,clusterCharge,prong,clusterNumber])


hasBegin=False
clusterNumber=0
for line in open("../simu/datafilesJustVolcano/meta.txt"):
    columns=line.split()    
    if columns[0]=="pixels":
        hasBegin=True
        size=float(columns[1])
    if columns[0]=="energy":
        energy=float(columns[1])
    if columns[0]=="clusterCharge":
        clusterCharge=float(columns[1])
    if columns[0]=="prong":
        prong= int(columns[1])
    if columns[0]=="error":
        error=float(columns[1])
        if error<e:
            prong=0
    if columns[0]=="newCluster" and hasBegin:
        clusterNumber+=1
        simuoptimal.append([size,energy,clusterCharge,prong,clusterNumber])


        
falseRate0=[]
efficency0=[]
falseRate1=[]
efficency1=[]


falseRate0Optimal=[]
efficency0Optimal=[]
falseRate1Optimal=[]
efficency1Optimal=[]



numberOfSimulated=10000.0
#numberOfSimulated=len(simu)

numberOfOriginalSimulated=10000.0
print "simulated",len(simuoptimal)
inCenterCharge=[]

for i in np.arange(0,500,10):
    inCenterCharge.append(i)
    result=tagging(data,background,simu,i,0,0,0)
    falseRate=result[1]*1.0/len(background)
    efficency=result[2]*1.0/numberOfSimulated
    falseRate0.append(falseRate)
    efficency0.append(efficency)
    result=tagging(data,background,simu,i,0,0,1)
    falseRate=result[1]*1.0/len(background)
    efficency=result[2]*1.0/numberOfSimulated
    tagged=result[0]*1.0/len(data)
    falseRate1.append(falseRate)
    efficency1.append(efficency)
    tagged=result[0]*1.0/len(data)
    print i,efficency,falseRate
    result=tagging(data,background,simuoptimal,i,0,0,0)
    falseRate=result[1]*1.0/len(background)
    efficency=result[2]*1.0/numberOfOriginalSimulated
    falseRate0Optimal.append(falseRate)
    efficency0Optimal.append(efficency)
    result=tagging(data,background,simuoptimal,i,0,0,1)
    falseRate=result[1]*1.0/len(background)
    efficency=result[2]*1.0/numberOfOriginalSimulated
    tagged=result[0]*1.0/len(data)
    falseRate1Optimal.append(falseRate)
    efficency1Optimal.append(efficency)
    



result=tagging(data,background,simu,70,0,0,1)
falseRate=result[1]*1.0/len(background)
print "antall bakgrunn",len(background)
print "antall clusters",len(data)
print "antall taggede",result[0]
print "result", result[2]*1.0/10000
result=tagging(data,background,simu,70,0,0,0)
print "result", result[2]*1.0/10000
print "false rate",falseRate
print "lengden til simu optimal",len(simu)


    
fig=plt.figure(figsize=FIGSIZE,dpi=100)
ax0 = plt.subplot(221)
ax1 = plt.subplot(222)
ax2 = plt.subplot(223)
ax3 = plt.subplot(224)

ax1.plot(falseRate0Optimal,efficency0Optimal,'k--',linewidth=4,label="Without dead pixels,\n No cuts on prongs")
ax1.plot(falseRate1Optimal,efficency1Optimal,'m',linewidth=4,label="Without dead pixels,\n At least one prong")
ax1.plot(falseRate0,efficency0,'k--',label="With dead pixels,\n No cuts on prongs")
ax1.plot(falseRate1,efficency1,'m',label="With dead pixels,\n At least one prong")
ax1.set_ylabel(r'$ p_t$')
ax1.set_xlabel(r'$ p_f$')
ax1.set_xlim(0,0.05)
ax1.set_ylim(0.1,1.0)
ax1.locator_params(axis='x',nbins=4)#to specify number of ticks on both or any single axes
ax1.plot([0.0,0.5],[0.54,0.54],'b')
ax1.annotate(r'$p_t$ = 0.54', xy=(0.025, 0.54), xycoords='data',
             xytext=(-35,-40), textcoords='offset points', fontsize=12,
             arrowprops=dict(arrowstyle="->"))

ax2.plot(inCenterCharge,efficency0,'k--',label="No cuts on prong")
ax2.plot(inCenterCharge,efficency1,'m',label="At least one prong")
ax2.plot(inCenterCharge,efficency0Optimal,'k--',linewidth=3,label="Optimal detector, No cuts on prong")
ax2.plot(inCenterCharge,efficency1Optimal,'m',linewidth=3,label="Optimal detector, At least one prong")
ax2.set_ylabel(r'$p_t$')
ax2.set_xlabel("Cluster size cut \# pixels")
ax2.plot([70,70],[0,1],'b')
ax2.annotate('70 pixels', xy=(70, 0.8), xycoords='data',
             xytext=(+40, 0), textcoords='offset points', fontsize=11,
             arrowprops=dict(arrowstyle="->"))
#arrowprops=dict(facecolor='black', connectionstyle="arc3,rad=.2",shrink=0.05),
ax2.set_ylim(0,1)
ax2.set_xlim(0,500)

ax3.plot(inCenterCharge,falseRate0,'k--',label="No cuts on prong")
ax3.plot(inCenterCharge,falseRate1,'m',label="At least one prong")
#ax3.plot(falseRate0,inCenterCharge,'k--',label="No cuts on prong")
#ax3.plot(falseRate1,inCenterCharge,'m',label="At least one prong")
ax3.set_ylabel(r'$p_f$')
ax3.set_xlabel("Cluster size cut \# pixels")
ax3.set_xlim(0,500)
ax3.set_ylim(0,0.05)
ax3.plot([70,70],[0,0.05],'b')
ax3.annotate('70 pixels', xy=(70, 0.04), xycoords='data',
             xytext=(+40,0), textcoords='offset points', fontsize=11,
             arrowprops=dict(arrowstyle="->"))
handles, labels = ax1.get_legend_handles_labels()
ax0.legend(handles, labels,frameon=False,borderpad=5,fontsize=9,handlelength=4)



plt.subplots_adjust(left=0.12,bottom=0.10,right=0.9,top=0.9,wspace=0.30,hspace=0.30)
#plt.savefig("/home/helga/Presantations/MedipixMeeting2017/fig/taggingEfficency.pdf")   
ax1.text(.5,.9,'a)',transform=ax1.transAxes)
ax2.text(.5,.9,'b)',transform=ax2.transAxes)
ax3.text(.5,.9,'c)',transform=ax3.transAxes)
ax0.axis("off")
plt.savefig("../../../fig/taggingEfficency.pdf")   
