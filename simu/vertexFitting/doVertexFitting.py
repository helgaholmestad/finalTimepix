#!/usr/bin/python
import math
import sys
import os
import numpy as np
from ROOT import gROOT, TCanvas,TH1D,TH2D,TFile,TStyle,TLegend,TPave,TPaveStats,TPad,TPaveLabel,gStyle,gPad,TPaletteAxis,TLine
gROOT.Reset()
from scipy import stats
import sympy
from sympy import *
import math
import scipy.odr.odrpack as odrpack
from numpy import polyfit
from math import fabs
from math import sqrt
#list of tracks contains for each event the  a list of the pixels 

def f(B,x):
    return B[0]*x+B[1]

def fitTrack(trackArray):
    results=[]
    x=[]
    y=[]
    energy=[]
    for i in trackArray:
        x.append(i[0])
        y.append(i[1])
        energy.append(i[2])
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    mydata=odrpack.Data(x,y,energy,energy)
    linear =odrpack.Model(f)
    myodr=odrpack.ODR(mydata,linear,beta0=[slope,intercept])
    myoutput= myodr.run()
    results.append(myoutput.beta)
    return results

def findTwoLongest(tracks):
    if len(tracks[0])>len(tracks[1]):
        long1=tracks[0]
        long2=tracks[1]
    else:
        long1=tracks[1]
        long2=tracks[0]
    for i in range(2,len(tracks),1):
        if len(tracks[i])>long1:
            long2=long1
            long1=tracks[i]
        elif len(tracks[i])>long2:
            long2=tracks[1]
    return [long1,long2]


listOfTracks=[]
track=[]
results2D=[]
resultsSimple2D=[]
results=[]
resultsSimple=[]
resultsCombined=[]
onedstart=-300
onedstop=300
onedbin=250
twodstart=-250
twodstop=250
twodbin=100
histo=TH2D("","",twodbin,twodstart,twodstop,twodbin,twodstart,twodstop)
histo1D=TH1D("","",onedbin,onedstart,onedstop)
histoSimple=TH2D("","",twodbin,twodstart,twodstop,twodbin,twodstart,twodstop)
histoSimple1D=TH1D("","",onedbin,onedstart,onedstop)
event=0
def lengthOfTracs(prong):
    maxx=0
    minx=1000
    maxy=0
    miny=1000
    for i in prong:
        x=i[0]
        y=i[1]
        if x>maxx:
            maxx=x
        if x<minx:
            minx=x
        if y>maxy:
            maxy=y
        if y<miny:
            miny=y
    deltax=maxx-minx
    deltay=maxy-miny
    return 55.0*np.sqrt(deltax*deltax+deltay*deltay)

            
def averageEnergyPerPixel(prong1,prong2):
    totalEnergy=0
    for pixel in prong1:
        totalEnergy=totalEnergy+pixel[2]
    for pixel in prong2:
        totalEnergy=totalEnergy+pixel[2]
    return totalEnergy*1.0/(len(prong1)+len(prong2))



def debutPrint(angle,prong1,prong2):
    can=TCanvas()
    histo=TH2D(str(angle),str(angle),256,0,256,256,0,256)
    for i in prong1:
        histo.Fill(i[0],i[1],i[2])
    for i in prong2:
        histo.Fill(i[0],i[1],i[2])
    histo.Draw("colz")
    can.Print("fig/"+str(angle)+".png")
    
def angleBetween(x,y,fit1,fit2,prong1,prong2):
    m1=(fit1[0][0])
    m2=(fit2[0][0])
    totalAngle=180.0*(np.arctan(m1)-np.arctan(m2))/np.pi
    return np.abs(totalAngle)
 

