#!/usr/bin/python
import math
import sys
import os
import numpy as np
from ROOT import gROOT, TCanvas,TH1D,TH2D,TFile,TStyle,TLegend,TPave,TPaveStats,TPad,TPaveLabel,gStyle,gPad,TPaletteAxis,TLine,TGraph
gROOT.Reset()
from scipy import stats
#import sympy
#from sympy import *
import math
import scipy.odr.odrpack as odrpack
from numpy import polyfit
from math import fabs
from math import sqrt

results=[]
test2d=TH2D("","",256,0,256,256,0,256)
test=TH1D("","",100,0,90)
histo=TH2D("","",100,-200,200,100,-200,200)
histo1D=TH1D("","",200,0,200)
prongAngle=[]
prongLength=[]
prongSize=[]
massCenter=[]
accuracy=[]
event=0

meanD=0
meanA=0
meanL=0
meanS=0
meanC=0
numberOfLines=0
for line in open("corrData.txt",'r'):
    length,angle,center,distance,size=line.split()
    if length=="nan" or angle=="nan" or center=="nan" or distance=="nan":
        continue
    length,angle,distance,center,size=float(length),float(angle),float(center),float(distance),float(size)
    #distance,angle,length1,length2,size1,size2,centerx,centery=line.split()
    #distance,angle,length1,length2,size1,size2,centerx,centery=float(distance),float(angle),float(length1),float(length2),float(size1),float(size2),float(centerx),float(centery)
    #center=np.sqrt(centerx*centerx+centery*centery)
    meanD+=distance
    meanA+=angle
    meanL+=length 
    meanC+=center
    meanS+=size
    numberOfLines+=1
    test.Fill(angle)
    prongAngle.append(angle)
    prongLength.append(length)
    prongSize.append(size)
    accuracy.append(distance)
    massCenter.append(center)
    #prongAngle.Fill(distance,angle)
    #prongLength.Fill(distance,0.5*(length1+length2))
meanD=meanD*1.0/numberOfLines
meanA=meanA*1.0/numberOfLines
meanL=meanL*1.0/numberOfLines
meanS=meanS*1.0/numberOfLines
meanC=meanC*1.0/numberOfLines
#test.Draw()
#input()
S_dd=0
S_aa=0
S_ll=0
S_da=0
S_dl=0
S_ss=0
S_ds=0
S_cc=0
S_dc=0
for line in open("corrData.txt",'r'):
    length,angle,center,distance,size=line.split()
    if length=="nan" or angle=="nan" or center=="nan" or distance=="nan":
        continue
    length,angle,distance,center,size=float(length),float(angle),float(center),float(distance),float(size)
    numberOfLines+=1
    length=length
    S_dd+=(distance-meanD)*(distance-meanD)
    S_aa+=(angle-meanA)*(angle-meanA)
    S_ll+=(length-meanL)*(length-meanL)
    S_cc+=(center-meanC)*(center-meanC)
    S_ss+=(size-meanS)*(size-meanS)
    S_da+=(distance-meanD)*(angle-meanA)
    S_dl+=(distance-meanD)*(length-meanL)
    S_dc+=(distance-meanD)*(center-meanC)
    S_ds+=(distance-meanD)*(size-meanS)
corrDistanceAngle=S_da*1.0/(np.sqrt(S_dd)*np.sqrt(S_aa))
corrDistanceLength=S_dl*1.0/(np.sqrt(S_dd)*np.sqrt(S_ll))
corrDistanceCenter=S_dc*1.0/(np.sqrt(S_dd)*np.sqrt(S_cc))
corrDistanceSize=S_ds*1.0/(np.sqrt(S_dd)*np.sqrt(S_ss))
print "correlation center",corrDistanceCenter
print "correlation angle",corrDistanceAngle
print "correlation length",corrDistanceLength
print "correlation size",corrDistanceSize

gStyle.SetOptStat("");        

accuracy=np.asarray(accuracy)
prongAngle=np.asarray(prongAngle)
prongLength=np.asarray(prongLength)
massCenter=np.asarray(massCenter)
prongSize=np.asarray(prongSize)

