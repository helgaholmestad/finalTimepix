#!/usr/bin/python
import math
import sys
import numpy as np
from scipy import linspace, polyval, polyfit, sqrt, stats, randn
#from ROOT import gROOT, TCanvas,TH1D,TH2D,TFile,TStyle,TLegend,TPave,TPaveStats,TPad,TPaveLabel,gStyle,gPad,TPaletteAxis,TLine
#gROOT.Reset()
from ROOT import gROOT,TCanvas,TH1D,TH2D,TFile,TStyle,TLegend,TPave,TPaveStats,TPad,TPaveLabel,gStyle,TPaletteAxis,TLine
#gROOT.Reset()


def printCanvas(histogram,title):
    can=TCanvas()
    histogram.Draw("colz")
    gStyle.SetOptStat("")
    histogram.SetTitle("")
    histogram.GetXaxis().SetTitle("pixel number")
    histogram.GetYaxis().SetTitle("pixel number")
    histogram.GetZaxis().SetTitle("measured energy in cells")
    gPad.Update()
    palette=histogram.GetListOfFunctions().FindObject("palette")
    can.SetRightMargin(0.2)
    palette.SetX1NDC(0.8)
    palette.SetX2NDC(0.815)
    palette.SetY1NDC(0.1)
    palette.SetY2NDC(0.9)
    gPad.Modified()
    gPad.Update()
    print "title",title
    can.Print(title+".png")
 
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
                        #prongs.write(pixelInfo)
                        histogram.SetBinContent(i,j,0)
                        numberOfRemovedPixels=numberOfRemovedPixels+1
                    if abs(theta)> 3.0 and abs(maxTheta)>3.0:
                        #prongs.write(pixelInfo)
                        histogram.SetBinContent(i,j,0)
                        numberOfRemovedPixels=numberOfRemovedPixels+1
    #prongs.write("pixelsInProng  "+str(numberOfRemovedPixels)+"\n")
    return histogram,numberOfRemovedPixels


def printCluster(histogram,taggedCluster):
    taggedCluster.write("new \n")
    for i in range(256):
        for k in range(256):
            if histogram.GetBinContent(i,k)!=0.0:
                taggedCluster.write(str(i)+"  "+str(k)+"  "+str(histogram.GetBinContent(i,k))+"\n")


def hough(inputfile,pattern,folder):
    print "i hough"
    taggedCluster=open(folder+"/"+pattern+"taggedClusters.txt",'a')
    meta=open(folder+"/"+pattern+"meta.txt",'a')
    tfile = TFile.Open(inputfile,'READ')
    event=0
    prong0=0
    prong1=0
    prong2=0
    prong3=0
    prong4=0
    noFile=False
    if len(tfile.GetListOfKeys())>5:
        meta.write("newFile"+'\n')
    else:
        meta.write("noFile"+'\n')
        meta.close()
        return
    print len(tfile.GetListOfKeys())
    for k in range(len(tfile.GetListOfKeys())-3):
        pNumber=0
        print "er vi her"
        histogramD=  tfile.Get("clusterNumber "+str(k))
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
            pNumber=pNumber+1
            maxBin=accumulator.GetMaximumBin()
            if accumulator.GetBinContent(maxBin)<4:
                break
            max=accumulator.GetXaxis().GetBinCenter(accumulator.GetMaximumBin())
            histogram,pixelsInLine=removeLine(center[0][0],center[0][1],max,histogram)
            pixelsLeft=histogramD.GetEntries()-pixelsInLine
            lines.append(addLine(max,center[0][0],center[0][1]))
            accumulator=newAccumulator(center[0][0],center[0][1],histogram)
            prong=prong+1
        print "size",histogramD.GetEntries()
        error =linearRegression(histogramD)
        event=event+1
        meta.write("newCluster " +"\n")
        meta.write("energy "+str(center[1])+"\n")
        meta.write("pixels "+str(histogramD.GetEntries())+"\n")
        meta.write("prong "+str(prong)+"\n")
        meta.write("clusterCharge "+str(clusterCharge) +"\n")
        meta.write("error "+str(error)+"\n")
        #printCanvas(histogramCenter,str(sys.argv[2]+"event"+str(event)))
        if error >1.0 and prong>0 and center[1]>800:
            meta.write("trough"+'\n')
            printCluster(histogramD,taggedCluster)
        else:
            meta.write("notTrough"+'\n')
    meta.close()
#if __name__ == '__main__':
#    hough1D(inputfile,pattern,folder):
    
