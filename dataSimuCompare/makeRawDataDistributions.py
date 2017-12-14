import math
import sys
import os
import numpy as np
from ROOT import gROOT, TCanvas,TH1D,TH2D,TFile,TStyle,TLegend,TPave,TPaveStats,TPad,TPaveLabel,gStyle,gPad,TPaletteAxis,TLine
gROOT.Reset()

gStyle.SetOptStat("");
histoPions=TH1D("","",30,0,30)
hasStarted=False
lessThan6keV=0
totalFill=0
for line in open("../simu/runningFLUKA/testPion001_fort.22"):
    columns = line.split()
    if((len(columns)>0 and columns[0]=="Binning")):
        hasStarted=True
        continue
    if(hasStarted==False or (len(columns)>0 and columns[0]=="Number")):
        continue 
    for i in range(len(columns)):
        if(i%2!=0):
            e=float(columns[i])*1000000
            histoPions.Fill(e)
            totalFill+=1
            if e<6.0:
              lessThan6keV+=1  


                            

rootdir="/home/helga/TimepixArticle/data/newTimepixFiles/"
dataPixelHistoRaw=TH1D("","",30,0,30)

for subdir, dirs, files in os.walk(rootdir):
    print(subdir)
    for file in files:
        if os.path.isfile(subdir+"/"+file) and "data_" in file and "test27" in subdir:
            for line in open(subdir+"/"+file,'r'):
                columns=line.split()
                if columns[0]=="pix_col":
                    continue
                dataPixelHistoRaw.Fill(float(columns[4]))


canvas2=TCanvas()

#histoPions.GetXaxis().SetTitle("energy deposited in 20 um silicon [keV]")
histoPions.GetXaxis().SetTitle("Measured energy deposition [keV]")
histoPions.GetYaxis().SetTitle("Normalized frequency")
histoPions.Scale(1.0/histoPions.Integral())
histoPions.GetYaxis().SetRangeUser(0.0,0.4)
histoPions.Draw("histo")

dataPixelHistoRaw.SetLineColor(2)
dataPixelHistoRaw.Scale(1.0/dataPixelHistoRaw.Integral())
dataPixelHistoRaw.GetXaxis().SetTitle("Measured energy deposition [keV]")
dataPixelHistoRaw.GetXaxis().SetTitle("Normalized frequency")
histoPions.GetYaxis().SetTitleSize(0.046)
histoPions.GetXaxis().SetTitleSize(0.046)
dataPixelHistoRaw.Draw("histo same")
#gPad.SetLogy()
                
legend2 =TLegend(0.55,0.53,0.9,0.9);
legend2.SetTextSize(0.035)
legend2.AddEntry(histoPions,"#splitline{A MIP transversing}{ 27.5 um of silicon}")
legend2.AddEntry(dataPixelHistoRaw,"#splitline{Energy measured in the}{ pixels for the main dataset}")
legend2.Draw("same")
canvas2.Print("../../../fig/pixelDistribution.pdf")


print("less than 6keV",lessThan6keV*100.0/totalFill)                
            