can2=TCanvas()
scatterCenter=TGraph(len(accuracy),accuracy,massCenter)
scatterCenter.SetTitle("")
scatterCenter.GetXaxis().SetTitleSize(0.05)
scatterCenter.GetYaxis().SetTitleSize(0.05)
scatterCenter.GetXaxis().SetTitleOffset(0.8)
scatterCenter.GetYaxis().SetTitleOffset(0.7)
scatterCenter.GetXaxis().SetRangeUser(0,5000)
scatterCenter.GetYaxis().SetRangeUser(0,5000)
scatterCenter.GetXaxis().SetTitle("Truth-fit [#mum]")
scatterCenter.GetYaxis().SetTitle("abs(Mass center - fit value) [#mum]")
scatterCenter.SetMarkerStyle(10)
scatterCenter.Draw('ap')
can2.Print("../../../../timepixArticle/fig/prongCenter.pdf")


can2=TCanvas()
scatterAngle=TGraph(len(accuracy),accuracy,prongAngle)
scatterAngle.SetTitle("")
scatterAngle.GetXaxis().SetRangeUser(0,200)
scatterAngle.GetXaxis().SetTitle("Truth -fit [#mum]")
scatterAngle.GetYaxis().SetTitle("abs(#theta -90)")
scatterAngle.SetMarkerStyle(20)
scatterAngle.GetXaxis().SetTitleSize(0.05)
scatterAngle.GetYaxis().SetTitleSize(0.05)
scatterAngle.GetXaxis().SetTitleOffset(0.8)
scatterAngle.GetYaxis().SetTitleOffset(0.7)
scatterAngle.Draw('ap')
can2.Print("../../../../timepixArticle/fig/prongAngle.pdf")


can2=TCanvas()
scatterLength=TGraph(len(accuracy),accuracy,prongLength)
scatterLength.SetTitle("")
scatterLength.GetYaxis().SetRangeUser(0,6000)
scatterLength.GetXaxis().SetRangeUser(0,200)
scatterLength.GetXaxis().SetTitle("Truth - fit [#mum]")
scatterLength.GetYaxis().SetTitle("[#mum]")
scatterLength.GetXaxis().SetTitleSize(0.05)
scatterLength.GetYaxis().SetTitleSize(0.05)
scatterLength.GetXaxis().SetTitleOffset(0.8)
scatterLength.GetYaxis().SetTitleOffset(0.7)
scatterLength.SetMarkerStyle(20)
scatterLength.Draw('ap')
# can2=TCanvas()
# prongAngle.GetXaxis().SetTitle("Orthogonal distance from center [mu]")
# prongAngle.GetYaxis().SetTitle("Angel between the two prongs fitted")
# prongAngle.Draw()
can2.Print("../../../../timepixArticle/fig/prongLength.pdf")

# can5=TCanvas()
# prongLength.GetXaxis().SetTitle("Orthogonal distance  from center [mu]")
# prongLength.GetYaxis().SetTitle("Average length of prongs fitted [mu]")
# prongLength.Draw()
# can5.Print("/home/helga/testbeamNewCleaning/fig/prongLength.pdf")

can2=TCanvas()
scatterSize=TGraph(len(accuracy),accuracy,prongSize)
scatterSize.SetTitle("")
scatterSize.GetXaxis().SetTitleSize(0.05)
scatterSize.GetYaxis().SetTitleSize(0.05)
scatterSize.GetXaxis().SetTitleOffset(0.8)
scatterSize.GetYaxis().SetTitleOffset(0.7)
scatterSize.GetXaxis().SetRangeUser(0,500)
scatterSize.GetYaxis().SetRangeUser(0,200)
scatterSize.GetXaxis().SetTitle("Truth-fit [#mum]")
scatterSize.GetYaxis().SetTitle("Number of pixels in the prongs")
scatterSize.SetMarkerStyle(20)
scatterSize.Draw('ap')
can2.Print("../../../../timepixArticle/fig/prongSize.pdf")
