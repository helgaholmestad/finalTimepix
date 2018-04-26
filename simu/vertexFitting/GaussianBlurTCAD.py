from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile
gROOT.Reset()
import sys
import numpy as np
from math import exp
from math import sqrt
import matplotlib.pyplot as plt
file=open("datafiles"+sys.argv[3]+"/"+sys.argv[2]+"results.txt",'w')
fileEnergy=open("datafiles"+sys.argv[3]+"/"+sys.argv[2]+"energyAround.txt",'w')
hasStarted=False
eventNumber=0
pixelNumber=0
myFile=TFile("datafiles"+sys.argv[3]+"/histogramsTCADRaw"+sys.argv[2]+".root","RECREATE")
#myFile=TFile(sys.argv[1]+".root","RECREATE")
finalData=TH2D("final","final",256,0,256,256,0,256)
finalWithCut=TH2D("event0","event0",256,0,256,256,0,256)
initialData=TH2D("initial","initial",256,0,256,256,0,256)
entry=0
radius=TH2D("","",100,0,100,200,0,20)
energyAroundHisto=TH1D("","",500,0,50)
energySpread={}
energySpread[(1,1)]=8.5
energySpread[(1,2)]=5.8
energySpread[(1,3)]=3.9

energySpread[(10,1)]=9.3
energySpread[(10,2)]=6.4
energySpread[(10,3)]=4.1

energySpread[(100,1)]=16.8
energySpread[(100,2)]=9.6
energySpread[(100,3)]=7.5

energySpread[(1000,1)]=34.5
energySpread[(1000,2)]=42.2
energySpread[(1000,3)]=29.6

energySpread[(10000,1)]=80.0
energySpread[(10000,2)]=42.2
energySpread[(10000,3)]=29.6

energySpread[(50000,1)]=128.4
energySpread[(50000,2)]=74.31
energySpread[(50000,3)]=52.3


def findNearest(value):
    myarray=[1,10,100,1000,10000,50000]
    lowerValue=1
    higherValue=1
    for m in myarray:
        if m>value:
            higherValue=m
            return lowerValue,higherValue
        lowerValue=m
    return 50000,50000
      
#remember that all the calculation is done in terms of pixel sizes of 2560 times 2560 pixels. Therefore the sigma has to be translated to pixel size
def choseSigma(layer,energy):
    #find out if we are outside domian and then set to the edge
    #determine upper and lower limit
    lower,upper=findNearest(energy)
    if lower==upper:
        sigma=energySpread[(lower,layer+1)]
    else:
        f=(energy*1.0-lower*1.0)/(1.0*upper-1.0*lower)
        sigma=(1-f)*energySpread[(lower,layer+1)]+f*energySpread[(upper,layer+1)]
    if sigma>20:
        Msize=50
    else:
        Msize=20
    return sigma,Msize
    
def smoot(pixel,energy,fromTCAD):    
    #matrixD=50
    matrixD=int(fromTCAD[1])
    sigma=float(fromTCAD[0])/5.5
    lIndex=matrixD-1
    theSum=0
    weights=np.zeros(shape=(matrixD,matrixD))
    #we start by finding the normalization so the charge is keept
    for i in range(matrixD):
        for k in range(matrixD):
            theSum+=exp((-i*i-k*k)/(2*sigma*sigma))*4.0
    check=0
    for i in range(matrixD):
        for k in range(matrixD):
            check+=(1.0/theSum)*exp((-i*i-k*k)/(2*sigma*sigma))
            weights[i,k]=(1.0/theSum)*exp((-i*i-k*k)/(2*sigma*sigma))
    #print "skal vare en ",check
    for i in range(1,lIndex):
        for k in range(1,lIndex):
            finalData.Fill((pixel[0]-i)/10.0,(pixel[1]-k)/10.0,energy*weights[i,k])
            finalData.Fill((pixel[0]-i)/10.0,(pixel[1]+k)/10.0,energy*weights[i,k])
            finalData.Fill((pixel[0]+i)/10.0,(pixel[1]-k)/10.0,energy*weights[i,k])
            finalData.Fill((pixel[0]+i)/10.0,(pixel[1]+k)/10.0,energy*weights[i,k])
    for i in range(1,lIndex):
        finalData.Fill((pixel[0]-i)/10.0,pixel[1]/10,energy*weights[i,0])
        finalData.Fill((pixel[0]+i)/10.0,pixel[1]/10,energy*weights[i,0])
        finalData.Fill((pixel[0]-i)/10.0,(pixel[1]+lIndex)/10,energy*weights[i,lIndex])
        finalData.Fill((pixel[0]+i)/10.0,(pixel[1]+lIndex)/10,energy*weights[i,lIndex])
        finalData.Fill((pixel[0]-i)/10.0,(pixel[1]-lIndex)/10,energy*weights[i,lIndex])
        finalData.Fill((pixel[0]+i)/10.0,(pixel[1]-lIndex)/10,energy*weights[i,lIndex])
    for k in range(1,lIndex):
        finalData.Fill((pixel[0])/10.0,(pixel[1]-k)/10,energy*weights[0,k])
        finalData.Fill((pixel[0])/10.0,(pixel[1]+k)/10,energy*weights[0,k])
        finalData.Fill((pixel[0]+lIndex)/10.0,(pixel[1]-k)/10,energy*weights[lIndex,k])
        finalData.Fill((pixel[0]+lIndex)/10.0,(pixel[1]+k)/10,energy*weights[lIndex,k])
        finalData.Fill((pixel[0]-lIndex)/10.0,(pixel[1]-k)/10,energy*weights[lIndex,k])
        finalData.Fill((pixel[0]-lIndex)/10.0,(pixel[1]+k)/10,energy*weights[lIndex,k])
    #corners
    finalData.Fill((pixel[0]-lIndex)/10.0,(pixel[1]-lIndex)/10,energy*weights[lIndex,lIndex])
    finalData.Fill((pixel[0]-lIndex)/10.0,(pixel[1])/10,energy*weights[lIndex,0])
    finalData.Fill((pixel[0]-lIndex)/10.0,(pixel[1]+lIndex)/10,energy*weights[lIndex,lIndex])
    finalData.Fill((pixel[0])/10.0,(pixel[1]-lIndex)/10,energy*weights[0,lIndex])
    finalData.Fill((pixel[0])/10.0,(pixel[1])/10,energy*weights[0,0])
    finalData.Fill((pixel[0])/10.0,(pixel[1]+lIndex)/10,energy*weights[0,lIndex])
    finalData.Fill((pixel[0]+lIndex)/10.0,(pixel[1]-lIndex)/10,energy*weights[lIndex,lIndex])
    finalData.Fill((pixel[0]+lIndex)/10.0,(pixel[1])/10,energy*weights[lIndex,0])
    finalData.Fill((pixel[0]+lIndex)/10.0,(pixel[1]+lIndex)/10,energy*weights[lIndex,lIndex])
