from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile,gStyle,gPad
gROOT.Reset()
import numpy as np
import sys
print sys.argv
import os
slowHisto=TH2D("","",256,0,256,256,0,256)
uncleanedHisto=TH2D("","",256,0,256,256,0,256)

tmp=TH1D("","",40000,0,400000)
#name of f /home/helga/testbeamNewCleaning/sortedData/46um/bending6000/20151004_46umDeg_all3000V/01_20151004_135756/test27_datadriven_AD/histograms14.root
filename="/home/helga/testbeamNewCleaning/sortedData/46um/bending6000/20151004_46umDeg_all3000V/01_20151004_135756/test27_datadriven_AD/data_14.dat"
filename=sys.argv[1]
#for line in open("../sortedData/46um/bending6000/20151003_46umDeg_all3000V/00_20151003_171600/test27_datadriven_AD/data_2.dat"):

for line in open(filename):
    columns=line.split()
    if columns[0]=="new" or columns[0]=="pix_col":
        continue
    else:
        tmp.Fill(float(columns[5]))
        
modeTime= tmp.GetBinCenter(tmp.GetMaximumBin())        

for line in open(filename):
    columns=line.split()
    if columns[0]=="new" or columns[0]=="pix_col":
        continue
    elif  (float(columns[5])-modeTime)>1000:
        continue
    else:
        x = int(columns[0])
        y = int(columns[1])
        uncleanedHisto.Fill(x,y,1)

uncleanedHisto.Draw("colz")
input()


