#!/usr/bin/python
import math
import sys
import numpy as np
import os
import scipy 
from scipy import linspace, polyval, polyfit, sqrt, stats, randn
from ROOT import gROOT, TCanvas,TH1D,TH2D,TFile,TStyle,TLegend,TPave,TPaveStats,TPad,TPaveLabel,gStyle,gPad,TPaletteAxis,TLine
gROOT.Reset()

histo=TH1D("","",67,0,670)
antall=0
total=0
for line in open(sys.argv[1]):
    k=line.split()
    if k[0]=="new":
        pass
    else:
        histo.Fill(float(k[2]))

histo.Scale(1.0/histo.Integral())
histo.Draw()
input()