def printToFile(histo, name):
    file.write("new\n")
    finalWithCut=TH2D(name,name,256,0,256,256,0,256)
    for i in range(256):
        for k in range(256):
            if(histo.GetBinContent(i,k)>5.0):
                finalWithCut.SetBinContent(i,k,histo.GetBinContent(i,k))
                file.write(str(i)+"  "+str(k)+"  "+str(histo.GetBinContent(i,k))+"\n")
    finalWithCut.Write()
                
totalEnergy=0
teller=0

def determineEnergyAround(event,thePixel,radius):    
    energy=0
    for pixel in event:
        if (pixel[0]-thePixel[0])*(pixel[0]-thePixel[0])+(pixel[1]-thePixel[1])*(pixel[1]-thePixel[1])<radius*radius:
            energy=energy+pixel[3]            
    return energy

def processOneEvent(event):
    for pixel in event:
        energyAround=determineEnergyAround(event,pixel,5)
        fileEnergy.write(str(energyAround)+"\n")
        energyAroundHisto.Fill(energyAround)
        smoot([pixel[0],pixel[1]],pixel[3],choseSigma(pixel[2],energyAround))
  

theEvent=[]
#plt.figure(0)
for line in open(sys.argv[1]):
#for line in open("../runningFLUKA/supersimpelTimepixCenter001_fort.22"):
    columns = line.split()
    if((len(columns)>0 and columns[0]=="Binning")):
        hasStarted=True
        print "teller",teller
        name="event"+str(teller)
        pixelNumber=0
        if len(theEvent)!=0: 
            processOneEvent(theEvent)
        printToFile(finalData,name)
        theEvent=[]
        #finalData.Write()
        #initialData.Write()
        finalData=TH2D("final"+str(teller),"final"+str(teller),256,0,256,256,0,256)
        initialData=TH2D("initial"+str(teller),"initial"+str(teller),256,0,2560,256,0,2560)
        teller+=1
        continue
    if(hasStarted==False or (len(columns)>0 and columns[0]=="Number")):
        continue
    for i in range(len(columns)):
        if(pixelNumber%2==0):
            thePixel=int(columns[i])
        if(pixelNumber%2!=0):
            z=thePixel/(2560*2560)
            pixelData=[((thePixel-z*2560*2560)/2560),((thePixel-2560*2560*z)%2560),z,float(columns[i])*1000000]
            initialData.Fill(((thePixel-z*2560*2560)/2560),((thePixel-2560*2560*z)%2560),float(columns[i])*1000000)
            theEvent.append(pixelData)
            # totalEnergy+=float(columns[i])
            # energy=float(columns[i])*1000000
            # #smoot([thePixel/2560,thePixel%2560],energy,choseSigma(energy))
        pixelNumber+=1

name="event"+str(teller)
teller+=1
if len(theEvent)!=0: 
    processOneEvent(theEvent)
printToFile(finalData,name)
finalData.Write()
myFile.Write()
#radius.Draw("colz")
#energyAroundHisto.Draw()
fileEnergy.close()
plt.show()




