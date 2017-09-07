from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile,gStyle,gPad
gROOT.Reset()
import numpy as np
import sys
print sys.argv
import os


rootdir="/home/helga/TimepixArticle/data/newTimepixFiles"
timeDistro=TH1D("","",200,-500,3000)

def findmodeTime(filename):
    tmp=TH1D("","",40000,0,400000)
    print filename
    for line in open(filename):
        columns=line.split()
        if columns[0]=="new" or columns[0]=="pix_col":
            continue
        if float(columns[4])<6.0:
            continue
        tmp.Fill(float(columns[5]))
    modeTime= tmp.GetBinCenter(tmp.GetMaximumBin())
    return modeTime

def addToHistogram(filename,modeTime):
    for line in open(filename):
        columns=line.split()
        if columns[0]=="new" or columns[0]=="pix_col":
            continue
        #if float(columns[5])>modeTime+300 and float(columns[5])<modeTime+3000:
        #   uncleanedHisto.Fill(float(columns[0]),float(columns[1]),float(columns[4]))
        #if float(columns[4])<6.0:
        #    continue
        d=float(columns[5])-modeTime
        timeDistro.Fill(d)




for subdir, dirs, files in os.walk(rootdir):
    if "last" in subdir:
        continue
    for file in files:
        if os.path.isfile(subdir+"/"+file) and "data" in file and "test27" in subdir:
            #print subdir+"/"+file
            modeTime=findmodeTime(subdir+"/"+file)
            addToHistogram(subdir+"/"+file,modeTime)

canvas1=TCanvas()
timeDistro.GetXaxis().SetTitle("Time of arrival [ns]")
timeDistro.GetXaxis().SetTitleSize(0.05)
timeDistro.GetYaxis().SetTitleSize(0.05)
timeDistro.GetYaxis().SetTitle("Frequency ")
timeDistro.Draw()
canvas1.Print("../../../fig/totalTimeDistro.pdf")
canvas1.Print("/home/helga/Presantations/MedipixMeeting2017/fig/totalTimeDistro.pdf")
    
