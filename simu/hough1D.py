#!/usr/bin/python
import math
import sys
import numpy as np
import os
import scipy 
from scipy import linspace, polyval, polyfit, sqrt, stats, randn
from ROOT import gROOT, TCanvas,TH1D,TH2D,TFile,TStyle,TLegend,TPave,TPaveStats,TPad,TPaveLabel,gStyle,gPad,TPaletteAxis,TLine
gROOT.Reset()

couldGoWrongClusters=0

def linearRegression(histogram):
    x=[]
    y=[]
    for i in range(1,257):
        for k in range(1,257):
            if histogram.GetBinContent(i,k)!=0:
                x.append(i)
                y.append(k)
    if len(x)==0:
        histogram.Draw("colz")
        input()
    (ar,br)=polyfit(x,y,1)
    xr=polyval([ar,br],x)
    err=sqrt(sum((xr-y)**2)/len(y))
    if abs(ar)>1.0:
        (ar,br)=polyfit(y,x,1)
        xr=polyval([ar,br],y)
        err=sqrt(sum((xr-x)**2)/len(y))
    return err


def findMassCenter(histogram):
    def findCircle(x,y,histogram):
        pixelsInside=0
        density=histogram.GetBinContent(x,y)
        radius=5
        for i in range(1,radius,1):
            for j in range(1,radius,1):        
                if i*j<radius*radius:
                    density=density+histogram.GetBinContent(x+i,y+j)
                    if histogram.GetBinContent(x+i,y+j)!=0:
                        pixelsInside=pixelsInside+1
                    density=density+histogram.GetBinContent(x-i,y-j)
                    if histogram.GetBinContent(x-i,y-j)!=0:
                        pixelsInside=pixelsInside+1
                    density=density+histogram.GetBinContent(x-i,y+j)
                    if histogram.GetBinContent(x-i,y+j)!=0:
                        pixelsInside=pixelsInside+1
                    density=density+histogram.GetBinContent(x+i,y-j)
                    if histogram.GetBinContent(x+i,y-j)!=0:
                        pixelsInside=pixelsInside+1
        return density,pixelsInside
    def calculateMassCenter(x,y,histogram):
        radius=5
        averagex=x*histogram.GetBinContent(x,y)
        averagey=y*histogram.GetBinContent(x,y)
        theSum=histogram.GetBinContent(x,y)
        print "the sum",theSum
        for i in range(1,radius,1):
            for j in range(1,radius,1):        
                if i*j<radius*radius:
                    theSum=theSum+histogram.GetBinContent(x+i,y+j)+histogram.GetBinContent(x+i,y-j)+histogram.GetBinContent(x-i,y+j)+histogram.GetBinContent(x-i,y-j)
                    averagex=averagex+(x+i)*histogram.GetBinContent(x+i,y+j)
                    averagex=averagex+(x+i)*histogram.GetBinContent(x+i,y-j)
                    averagex=averagex+(x-i)*histogram.GetBinContent(x-i,y+j)
                    averagex=averagex+(x-i)*histogram.GetBinContent(x-i,y-j)
                    averagey=averagey+(y+j)*histogram.GetBinContent(x+i,y+j)
                    averagey=averagey+(y-j)*histogram.GetBinContent(x+i,y-j)
                    averagey=averagey+(y+j)*histogram.GetBinContent(x-i,y+j)
                    averagey=averagey+(y-j)*histogram.GetBinContent(x-i,y-j)
        return averagex/theSum,averagey/theSum
    density=0
    inside=0
    center=[0]*2
    center[0]=0
    center[1]=0
    for i in range(256):
        for j in range(256):
            if histogram.GetBinContent(i,j)!=0:
                temp=findCircle(i,j,histogram)
                if temp[0]>density:
                    center[0]=i
                    center[1]=j
                    density=temp[0]
                    inside=temp[1]
    finalCenter=calculateMassCenter(center[0],center[1],histogram)
    return finalCenter,density,inside

def findClusterCharge(histogram):
    totalCharge=0
    for i in range(256):
        for k in range(256):
            totalCharge=totalCharge+histogram.GetBinContent(i,k)
    return totalCharge


def removeCenter(x,y,histogram):
    radius=5
    for i in range(256):
        for j in range(256):
            if (i-x)*(i-x)+(j-y)*(j-y)<radius*radius:
                histogram.SetBinContent(i,j,0)



def findRatio(x,y,histogram):
    ins=0
    out=0
    radius=7
    for i in range(256):
        for j in range(256):
            if (i-x)*(i-x)+(j-y)*(j-y)<radius*radius:
                ins=histogram.GetBinContent(i,j)+ins
            else:
                out=histogram.GetBinContent(i,j)+out
    if out==0:
        return 10000
    else:
        return ins*1.0/out
                
def addLinesOfCenter(x,y):
    line=TLine(0,y,x,y)
    line1=TLine(x,0,x,y)
    line.SetLineColor(2)
    line1.SetLineColor(2)
    #line1.Draw('same')
    #line.Draw('same')
    lines=[]
    lines.append(line1)
    lines.append(line)
    return lines

        
def newAccumulator(centerx,centery,histogram):
    accumulator=TH1D("accumulator","accumulator",100,-np.pi,np.pi)
    for i in range(256):
        for k in range(256):
            if histogram.GetBinContent(i,k)!=0:
                radius=np.sqrt(np.abs(centerx-i)*np.abs(centerx-i)+np.abs(centery-k)*np.abs(centery-k))
                if radius!=0:
                    theta=np.arccos((i-centerx)*1.0/radius)
                    if k-centery <0:
                        theta=-theta
                    accumulator.Fill(theta)
    return accumulator
                
