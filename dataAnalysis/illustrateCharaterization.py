#!/usr/bin/python
import math
import sys
import numpy as np
from scipy import linspace, polyval, polyfit, sqrt, stats, randn
#from ROOT import gROOT, TCanvas,TH1D,TH2D,TFile,TStyle,TLegend,TPave,TPaveStats,TPad,TPaveLabel,gStyle,gPad,TPaletteAxis,TLine
#gROOT.Reset()
from ROOT import gROOT,TCanvas,TH1D,TH2D,TFile,TStyle,TLegend,TPave,TPaveStats,TPad,TPaveLabel,gStyle,TPaletteAxis,TLine,gPad
#gROOT.Reset()


def printCanvas(histogram,title,theRange,maximum):
    can=TCanvas()
    histogram.Draw("colz")
    gStyle.SetOptStat("")
    histogram.SetTitle("")
    histogram.GetXaxis().SetTitle("pixel number")
    histogram.GetYaxis().SetTitle("pixel number")
    histogram.GetZaxis().SetTitle("measured energy in cells")
    histogram.GetXaxis().SetRangeUser(theRange[0]-20,theRange[1]+20)
    histogram.GetYaxis().SetRangeUser(theRange[2]-20,theRange[3]+20)
    histogram.GetZaxis().SetRangeUser(0,maximum)
    gPad.Update()
    palette=histogram.GetListOfFunctions().FindObject("palette")
    can.SetRightMargin(0.2)
    palette.SetX1NDC(0.8)
    palette.SetX2NDC(0.815)
    palette.SetY1NDC(0.1)
    palette.SetY2NDC(0.9)
    gPad.Modified()
    gPad.Update()
    
    print ("title",title)
    can.Print("test/"+str(title)+".png")
 
def linearRegression(histogram):
    x=[]
    y=[]
    for i in range(257):
        for k in range(257):
            if histogram.GetBinContent(i,k)!=0:
                x.append(i)
                y.append(k)
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
    return center,density,inside

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
    #prongs.write("prong \n")
    originalNumberOfPixels=histogram.GetEntries()
    numberOfRemovedPixels=0
    maxx=0
    minx=1000
    maxy=0
    miny=1000
    for i in range(256):
        for j in range(256):
            pixelInfo=str(i)+"  "+str(j)+"  "+str(histogram.GetBinContent(i,j))+"\n"
            if histogram.GetBinContent(i,j)!=0:
                radius=np.sqrt(np.abs(centerx-i)*np.abs(centerx-i)+np.abs(centery-j)*np.abs(centery-j))
                if radius!=0:
                    theta=np.arccos((i-centerx)*1.0/radius)
                    if j-centery <0:
                        theta=-theta
                    if abs(theta-maxTheta)<(20.0/180)*np.pi:
                        if i>maxx:
                            maxx=i
                        if i<minx:
                            minx=i
                        if j>maxy:
                            maxy=j
                        if j<miny:
                            miny=j
                        #prongs.write(pixelInfo)
                        histogram.SetBinContent(i,j,0)
                        numberOfRemovedPixels=numberOfRemovedPixels+1
                    if abs(theta)> 3.0 and abs(maxTheta)>3.0:
                        #prongs.write(pixelInfo)
                        histogram.SetBinContent(i,j,0)
                        numberOfRemovedPixels=numberOfRemovedPixels+1
    #prongs.write("pixelsInProng  "+str(numberOfRemovedPixels)+"\n")
    deltax=maxx-minx
    deltay=maxy-miny
    lengthOfProng=55.0*np.sqrt(deltax*deltax+deltay*deltay)           
    return histogram,numberOfRemovedPixels,lengthOfProng

def printCluster(histogram,taggedCluster):
    taggedCluster.write("new \n")
    for i in range(256):
        for k in range(256):
            if histogram.GetBinContent(i,k)!=0.0:
                taggedCluster.write(str(i)+"  "+str(k)+"  "+str(histogram.GetBinContent(i,k))+"\n")


tfile = TFile.Open("/home/helga/TimepixArticle/data/newTimepixFiles/20160528_33umAl_D1_0kV_D2_4kV_E1_5kV_E2_3kV_leadblocks/00_20160528_172838/test27_datadriven_AD/"+sys.argv[1],'READ')
event=0
noFile=False

def getBoundries(histogram):
    xmin=300
    ymin=300
    xmax=0
    ymax=0
    for i in range(256):
        for k in range(256):
            c=histogram.GetBinContent(i,k)
            if c<=0:
                continue
            else:
                if i>xmax:
                    xmax=i
                if i<xmin:
                    xmin=i
                if k>ymax:
                    ymax=k
                if k<ymin:
                    ymin=k
    meanx=0.5*(xmax+xmin)
    meany=0.5*(ymax+ymin)
    deltax=1.0*(xmax-xmin)
    deltay=1.0*(ymax-ymin)
    if deltax>deltay:
        ymax=meany+0.5*deltax
        ymin=meany-0.5*deltax
    else:
        xmax=meanx+0.5*deltay
        xmin=meanx-0.5*deltay
    return xmin,xmax,ymin,ymax


for k in range(len(tfile.GetListOfKeys())-3):
    pNumber=0
    #print ("er vi her")
    histogramD=  tfile.Get("clusterNumber "+str(k))
    histogram=histogramD.Clone()
    error =linearRegression(histogramD)
    if error>1.0:
        continue
    eventNumber=event+1
    if histogram.GetEntries()<70:
        print "continue"
        continue
    plotNumber=0
    theRange=getBoundries(histogram)
    maximum=histogram.GetMaximum()
    printCanvas(histogram,str(k)+str(plotNumber),theRange,maximum)
    lines=[]
    center=findMassCenter(histogram)
    clusterCharge=findClusterCharge(histogram)
    histogramCenter=histogram.Clone()
    removeCenter(center[0][0],center[0][1],histogram)
    plotNumber+=1
    printCanvas(histogram,str(k)+str(plotNumber),theRange,maximum)
    ratio=findRatio(center[0][0],center[0][1],histogramCenter)
    accumulator=newAccumulator(center[0][0],center[0][1],histogram)
    prong=0
    prongLenghts=[]
    while True:
        pNumber=pNumber+1
        maxBin=accumulator.GetMaximumBin()
        if accumulator.GetBinContent(maxBin)<4:
            break
        max=accumulator.GetXaxis().GetBinCenter(accumulator.GetMaximumBin())
        histogram,pixelsInLine,lengthOfProng=removeLine(center[0][0],center[0][1],max,histogram)
        prongLenghts.append(lengthOfProng)
        pixelsLeft=histogramD.GetEntries()-pixelsInLine
        lines.append(addLine(max,center[0][0],center[0][1]))
        accumulator=newAccumulator(center[0][0],center[0][1],histogram)
        prong=prong+1
        #print ("size",histogramD.GetEntries())
        plotNumber+=1
        printCanvas(histogram,str(k)+str(plotNumber),theRange,maximum)
      
