from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile,gStyle,gPad
gROOT.Reset()
distanceR=4.1
import numpy
import random
import os
import sys
random.seed(3)
histoRaw=TH1D("","",500,0,5000)
file=open("datafilesJustVolcano/"+sys.argv[1]+"justVolcano.txt","w")
for line in open("datafilesJustVolcano/"+sys.argv[1]+"results.txt","r"):
    i=line.split()
    if len(columns)==1:
        file.write("new\n")
    elif i[2]<450:
        toWrite=str(str(i[0])+" "+str(i[1])+"  "+str(i[2])+"\n")
    else:
        randomEnergy=random.gauss(500,50)
        toWrite=str(str(i[0])+" "+str(i[1])+"  "+str(randomEnergy)+"\n")
    file.write(toWrite)

myFile=TFile("datafiles/histograms"+sys.argv[1]+"TCADjustVolcano.root","RECREATE")
finalWithCut=TH2D("event0","event0",256,0,256,256,0,256)
teller=0
for line in open("datafiles/"+sys.argv[1]+"justVolcano.txt","r"):
    columns=line.split()
    if columns[0]=="new":
        finalWithCut.Write()
        teller+=1
        name="event"+str(teller)
        finalWithCut=TH2D(name,name,256,0,256,256,0,256)
    else:
        finalWithCut.Fill(int(columns[0]),int(columns[1]),float(columns[2]))
finalWithCut.Write()
myFile.Write()

