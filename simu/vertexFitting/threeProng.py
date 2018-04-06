#!/usr/bin/python
import math
import sys
import os
import numpy as np
from ROOT import gROOT, TCanvas,TH1D,TH2D,TFile,TStyle,TLegend,TPave,TPaveStats,TPad,TPaveLabel,gStyle,gPad,TPaletteAxis,TLine,TLatex
gROOT.Reset()
from scipy import stats
#import sympy
#from sympy import *
import math
import scipy.odr.odrpack as odrpack
from numpy import polyfit
from math import fabs
from math import sqrt
#list of tracks contains for each event the  a list of the pixels 

onedstart=-300
onedstop=300
onedbin=250
twodstart=-550
twodstop=550
twodbin=100
histo=TH2D("","",twodbin,twodstart,twodstop,twodbin,twodstart,twodstop)
histo1D=TH1D("","",onedbin,onedstart,onedstop)
histoSimple=TH2D("","",twodbin,twodstart,twodstop,twodbin,twodstart,twodstop)
histoSimple1D=TH1D("","",onedbin,onedstart,onedstop)

def findClosestToNintyAngle(t,a):
    i=a.index(min(a))
    return t[i]

def findDistanceToMassCenter(x,y,xm,ym):
    fromCenter=np.sqrt((xm-x)*(xm-x)+(y-ym)*(y-ym))*55
    return fromCenter
    
def processOneEvent(x,y,tx,ty,xm,ym,a):
    estimatex=None
    estimatey=None
    if len(x)==1:
        estimatex,estimatey=x[0],y[0]
    elif len(x)>1:
        estimatex,estimatey=findEstimate(x,y,xm,ym,a)
    if estimatex==None or estimatey==None:
        return None,None
    if findDistanceToMassCenter(estimatex,estimatey,xm,ym)>110.0:
        return None,None
    residualx=estimatex-tx
    residualy=estimatey-ty
    return residualx,residualy


def findEstimate(x,y,mx,my,a):
    bestIndex=[]
    for n in range(len(x)):
        t=[]
        for m in range(len(x)):
            diff=np.sqrt((x[n]-x[m])*(x[n]-x[m])+(y[n]-y[m])*(y[n]-y[m]))
            if diff<1.0:
                t.append(m)
        if len(t)>len(bestIndex):
            bestIndex=t
        xnew=[x[i] for i in bestIndex]
        ynew=[y[i] for i in bestIndex]
    print "find sum of",xnew,ynew
    if len(xnew)==1:
        return findClosestToNintyAngle(x,a),findClosestToNintyAngle(y,a)
        #return findClosestToMassCenter(x,mx),findClosestToMassCenter(y,my)
    return sum(xnew)*1.0/len(bestIndex),sum(ynew)*1.0/len(bestIndex)
x=[]
y=[]
a=[]
residual=[]
residualSimple=[]
antallEvents=0
for line in open(sys.argv[1],'r'):
    data=line.split()
    if data[0]=="end":
        antallEvents+=1
        xt=float(data[1])
        yt=float(data[2])
        xm=float(data[3])
        ym=float(data[4])
        histoSimple.Fill((xm-xt)*55.0,(ym-yt)*55.0)
        histoSimple1D.Fill((xm-xt)*55.0)
        histoSimple1D.Fill((ym-yt)*55.0)
        residualSimple.append(abs((xm-xt)*55.0))
        residualSimple.append(abs((ym-yt)*55.0))
        rx,ry=processOneEvent(x,y,xt,yt,xm,ym,a)
        x=[]
        y=[]
        a=[]
        if rx==None or ry==None:
            continue
        histo.Fill(rx*55.0,ry*55.0)
        histo1D.Fill(rx*55.0)
        histo1D.Fill(ry*55.0)  
        residual.append(abs(rx*55.0))
        residual.append(abs(ry*55.0))
        continue
    x.append(float(data[0]))
    y.append(float(data[1]))
    a.append(float(data[2]))
residual=np.array(residual)
residual = residual[np.isfinite(residual)]
residual.sort()
proportion=len(residual)/40000.0
print "vertex fitting method"
print proportion
print residual[int(len(residual)*0.68)]
residualSimple=np.array(residualSimple)
residualSimple = residualSimple[np.isfinite(residualSimple)]
residualSimple.sort()
print "mass center method"
print len(residualSimple)
print residualSimple[int(len(residualSimple)*0.68)]



#make plots

gStyle.SetOptStat("");        
gStyle.SetFrameLineColor(0); 

