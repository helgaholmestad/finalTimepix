from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile,gStyle,gPad,TLegend
gROOT.Reset()
import numpy as np
import sys
print sys.argv
import os
import matplotlib.pyplot as plt


def makeCombinedPlot(histoMain,histoReference,log,name,xaxis):
    can=TCanvas()
    can.SetLeftMargin(0.2)
    #histos.Sumw2()
    #histosim.Draw("HIST")
    histoMain.Scale(1.0/histoMain.Integral())
    #histos.Scale(1.0/histos.Integral())
    histoReference.Scale(1.0/histoReference.Integral()) 
    gStyle.SetOptStat("");
    legend =TLegend(0.52,0.65,0.9,0.9);
    legend.AddEntry(histoMain,"Main data sample")
    legend.AddEntry(histoReference,"Reference sample")
    
    #histoReference.SetLineWidth(3)
    #histob.SetLineWidth(3)
    #combined.SetLineWidth(3) 
    #histob.SetFillColorAlpha(596,1)
    #histob.SetFillColorAlpha(3,0.5)
    #histob.SetLineColor(3)
    #combined.GetYaxis().SetRangeUser(10,scale*combined.GetMaximum())
    #combined.SetFillColor(840)
    histoReference.GetXaxis().SetTitle(xaxis)
    histoReference.GetYaxis().SetTitle("Normalized frequency")
    histoReference.GetXaxis().SetTitleSize(0.05)
    histoReference.GetYaxis().SetTitleSize(0.05)
    #combined.GetXaxis().SetTitleFont(131)
    #combined.GetYaxis().SetTitleFont(131)
    histoReference.GetYaxis().SetLabelSize(0.045)
    histoReference.GetXaxis().SetLabelSize(0.045)
    histoReference.GetXaxis().SetTitleOffset(0.83)
    histoReference.GetXaxis().SetNdivisions(5)
    histoMain.SetLineColorAlpha(1,0.3)
    histoReference.SetLineColorAlpha(4,0.8)
    histoMain.SetFillColorAlpha(1,0.3)
    histoReference.SetFillColorAlpha(4,0.8)
    histoReference.Draw("hist")
    histoMain.Draw("hist same")
    #histos.Draw("E1 same")
    #histosim.Draw("same")
    legend.SetTextFont(131)
    legend.SetTextSize(0.055)
    legend.Draw("same")
    can.SetBottomMargin(0.14)
    if log==True:
        can.SetLogy()
    can.Print("/home/helga/gitThesis/thesis/GraceTimepix/fig/compare"+str(name)+".pdf")

    
signalEnergy=TH1D("","",20,0,25000)
signalProng=TH1D("","",5,-0.5,4.5)
signalSize=TH1D("","",10,0,400)
signalTotalCharge=TH1D("","",18,0,35000)

backgroundEnergy=TH1D("","",20,0,25000)
backgroundProng=TH1D("","",5,-0.5,4.5)
backgroundSize=TH1D("","",10,0,400)
backgroundTotalCharge=TH1D("","",18,0,35000)

hasStarted=False
tagged=0
prongCut=1
sizeCut=70
#for line in open("../dataAnalysis/datafiles/sammenligne.txt"):
for line in open("../dataAnalysis/datafiles/meta.txt"):
    columns=line.split()
    if columns[0]=="energy":
        hasStarted=True
        centerEnergy=float(columns[1])
        signalEnergy.Fill(float(columns[1]))
    if columns[0]=="pixels":
        pixels= float(columns[1])
        signalSize.Fill(float(columns[1]))
    if columns[0]=="clusterCharge":
        totalEnergy=float(columns[1])
        signalTotalCharge.Fill(float(columns[1]))
    if columns[0]=="prong":
        prong= int(columns[1])
    if columns[0]=="error":
        error=float(columns[1])
        if error<1.0:
            prong=0
            signalProng.Fill(0)
        else:
            signalProng.Fill(prong)
    #if columns[0]=="newCluster" and hasStarted:
    #    if prong>=prongCut and pixels>=sizeCut:
    #        signalEnergyTagged.Fill(centerEnergy)
    #        signalProngTagged.Fill(prong)
    #        signalSizeTagged.Fill(pixels)
    #        signalTotalChargeTagged.Fill(totalEnergy)
    #        tagged+=1
hasStarted=False
taggedBackground=0
totalBackground=0
for line in open("../dataAnalysis/reversedDatafiles/meta.txt"):
    columns=line.split()
    if columns[0]=="energy":
        hasStarted=True
        centerEnergy=float(columns[1])
        backgroundEnergy.Fill(float(columns[1]))
    if columns[0]=="pixels":
        pixels= float(columns[1])
        backgroundSize.Fill(float(columns[1]))
    if columns[0]=="prong":
        prong= int(columns[1])
    if columns[0]=="clusterCharge":
        totalEnergy=float(columns[1])
        backgroundTotalCharge.Fill(float(columns[1]))
    if columns[0]=="error":
        error=float(columns[1])
        if error<1.0:
            prong=0
            backgroundProng.Fill(0)
        else:
            backgroundProng.Fill(prong)
    #if columns[0]=="newCluster" and hasStarted:
    #    totalBackground+=1
    #    if prong>=prongCut and pixels>=sizeCut:
    #        backgroundEnergyTagged.Fill(centerEnergy)
    #        backgroundProngTagged.Fill(prong)
    #        backgroundSizeTagged.Fill(pixels)
    #        backgroundTotalChargeTagged.Fill(totalEnergy)
    #        taggedBackground+=1

print "taggedb",taggedBackground


makeCombinedPlot(signalSize.Clone(),backgroundSize.Clone(),True,"ClusterSize","  Pixels ")

makeCombinedPlot(signalProng.Clone(),backgroundProng.Clone(),True,"ClusterProng","Prongs ")

makeCombinedPlot(signalEnergy.Clone(),backgroundEnergy.Clone(),True,"ClusterCenterEnergy"," [keV]  ")

makeCombinedPlot(signalTotalCharge.Clone(),backgroundTotalCharge.Clone(),True,"ClusterTotalEnergy"," [keV] ")



#makeCombinedPlot(simuSizeTagged.Clone(),signalSizeTagged.Clone(),backgroundSizeTagged.Clone(),combiSizeTagged.Clone(),1,True,"sizeTagged","# pixels",10,p,False)
#makeCombinedPlot(simuEnergyTagged.Clone(),signalEnergyTagged.Clone(),backgroundEnergyTagged.Clone(),combiEnergyTagged.Clone(),1,True,"centerEnergyTagged","keV",10,p,False)
#makeCombinedPlot(simuProngTagged.Clone(),signalProngTagged.Clone(),backgroundProngTagged.Clone(),combiProngTagged.Clone(),1,True,"prongsTagged","# prongs",30,p,False)
#makeCombinedPlot(simuTotalChargeTagged.Clone(),signalTotalChargeTagged.Clone(),backgroundTotalChargeTagged.Clone(),combiTotalChargeTagged.Clone(),1,True,"chargeTagged","keV",10,p,False)