def addLine(theta,centerx,centery):
    line=TLine(centerx,centery,centerx+200*np.cos(theta),centery+200*np.sin(theta))
    line.SetLineColor(2)
    return line

def removeLine(centerx,centery,maxTheta,histogram):
    originalNumberOfPixels=histogram.GetEntries()
    numberOfRemovedPixels=0
    for i in range(256):
        for j in range(256):
            pixelInfo="pixel  "+str(i)+"  "+str(j)+"  "+str(histogram.GetBinContent(i,j))+"\n"
            if histogram.GetBinContent(i,j)!=0:
                radius=np.sqrt(np.abs(centerx-i)*np.abs(centerx-i)+np.abs(centery-j)*np.abs(centery-j))
                if radius!=0:
                    theta=np.arccos((i-centerx)*1.0/radius)
                    if j-centery <0:
                        theta=-theta
                    if abs(theta-maxTheta)<(20.0/180)*np.pi:
                        histogram.SetBinContent(i,j,0)
                        numberOfRemovedPixels=numberOfRemovedPixels+1
                    if abs(theta)> 3.0 and abs(maxTheta)>3.0:
                        histogram.SetBinContent(i,j,0)
                        numberOfRemovedPixels=numberOfRemovedPixels+1
    return histogram,numberOfRemovedPixels


if os.path.isfile(sys.argv[2]):
    os.remove(sys.argv[2])
meta=open(sys.argv[2],'w')

tfile = TFile.Open(sys.argv[1],'READ')
event=2
print "number of keys",sys.argv[1],len(tfile.GetListOfKeys())

teller=0
numberNone=0
print "list of keys"
for test in tfile.GetListOfKeys():
    tfile.Get(test)
for k in tfile.GetListOfKeys():
    if k>1000:
        continue
    teller+=1
    histogramD=k.ReadObj()
    if histogramD==None or histogramD.GetEntries()<10:
        numberNone+=1
        print "none"
        continue
    if histogramD.GetEntries()==0:
        continue
    histogram=histogramD.Clone()
    lines=[]
    center=findMassCenter(histogram)
    clusterCharge=findClusterCharge(histogram)
    histogramCenter=histogram.Clone()
    removeCenter(center[0][0],center[0][1],histogram)
    ratio=findRatio(center[0][0],center[0][1],histogramCenter)
    accumulator=newAccumulator(center[0][0],center[0][1],histogram)
    prong=0
    while True:
        maxBin=accumulator.GetMaximumBin()
        #can=TCanvas()
        #histogram.Draw('colz')
        #can.Print(sys.argv[2]+'event'+str(event)+'removed'+str(prong)+'.png')
        if accumulator.GetBinContent(maxBin)<4:
            break
        max=accumulator.GetXaxis().GetBinCenter(accumulator.GetMaximumBin())
        histogram,pixelsInLine=removeLine(center[0][0],center[0][1],max,histogram)
        pixelsLeft=histogramD.GetEntries()-pixelsInLine
        lines.append(addLine(max,center[0][0],center[0][1]))
        accumulator=newAccumulator(center[0][0],center[0][1],histogram)
        prong=prong+1
    if histogramD.GetEntries()>10:
        error =linearRegression(histogramD)
    event=event+1
    meta.write("newCluster " +str(teller)+"\n")
    meta.write("energy "+str(center[1])+"\n")
    meta.write("pixels "+str(histogramD.GetEntries())+"\n")
    meta.write("prong "+str(prong)+"\n")
    meta.write("clusterCharge "+str(clusterCharge) +"\n")
    meta.write("error "+str(error)+"\n")
    if prong>2 and histogramD.GetEntries()>100:
        couldGoWrongClusters+=1
    if error >1.0 and prong>0 and histogramD.GetEntries()>70:
        meta.write("trough"+'\n')
    else:
        meta.write("notTrough"+'\n')
    event +=1
    title=histogramD.GetTitle()
    print "hva er title",title
    clusterNumber=title.split("cluster")[0].split("event")[1]
    meta.write("clusterNumber "+str(clusterNumber)+"\n")
    
    
print "antall none",numberNone
print "antall som kan ga galt",couldGoWrongClusters

































# lines=[]
# numberOfTracks=2
# for k in range(numberOfTracks):
#     newAccumulator(center[0][0],center[0][1])
#     max=accumulator.GetXaxis().GetBinCenter(accumulator.GetMaximumBin())
#     print "max", 180*max/np.pi
#     lines.append(addLine(max,center[0][0],center[0][1]))
#     #accumulator.Draw()
#     #input()
#     #theta=accumulator.GetYaxis().GetBinCenter(max/102)
#     #p=accumulator.GetXaxis().GetBinCenter(max%102)
#     #removeLine(p,theta)
#     #accumulator.SetBinContent(max,0)

# #name="density "+ str(center[1])+ "  "+str(center[2])
# #histogramOriginal.SetTitle(name)
# #histogramOriginal.Draw('colz')
# #lines=addLinesOfCenter(center[0][0],center[0][1])

# #histogramOriginal.Draw('colz')
# for k in lines:
#     k.Draw('same')
#     canvas.Update()

# #accumulator.Draw()
# canvas.Print(str(sys.argv[3]))
