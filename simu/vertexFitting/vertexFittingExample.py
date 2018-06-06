#!/usr/bin/python
import math
import sys
import os
import numpy as np
from ROOT import gROOT, TCanvas,TH1D,TH2D,TFile,TStyle,TLegend,TPave,TPaveStats,TPad,TPaveLabel,gStyle,gPad,TPaletteAxis,TLine
gROOT.Reset()
import scipy.optimize as opt
from scipy import stats
#import sympy
#from sympy import *
import math
import scipy.odr.odrpack as odrpack
from numpy import polyfit
from math import fabs
from math import sqrt
#list of tracks contains for each event the  a list of the pixels

def fv(B,x,a1,b1):
    return B[0]*x+b1-B[0]*a1

def minThis(vertex,trackArray):
    sumOfSquares=0
    for i in range(len(trackArray)):
        x=[]
        y=[]
        energy=[]
        #print trackArray
        for i in trackArray[i]:
            x.append(i[0])
            y.append(i[1])
            energy.append(i[2])
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        mydata=odrpack.Data(x,y,energy,energy)
        linear =odrpack.Model(fv,extra_args=vertex)
        myodr=odrpack.ODR(mydata,linear,beta0=[slope,intercept])
        myoutput= myodr.run()
        sumOfSquares+=myoutput.sum_square
    return sumOfSquares


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


def angleBetween(fit1,fit2,prong1,prong2):
    m1=(fit1[0][0])
    m2=(fit2[0][0])
    totalAngle=180.0*(np.arctan(m1)-np.arctan(m2))/np.pi
    return np.abs(totalAngle)
 

def findVertex(listOfTracks,centerx,centery):
    bestAngle=400
    bestValue=(0,0)
    foundGood=False
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
            if resultx<0 or resulty<0 or resulty>256 or resulty>256:
                continue
            fromCenter=np.sqrt((centerx-resultx)*(centerx-resultx)+(centery-resulty)*(centery-resulty))*55
            angle= angleBetween(fit1,fit2,listOfTracks[0],listOfTracks[1])
            offset=np.abs(90-angle)
            numberOfPixels=(len(listOfTracks[0])+len(listOfTracks[1]))*0.5
            allResults.write("vertex "+str(resultx)+"  "+str(resulty)+"  "+str(offset)+"\n")
        listOfTracks.remove(listOfTracks[0])
    if foundGood==False:
        return None
    return bestValue[0],bestValue[1],angle,fit1,fit2

event=-1
antall=0

allResults=open(sys.argv[2],'w')
for line in open(sys.argv[1],'r'):
    columns=line.split()
    if columns[0]=="new" and columns[1]=="cluster":
        event+=1
    if columns[0]=="center":
        massCenterx=float(columns[1])
        massCentery=float(columns[2])
    if columns[0]=="pixel":
        info=[int(columns[1]),int(columns[2]),float(columns[3])]
        track.append(info)
    if columns[0]=="pixelsInProng":
        listOfTracks.append(track)
        track=[]
    if columns[0]=="done":
        allResults.write("new cluster \n")
        allResults.write("massCenter  "+str(massCenterx)+"  "+str(massCentery)+"\n")
        if len(listOfTracks)<2:
            listOfTracks=[]
            continue
        theVertex= findVertex(listOfTracks,massCenterx,massCentery)
        if theVertex==None:
            listOfTracks=[]
            continue
        listOfTracks=[]
        