def findVertex(listOfTracks,centerx,centery,truthx,truthy):
    bestAngle=400
    bestValue=(0,0)
    foundGood=False
    bestFit=10000
    if len(listOfTracks)<2:
        return None
    while len(listOfTracks)>1:
        fit1=fitTrack(listOfTracks[0])
        length1=lengthOfTracs(listOfTracks[0])
        for i in range(1,len(listOfTracks),1):
            length2=lengthOfTracs(listOfTracks[i])
            length=0.5*(length1+length2)
            fit2=fitTrack(listOfTracks[i])
            resultx=(fit1[0][1]-fit2[0][1])/(fit2[0][0]-fit1[0][0])
            resulty=fit2[0][0]*resultx+fit2[0][1]
            #excluding events are fitted to be outside the detector
            #if resultx<0 or resulty<0 or resulty>256 or resulty>256:
            #    continue
            fromCenter=np.sqrt((centerx-resultx)*(centerx-resultx)+(centery-resulty)*(centery-resulty))*55
            angle= angleBetween(centerx,centery,fit1,fit2,listOfTracks[0],listOfTracks[1])
            offset=np.abs(90-angle)
            fromTruth=55.0*np.sqrt((truthx-resultx)*(truthx-resultx)+(truthy-resulty)*(truthy-resulty))
            numberOfPixels=(len(listOfTracks[0])+len(listOfTracks[1]))*0.5
            file.write(str(length)+"  "+str(offset)+"  "+str(fromTruth)+"  "+str(fromCenter)+"  "+str(numberOfPixels)+"\n")
            fileprong.write(str(resultx)+"  "+str(resulty)+" "+str(offset)+"\n")
            #if offset<bestAngle:# and fromCenter<80:
            #if fromCenter<bestFit:
           #     bestFit=fromCenter
           #     foundGood=True
           #     bestAngle=offset
           #     bestValue=(resultx,resulty)
        listOfTracks.remove(listOfTracks[0])
    fileprong.write("end"+"  "+str(truthx)+"  "+str(truthy)+"  "+str(centerx)+"  "+str(centery)+"  "+str(offset)+"\n")
    if foundGood==False:
        return None
    return bestValue[0],bestValue[1],angle,fit1,fit2

truthDict={}
for line in open("../runningFLUKA/truthValues.txt",'r'):
    values=line.split()
    event=int(values[0])
    truth=(float(values[1]),float(values[2]))
    truthDict[event]=truth

event=-1
antall=0

fileprong=open("threeprong.txt",'w')
file=open("corrData.txt",'w')
for line in open(sys.argv[1],'r'):
    columns=line.split()
    if columns[0]=="new" and columns[1]=="cluster":
        event+=1
    if columns[0]=="center":
        massCenterx=float(columns[1])
        massCentery=float(columns[2])
        centerx=(float(columns[1])-truthDict[event][0])*55.0
        centery=(float(columns[2])-truthDict[event][1])*55.0
        if centerx<225:
            histoSimple.Fill(centerx,centery)
        histoSimple1D.Fill(centerx)
        histoSimple1D.Fill(centery)
        resultsSimple.append(np.abs(centerx))
        resultsSimple.append(np.abs(centery))
        resultsSimple2D.append(np.sqrt(centerx*centerx+centery*centery))
    if columns[0]=="pixel":
        info=[int(columns[1]),int(columns[2]),float(columns[3])]
        track.append(info)
    if columns[0]=="pixelsInProng":
        listOfTracks.append(track)
        track=[]
    if columns[0]=="trough":
        if len(listOfTracks)<2:
            listOfTracks=[]
            continue            
        theVertex= findVertex(listOfTracks,massCenterx,massCentery,truthDict[event][0],truthDict[event][1])
        if theVertex==None:
            listOfTracks=[]
            continue
        distancex,distancey,angle,fit1,fit2=theVertex
        distancex=(distancex-truthDict[event][0])*55.0
        distancey=(distancey-truthDict[event][1])*55.0
        histo1D.Fill(distancex)
        histo1D.Fill(distancey)
        histo.Fill(distancex,distancey)
        results.append(np.abs(distancex))
        results.append(np.abs(distancey))
        results2D.append(np.sqrt(distancex*distancex+distancey*distancey))
        resultsCombined.append(np.abs(centerx+distancex)*0.5)
        resultsCombined.append(np.abs(centery+distancey)*0.5)
        listOfTracks=[]
    if columns[0]=="notTrough":
        listOfTracks=[]
# print "antall gode", antall
# gStyle.SetOptStat("");        
# gStyle.SetFrameLineColor(0); 

# twodsize=1.0*(twodstop-twodstart)/twodbin
# onedsize=1.0*(onedstop-onedstart)/onedbin
# can=TCanvas()
# can.SetLeftMargin(0.12)
# can.SetRightMargin(0.2)
# can.SetBottomMargin(0.15)
# histo.Draw("colz")
# histo.Scale(1.0/(twodsize*twodsize))
# histo.GetXaxis().SetTitle("Residual [#mum]")
# histo.GetYaxis().SetTitle("Residual [#mum]")
# histo.GetXaxis().SetTitleSize(0.05)
# histo.GetYaxis().SetTitleSize(0.05)
# histo.GetXaxis().SetLabelSize(0.045)
# histo.GetYaxis().SetLabelSize(0.045)
# histo.GetXaxis().SetTitleOffset(1.1)
# histo.GetYaxis().SetTitleOffset(1.1)
# #histo.GetZaxis().SetTitle("Normalized frequency")
# #histo.GetZaxis().SetTitleSize(0.06)
# #histo.GetZaxis().SetTitleOffset(0.7)
# gStyle.SetOptStat("")
# gStyle.SetFrameLineColor(0); 
# gPad.Update()
# palette=histo.GetListOfFunctions().FindObject("palette")
# #can.SetRightMargin(0.2)
# #can.SetBottomMargin(0.15)
# #can.SetLeftMargin(0.15)
# palette.SetX1NDC(0.75)
# palette.SetX2NDC(0.77)
# palette.SetY1NDC(0.15)
# palette.SetY2NDC(0.9)
# histo.GetZaxis().SetTitle("Frequency [1.0/#mum^2]")
# histo.GetZaxis().SetTitleSize(0.05)
# histo.GetZaxis().SetTitleOffset(1.3)
# gPad.Modified()
# can.Print("../../fig/2dfit.pdf")



