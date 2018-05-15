import math
import sys
import os
import numpy as np
from ROOT import gROOT, TCanvas,TH1D,TH2D,TFile,TStyle,TLegend,TPave,TPaveStats,TPad,TPaveLabel,gStyle,gPad,TPaletteAxis,TLine
gROOT.Reset()

gStyle.SetOptStat("");
histoPions=TH1D("","",60,0,30)
hasStarted=False
lessThan6keV=0
totalFill=0
haloHits=0
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
dataPixelHistoRaw=TH1D("","",60,0,30)

for subdir, dirs, files in os.walk(rootdir):
    print(subdir)
    for file in files:
        if os.path.isfile(subdir+"/"+file) and "data_" in file and "test27" in subdir:
            for line in open(subdir+"/"+file,'r'):
                columns=line.split()
                if columns[0]=="pix_col":
                    continue
                eD=float(columns[4])
                dataPixelHistoRaw.Fill(eD)
                if eD<6.0:
                    haloHits+=1

dataPixelHistoRaw.Draw()
canvas2=TCanvas(
)
#histoPions.GetXaxis().SetTitle("energy deposited in 20 um silicon [keV]")
histoPions.GetXaxis().SetTitle("Measured energy deposition [keV]")
histoPions.GetYaxis().SetTitle("Normalized frequency")
histoPions.Scale(1.0/histoPions.Integral())
histoPions.GetYaxis().SetRangeUser(0.0,0.4)
histoPions.SetLineColor(1)
histoPions.SetLineWidth(3)
#histoPions.Draw("histo")

dataPixelHistoRaw.SetLineColor(1)
dataPixelHistoRaw.SetFillColorAlpha(596,1.0)
dataPixelHistoRaw.Scale(1.0/dataPixelHistoRaw.Integral())
dataPixelHistoRaw.GetXaxis().SetTitle("Measured energy deposition per pixel [keV]")
dataPixelHistoRaw.GetXaxis().SetTitleOffset(0.88)
dataPixelHistoRaw.GetYaxis().SetTitle("Normalized frequency")
dataPixelHistoRaw.GetYaxis().SetTitleSize(0.045)
dataPixelHistoRaw.GetXaxis().SetTitleSize(0.045)

#dataPixelHistoRaw.GetXaxis().SetTitleFont(131)
#dataPixelHistoRaw.GetYaxis().SetTitleFont(131)

dataPixelHistoRaw.Draw("histo ")
histoPions.Draw("histo same")
#canvasT=TCanvas()
#dataPixelHistoRaw.Draw("hist same")
#canvasT.Print("/home/helga/gitThesis/thesis/Annihilation/fig/energyInPixels.pdf")
#gPad.SetLogy()

legend2 =TLegend(0.5,0.6,0.9,0.9);
legend2.SetTextSize(0.043)
#legend2.AddEntry(histoPions,"#splitline{A MIP transversing}{ 39.2 um of silicon}")
#legend2.AddEntry(dataPixelHistoRaw,"#splitline{Energy measured in the}{ pixels for the main dataset}")
legend2.AddEntry(histoPions,"#splitline{A MIP traversing}{38.9 um of silicon.}")
legend2.AddEntry(dataPixelHistoRaw,"#splitline{Measured energy per}{#splitline{pixel for main dataset}{including the halo}}")
#legend2.SetTextFont(131)
legend2.Draw("same")
canvas2.Print("../../../timepixArticle/fig/pixelDistribution.pdf")


print("proportion halo hits",haloHits*100.0/dataPixelHistoRaw.GetEntries())
print("less than 4keV",lessThan6keV*100.0/totalFill)                
            
