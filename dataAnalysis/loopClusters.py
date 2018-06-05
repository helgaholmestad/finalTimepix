from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile
gROOT.Reset()
import numpy as np
import sys
print sys.argv
import os
import os.path
import re
pixelList=[]
distanceT=20.
distanceR=6.1

if len(sys.argv)==2:
    rootdir=sys.argv[1]
else:
    rootdir='../../../data'
#clustering algorithm here
fileS=open("stat",'w')
def plotClusters(filepath):
    histogram=TH2D("clusterNumber1","clusterNumber1",256,0,256,256,0,256)
    histogramTotal=TH2D("total","total",256,0,256,256,0,256)
    histogramTime=TH1D("default","default",1,0,1)
    outputRootFile=filepath.replace("clustering","histograms").replace(".dat",".root")
    myFile=TFile(outputRootFile,"RECREATE")
    clusterNumber=0
    hasStarted=False
    average=0
    modeTime=0
    totalTime=0
    numberOfPixels=0
    fileS.write("new\n")
    print "working with file ",filepath
    for line in open(filepath):
        columns = line.split()
        if columns[0]=="new":
            if hasStarted==False:
                modeTime=float(columns[2])
                histogramTime=TH1D("ToA","ToA",200,-1000,3000)
            #if hasStarted and histogram.GetEntries()>10 and histogram.GetEntries()<1000:
            if hasStarted and histogram.GetEntries()>0 and histogram.GetEntries()<1000:
                average=totalTime/(1.0*numberOfPixels)
                delay=average-modeTime
                fileS.write(str(histogram.GetEntries())+"\n")
                if delay>1000:
                    histogram.SetTitle("delayed "+str(delay))
                    histogram.Write()
                    clusterNumber=clusterNumber+1
            del histogram
            totalTime=0
            numberOfPixels=0
            #modeTime=float(columns[2])
            histogram=TH2D("clusterNumber "+str(clusterNumber),"clusterNumber ",256,0,256,256,0,256)
        else:
            numberOfPixels=numberOfPixels+1
            totalTime=float(columns[3])+totalTime
            histogram.Fill(int(columns[0]),int(columns[1]),float(columns[2]))
            histogramTotal.Fill(int(columns[0]),int(columns[1]),float(columns[2]))
            histogramTime.Fill(float(columns[3])-modeTime)
            hasStarted=True
    histogramTotal.Write()
    histogramTime.Write()
    del histogramTime
    del histogramTotal
    del histogram
    myFile.Write()

            


for subdir, dirs, files in os.walk(rootdir):
   # if not "80um" in subdir:
    #    continue
    #if not "bending6000" in subdir:
    #    continue
    for file in files:
        if os.path.isfile(subdir+"/"+file) and "clustering" in file and "test27" in subdir:
            plotClusters(subdir+"/"+file)


