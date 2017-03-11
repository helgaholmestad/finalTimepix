from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile,gStyle,gPad
gROOT.Reset()
import numpy as np
import sys
print sys.argv
import os


rootdir="/home/helga/newTimepixFiles"
timeDistro=TH1D("","",200,500,3000)
recoveredDistro=TH1D("","",200,500,3000)
test=TH2D("","",100,0,100,200,300,3000)


def makeCountingHistogram(filename):
    listOfRecoveredPixels=[]
    tmpPixel=[]
    tmp=TH2D("","",256,0,256,256,0,256)
    orignial={}
    recovered={}
    for line in open(filename):
        columns=line.split()
        if columns[0]=="new" or columns[0]=="pix_col":
            continue
        x=int(columns[0])
        y=int(columns[1])
        if tmp.GetBinContent(x+1,y+1)==1:
            tmpPixel=[x,y,float(columns[5])]
            recovered[(x,y)]=(float(columns[4]),float(columns[5]))
            listOfRecoveredPixels.append(tmpPixel)
        else:
            tmp.Fill(x,y,1)
            orignial[(x,y)]=(float(columns[4]),float(columns[5]))
    orignialS=set(orignial)
    recoveredS=set(recovered)
    for name in orignialS.intersection(recovered):
        print orignial[name][0],recovered[name][0]
        test.Fill(orignial[name][0],recovered[name][1]-orignial[name][1])
        #recoveredDistro.Fill(abs(orignial[name]-recovered[name]))
    tmp.Draw("colz")
   # print "recovered pixels"
    #for i in range(256):
    #    for k in range(256):
    #        if tmp.GetBinContent(i,k)==2:
    #            print i,k
    return listOfRecoveredPixels
  

def findmodeTime(filename):
    tmp=TH1D("","",40000,0,400000)
    print filename
    for line in open(filename):
        columns=line.split()
        if columns[0]=="new" or columns[0]=="pix_col":
            continue
        #if float(columns[4])<6.0:
        #    continue
        tmp.Fill(float(columns[5]))
    modeTime= tmp.GetBinCenter(tmp.GetMaximumBin())
    return modeTime

def addToHistogram(filename,modeTime,recoveredPixels):
    for line in open(filename):
        columns=line.split()
        if columns[0]=="new" or columns[0]=="pix_col":
            continue
        d=float(columns[5])-modeTime
        timeDistro.Fill(d)
    for pixel in recoveredPixels:
        recoveredDistro.Fill(pixel[2]-modeTime)
        #print pixel[2]-modeTime


for subdir, dirs, files in os.walk(rootdir):
    if "last" in subdir:
        continue
    for file in files:
        if os.path.isfile(subdir+"/"+file) and "data" in file and "test27" in subdir:
            #print subdir+"/"+file
            modeTime=findmodeTime(subdir+"/"+file)
            listOfRecovered=makeCountingHistogram(subdir+"/"+file)
            addToHistogram(subdir+"/"+file,modeTime,listOfRecovered)
            break

test.Draw("colz")
input()
canvas1=TCanvas()
timeDistro.SetLineColor(2)
timeDistro.GetXaxis().SetTitle("Time of arrival [ns]")
timeDistro.GetXaxis().SetTitleSize(0.05)
timeDistro.GetYaxis().SetTitleSize(0.05)
timeDistro.GetYaxis().SetTitle("Frequency ")
timeDistro.Scale(1.0/timeDistro.Integral())
recoveredDistro.Scale(1.0/recoveredDistro.Integral())
recoveredDistro.Draw()
timeDistro.Draw("same")
input()
# canvas1.Print("../fig/totalTimeDistro.pdf")
# canvas1.Print("/home/helga/Presantations/MedipixMeeting2017/fig/totalTimeDistro.pdf")
    
