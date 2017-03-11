import sys
import math
import sys
import numpy as np
from scipy import linspace, polyval, polyfit, sqrt, stats, randn
from ROOT import gROOT, TCanvas,TH1D,TH2D,TFile,TStyle,TLegend,TPave,TPaveStats,TPad,TPaveLabel,gStyle,gPad,TPaletteAxis,TLine
antall=0
total=0
histo=TH1D("","",67,0,670)
for line in open(sys.argv[1]):
    k=line.split()
    if k[0]=="new":
        print antall
        #print antall+total
        antall=0
        total=0
    else:
        histo.Fill(float(k[2]))

histo.Scale(1.0/histo.Integral())
histo.GetYaxis().SetRangeUser(0,0.30)
histo.Draw("hist")




histo2=TH1D("","",67,0,670)
for line in open(sys.argv[2]):
    k=line.split()
    if k[0]=="new":
        print antall
        #print antall+total
        antall=0
        total=0
    else:
        histo2.Fill(float(k[2]))

histo2.Scale(1.0/histo2.Integral())
histo2.SetLineColor(2)
histo2.Draw("hist same")


input()
