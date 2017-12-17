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
#filename="/home/helga/sortedData/46um/bending6000/20151004_46umDeg_all3000V/01_20151004_135756/test27_datadriven_AD/data_14.dat"
filename="../../../data/illustrations/data_14.dat"
#for line in open("../sortedData/46um/bending6000/20151003_46umDeg_all3000V/00_20151003_171600/test27_datadriven_AD/data_2.dat"):
for line in open(filename):
    columns=line.split()
    if columns[0]=="new" or columns[0]=="pix_col":
        continue
    if float(columns[4])<5.0:
        continue
    tmp.Fill(float(columns[5]))

gStyle.SetOptStat("")

    
modeTime= tmp.GetBinCenter(tmp.GetMaximumBin())
print modeTime
modeTime= 360590.0
timeDistro=TH1D("","",200,-500,1500)

print modeTime
for line in open(filename):
    columns=line.split()
    if columns[0]=="new" or columns[0]=="pix_col":
        continue
    if float(columns[5])>modeTime+600 and float(columns[5])<modeTime+3000:
         uncleanedHisto.Fill(float(columns[0]),float(columns[1]),float(columns[4]))
    if float(columns[4])<5.0:
        continue
    d=float(columns[5])-modeTime
    timeDistro.Fill(d)
    if float(columns[5])>modeTime+600 and float(columns[5])<modeTime+3000:
        slowHisto.Fill(float(columns[0]),float(columns[1]),float(columns[4]))
    #    print line


canvas1=TCanvas()

timeDistro.GetXaxis().SetTitle("Time of arrival [ns]")
timeDistro.GetXaxis().SetTitleSize(0.05)
timeDistro.GetYaxis().SetTitleSize(0.05)
timeDistro.GetYaxis().SetTitle("Frequency [ns]")
timeDistro.Draw()
canvas1.Print("../../../fig/timeDistro.pdf")
    

canvas=TCanvas()
slowHisto.Draw("colz")
slowHisto.GetXaxis().SetTitle("pixel #")
slowHisto.GetYaxis().SetTitle("pixel #")
slowHisto.GetXaxis().SetTitleSize(0.05)
slowHisto.GetYaxis().SetTitleSize(0.05)
slowHisto.GetZaxis().SetTitleSize(0.05)
slowHisto.GetZaxis().SetTitle("Measured energy deposition [keV]")
slowHisto.GetZaxis().SetTitleOffset(0.7)

gStyle.SetOptStat("")
gPad.Update()
palette=slowHisto.GetListOfFunctions().FindObject("palette")
canvas.SetRightMargin(0.1)
palette.SetX1NDC(0.9)
palette.SetX2NDC(0.925)
#palette.SetY1NDC(0.1)
#palette.SetY2NDC(0.9)
gPad.Modified()
canvas.Print("../../../timepixArticle/fig/fullFrame.pdf")


canvas=TCanvas()
uncleanedHisto.Draw("colz")
uncleanedHisto.GetXaxis().SetTitle("pixel #")
uncleanedHisto.GetYaxis().SetTitle("pixel #")
uncleanedHisto.GetXaxis().SetTitleSize(0.05)
uncleanedHisto.GetYaxis().SetTitleSize(0.05)
uncleanedHisto.GetZaxis().SetTitleSize(0.05)
uncleanedHisto.GetZaxis().SetTitle("Measured energy deposition [keV]")
uncleanedHisto.GetZaxis().SetTitleOffset(0.7)

gStyle.SetOptStat("")
gPad.Update()
palette=uncleanedHisto.GetListOfFunctions().FindObject("palette")
canvas.SetRightMargin(0.1)
palette.SetX1NDC(0.9)
palette.SetX2NDC(0.925)
#palette.SetY1NDC(0.1)
#palette.SetY2NDC(0.9)
gPad.Modified()
canvas.Print("../../../timepixArticle/fig/fullFrameUncleaned.pdf")