twodsize=1.0*(twodstop-twodstart)/twodbin
onedsize=1.0*(onedstop-onedstart)/onedbin
can=TCanvas()
can.SetLeftMargin(0.12)
can.SetRightMargin(0.2)
can.SetBottomMargin(0.15)
histo.Draw("colz")
histo.Scale(1.0/(twodsize*twodsize))
histo.GetXaxis().SetTitle("Residual [#mum]")
histo.GetYaxis().SetTitle("Residual [#mum]")
histo.GetXaxis().SetTitleSize(0.072)
histo.GetYaxis().SetTitleSize(0.072)
histo.GetXaxis().SetTitleOffset(0.95)
histo.GetYaxis().SetTitleOffset(0.95)
histo.GetXaxis().SetLabelSize(0.05)
histo.GetYaxis().SetLabelSize(0.05)
#histo.GetZaxis().SetTitle("Normalized frequency")
#histo.GetZaxis().SetTitleSize(0.06)
#histo.GetZaxis().SetTitleOffset(0.7)
gStyle.SetOptStat("")
gStyle.SetFrameLineColor(0); 
gPad.Update()
palette=histo.GetListOfFunctions().FindObject("palette")
can.SetRightMargin(0.2)
can.SetLeftMargin(0.15)
#can.SetRightMargin(0.2)
#can.SetBottomMargin(0.15)
#can.SetLeftMargin(0.15)
palette.SetX1NDC(0.75)
palette.SetX2NDC(0.77)
palette.SetY1NDC(0.15)
palette.SetY2NDC(0.9)
histo.GetZaxis().SetTitle("Frequency [1.0/#mum^{2}]")
histo.GetZaxis().SetTitleSize(0.072)
histo.GetZaxis().SetTitleOffset(0.9)
gPad.Modified()
can.Print("../../../../timepixArticle/fig/2dfit.pdf")



canS=TCanvas()
canS.SetBottomMargin(0.15)
histoSimple.Draw("colz")
histoSimple.Scale(1.0/(twodsize*twodsize))
histoSimple.GetXaxis().SetTitle("Residual [um]")
histoSimple.GetYaxis().SetTitle("Residual [um]")
histoSimple.GetXaxis().SetTitleSize(0.072)
histoSimple.GetYaxis().SetTitleSize(0.072)
#histoSimple.GetXaxis().SetTitleFont(131)
#histoSimple.GetYaxis().SetTitleFont(131)
histoSimple.GetXaxis().SetLabelSize(0.05)
histoSimple.GetYaxis().SetLabelSize(0.05)
histoSimple.GetXaxis().SetTitleOffset(0.95)
histoSimple.GetYaxis().SetTitleOffset(0.95)
gStyle.SetOptStat("")
gStyle.SetFrameLineColor(0); 
gPad.Update()
palette=histoSimple.GetListOfFunctions().FindObject("palette")
canS.SetRightMargin(0.2)
canS.SetLeftMargin(0.15)
palette.SetX1NDC(0.75)
palette.SetX2NDC(0.77)
palette.SetY1NDC(0.15)
palette.SetY2NDC(0.9)
histoSimple.GetZaxis().SetTitle("Frequency [1.0/#mum^{2}]")
histoSimple.GetZaxis().SetTitleSize(0.072)
histoSimple.GetZaxis().SetTitleOffset(0.9)
gPad.Modified()
canS.Print("../../../../timepixArticle/fig/2dfitSimple.pdf")




gStyle.SetFrameLineColor(0); 
can1=TCanvas()
can1.SetBottomMargin(0.15)
can1.SetLeftMargin(0.15)
histo1D.Draw("histo")
histo1D.Scale(1.0/onedsize)
histo1D.GetXaxis().SetTitle("Residual [#mum]")
histo1D.GetYaxis().SetTitle("Frequency [1.0/#mum]")
histo1D.GetXaxis().SetTitleSize(0.072)
histo1D.GetYaxis().SetTitleSize(0.072)
#histo1D.GetXaxis().SetTitleFont(131)
#histo1D.GetYaxis().SetTitleFont(131)
histo1D.GetXaxis().SetLabelSize(0.05)
histo1D.GetYaxis().SetLabelSize(0.05)

histo1D.GetXaxis().SetTitleOffset(0.95)
histo1D.GetYaxis().SetTitleOffset(0.95)
can1.Print("../../../../timepixArticle/fig/1dfit.pdf")




gStyle.SetFrameLineColor(0); 
can1=TCanvas()
can1.SetBottomMargin(0.15)
can1.SetLeftMargin(0.2)
histoSimple1D.Draw("histo")
histoSimple1D.Scale(1.0/onedsize)
histoSimple1D.GetXaxis().SetTitle("Residual [#mum]")
histoSimple1D.GetYaxis().SetTitle("Frequency [1.0/#mum]")
histoSimple1D.GetXaxis().SetTitleSize(0.072)
histoSimple1D.GetYaxis().SetTitleSize(0.072)
#histoSimple1D.GetXaxis().SetTitleFont(131)
#histoSimple1D.GetYaxis().SetTitleFont(131)

histoSimple1D.GetXaxis().SetLabelSize(0.05)
histoSimple1D.GetYaxis().SetLabelSize(0.05)
histoSimple1D.GetXaxis().SetTitleOffset(0.95)
histoSimple1D.GetYaxis().SetTitleOffset(0.95)

can1.Print("../../../../timepixArticle/fig/1dfitSimple.pdf")




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
print "totalt antall events",antallEvents