# canS=TCanvas()
# canS.SetBottomMargin(0.15)
# histoSimple.Draw("colz")
# histoSimple.Scale(1.0/(twodsize*twodsize))
# histoSimple.GetXaxis().SetTitle("Residual [#mum]")
# histoSimple.GetYaxis().SetTitle("Residual [#mum]")
# histoSimple.GetXaxis().SetTitleSize(0.05)
# histoSimple.GetYaxis().SetTitleSize(0.05)
# histoSimple.GetXaxis().SetLabelSize(0.045)
# histoSimple.GetYaxis().SetLabelSize(0.045)
# histoSimple.GetXaxis().SetTitleOffset(1.1)
# histoSimple.GetYaxis().SetTitleOffset(1.1)
# gStyle.SetOptStat("")
# gStyle.SetFrameLineColor(0); 
# gPad.Update()
# palette=histoSimple.GetListOfFunctions().FindObject("palette")
# canS.SetRightMargin(0.2)
# canS.SetLeftMargin(0.15)
# palette.SetX1NDC(0.75)
# palette.SetX2NDC(0.77)
# palette.SetY1NDC(0.15)
# palette.SetY2NDC(0.9)
# histoSimple.GetZaxis().SetTitle("Frequency [1.0/#mum^2]")
# histoSimple.GetZaxis().SetTitleSize(0.05)
# histoSimple.GetZaxis().SetTitleOffset(1.3)
# gPad.Modified()
# canS.Print("../../fig/2dfitSimple.pdf")




# gStyle.SetFrameLineColor(0); 
# can1=TCanvas()
# can1.SetBottomMargin(0.15)
# can1.SetLeftMargin(0.15)
# histo1D.Draw("histo")
# histo1D.Scale(1.0/onedsize)
# histo1D.GetXaxis().SetTitle("Residual [#mum]")
# histo1D.GetYaxis().SetTitle("Frequency [1.0/#mum]")
# histo1D.GetXaxis().SetTitleSize(0.05)
# histo1D.GetYaxis().SetTitleSize(0.05)
# histo1D.GetXaxis().SetLabelSize(0.045)
# histo1D.GetYaxis().SetLabelSize(0.045)

# histo1D.GetXaxis().SetTitleOffset(1.1)
# histo1D.GetYaxis().SetTitleOffset(1.1)
# can1.Print("../../fig/1dfit.pdf")




# gStyle.SetFrameLineColor(0); 
# can1=TCanvas()
# can1.SetBottomMargin(0.15)
# can1.SetLeftMargin(0.15)
# histoSimple1D.Draw("histo")
# histoSimple1D.Scale(1.0/onedsize)
# histoSimple1D.GetXaxis().SetTitle("Residual [#mum]")
# histoSimple1D.GetYaxis().SetTitle("Frequency [1.0/#mum]")
# histoSimple1D.GetXaxis().SetTitleSize(0.05)
# histoSimple1D.GetYaxis().SetTitleSize(0.05)
# histoSimple1D.GetXaxis().SetLabelSize(0.045)
# histoSimple1D.GetYaxis().SetLabelSize(0.045)
# histoSimple1D.GetXaxis().SetTitleOffset(1.1)
# histoSimple1D.GetYaxis().SetTitleOffset(1.1)
# can1.Print("../../fig/1dfitSimple.pdf")




# squaredResults=np.square(results)
# squaredResults.sort()
# print "rms",np.sqrt(sum(squaredResults)*1.0/(len(squaredResults)))

# results.sort()
# results2D.sort()
# print results
# print "hvor mange er tilpasset",len(results)
# print "hvor stor andel tilpasset", len(results)*1.0/40000
# print "estimated sigma", results[int(len(results)*0.68)]
# print "estimated sigma 2d", results2D[int(len(results2D)*0.68)]


# resultsSimple.sort()
# resultsSimple2D.sort()
# print "hvor mange er tilpasset",len(resultsSimple)
# print "hvor stor andel tilpasset", len(resultsSimple)*1.0/40000
# print "estimated sigma", resultsSimple[int(len(resultsSimple)*0.68)]
# print "estimated sigma 2D", resultsSimple2D[int(len(resultsSimple2D)*0.68)]
