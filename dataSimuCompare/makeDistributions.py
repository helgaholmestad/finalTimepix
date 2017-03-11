from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile,gStyle,gPad,TLegend
gROOT.Reset()
import numpy as np
import sys
print sys.argv
import os
import matplotlib.pyplot as plt

def calculateChiSquared(histosim,histos,histob,combined,p):
    histos.Sumw2()
    histos.Scale(1.0/histos.Integral())
    histob.Scale(1.0/histob.Integral())
    histosim.Scale(1.0/histosim.Integral())
    #combined.Scale(1.0/combined.Integral())
    for i in range(histos.GetXaxis().GetNbins()):
        combined.SetBinContent(i,p*histob.GetBinContent(i)+(1.0-p)*histosim.GetBinContent(i))
    chi=0
    for i in xrange(histos.GetXaxis().GetNbins()):
        diff=histos.GetBinContent(i)-combined.GetBinContent(i)
        thesum=histos.GetBinContent(i)+combined.GetBinContent(i)
        if thesum!=0:
            chi+=diff*diff/thesum
    return chi



def makeCombinedPlot(histosim,histos,histob,combined,yrange,log,name,xaxis,scale,pnumber):
    can=TCanvas()
    #histos.Sumw2()
    histosim.Draw("HIST")
    histosim.Scale((1.0-pnumber)*histos.Integral()/histosim.Integral())
    #histos.Scale(1.0/histos.Integral())
    histob.Scale(pnumber*histos.Integral()/histob.Integral())
    for i in range(histos.GetXaxis().GetNbins()+2):
        combined.SetBinContent(i,histob.GetBinContent(i)+histosim.GetBinContent(i))
    legend =TLegend(0.6,0.7,0.9,0.9);
    gStyle.SetOptStat("");
    legend.AddEntry(histos,"Data")
    legend.AddEntry(histob,"Fragments")
    legend.AddEntry(combined,"SimuP + Fragments")
    histos.SetLineWidth(3)
    #histob.SetLineWidth(3)
    #combined.SetLineWidth(3)
    histos.SetLineColor(2)
    combined.SetFillStyle(3005)
    #if log==False:
    #    histos.GetYaxis().SetRangeUser(0,yrange)
    combined.SetLineColor(4)
    histob.SetFillColor(3)
    #histob.SetFillColorAlpha(3,0.5)
    #histob.SetLineColor(3)
    combined.GetYaxis().SetRangeUser(1,scale*combined.GetMaximum())
    combined.SetFillColor(4)
    combined.GetXaxis().SetTitle(xaxis)
    combined.GetYaxis().SetTitle("Frequency")
    combined.GetXaxis().SetTitleSize(0.05)
    combined.GetYaxis().SetTitleSize(0.05)
    combined.Draw()
    histob.Draw("hist same")
    histos.Draw("E1 same")
    #histosim.Draw("same")
    legend.Draw("same")
    if log==True:
        can.SetLogy()
    can.Print("../fig/compare/"+str(name)+".png")

    
signalEnergy=TH1D("","",20,0,25000)
signalProng=TH1D("","",5,-0.5,4.5)
signalSize=TH1D("","",10,0,400)
signalTotalCharge=TH1D("","",18,0,35000)

simuEnergy=TH1D("","",20,0,25000)
simuProng=TH1D("","",5,-0.5,4.5)
simuSize=TH1D("","",10,0,400)
simuTotalCharge=TH1D("","",18,0,35000)

            
backgroundEnergy=TH1D("","",20,0,25000)
backgroundProng=TH1D("","",5,-0.5,4.5)
backgroundSize=TH1D("","",10,0,400)
backgroundTotalCharge=TH1D("","",18,0,35000)

combiEnergy=TH1D("","",20,0,25000)
combiProng=TH1D("","",5,-0.5,4.5)
combiSize=TH1D("","",10,0,400)
combiTotalCharge=TH1D("","",18,0,35000)



#For the tagged data
signalEnergyTagged=TH1D("","",25,0,25000)
signalProngTagged=TH1D("","",5,-0.5,4.5)
signalSizeTagged=TH1D("","",10,0,400)
signalTotalChargeTagged=TH1D("","",18,0,35000)

simuEnergyTagged=TH1D("","",25,0,25000)
simuProngTagged=TH1D("","",5,-0.5,4.5)
simuSizeTagged=TH1D("","",10,0,400)
simuTotalChargeTagged=TH1D("","",18,0,35000)

            
backgroundEnergyTagged=TH1D("","",25,0,25000)
backgroundProngTagged=TH1D("","",5,-0.5,4.5)
backgroundSizeTagged=TH1D("","",10,0,400)
backgroundTotalChargeTagged=TH1D("","",18,0,35000)

combiEnergyTagged=TH1D("","",25,0,25000)
combiProngTagged=TH1D("","",5,-0.5,4.5)
combiSizeTagged=TH1D("","",10,0,400)
combiTotalChargeTagged=TH1D("","",18,0,35000)

sizeCut=70
prongCut=1
centerEnergyCut=1000
energy=0
prong=0
pixel=0
centerEnergy=0
hasStarted=False
tagged=0
#for line in open("../dataAnalysis/datafiles/sammenligne.txt"):
for line in open("../dataAnalysis/theDatafiles/meta.txt"):
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
    if columns[0]=="newCluster" and hasStarted:
        if prong>=prongCut and pixels>=sizeCut:
            signalEnergyTagged.Fill(centerEnergy)
            signalProngTagged.Fill(prong)
            signalSizeTagged.Fill(pixels)
            signalTotalChargeTagged.Fill(totalEnergy)
            tagged+=1
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
    if columns[0]=="newCluster" and hasStarted:
        totalBackground+=1
        if prong>=prongCut and pixels>=sizeCut:
            print "her"
            backgroundEnergyTagged.Fill(centerEnergy)
            backgroundProngTagged.Fill(prong)
            backgroundSizeTagged.Fill(pixels)
            backgroundTotalChargeTagged.Fill(totalEnergy)
            taggedBackground+=1

print "taggedb",taggedBackground
            
hasStarted=False
#for line in open("/home/helga/testbeamNewCleaning/FLUKA/simulation/meta.txt"):
for line in open("../simu/datafiles/meta.txt"):
    columns=line.split()
    if columns[0]=="energy":
        centerEnergy=float(columns[1])
        simuEnergy.Fill(float(columns[1]))
        hasStarted=True
    if columns[0]=="pixels":
        pixels= float(columns[1])
        simuSize.Fill(float(columns[1]))
    if columns[0]=="clusterCharge":
        totalEnergy=float(columns[1])
        simuTotalCharge.Fill(float(columns[1]))
    if columns[0]=="prong":
        prong= int(columns[1])
    if columns[0]=="error":
        error=float(columns[1])
        if error<1.0:
            simuProng.Fill(0)
        else:
            simuProng.Fill(prong)
    if columns[0]=="newCluster" and hasStarted:
        if prong>=prongCut and pixels>=sizeCut:
            simuEnergyTagged.Fill(centerEnergy)
            simuProngTagged.Fill(prong)
            simuSizeTagged.Fill(pixels)
            simuTotalChargeTagged.Fill(totalEnergy)
            
            

p2=0
minimum=100000000000
for i in np.arange(0,1,0.01):
    totalChiSquared=calculateChiSquared(simuProng.Clone(),signalProng.Clone(),backgroundProng.Clone(),combiProng.Clone(),i)
    if minimum>totalChiSquared:
        minimum=totalChiSquared
        p2=i
p3=0
minimum=100000000000
for i in np.arange(0,1,0.01):
    totalChiSquared=calculateChiSquared(simuEnergy.Clone(),signalEnergy.Clone(),backgroundEnergy.Clone(),combiEnergy.Clone(),i)
    if minimum>totalChiSquared:
        minimum=totalChiSquared
        p3=i
p4=0
minimum=100000000000
for i in np.arange(0,1,0.01):
    totalChiSquared=calculateChiSquared(simuTotalCharge.Clone(),signalTotalCharge.Clone(),backgroundTotalCharge.Clone(),combiTotalCharge.Clone(),i)
    if minimum>totalChiSquared:
        minimum=totalChiSquared
        p4=i

minimum=100000000000
p1=0
y=[]
x=[]
totalChiSquared=0
for i in np.arange(0,1,0.01):
    totalChiSquared=calculateChiSquared(simuSize.Clone(),signalSize.Clone(),backgroundSize.Clone(),combiSize.Clone(),i)
    x.append(i)
    y.append(totalChiSquared)
    if minimum>totalChiSquared:
        minimum=totalChiSquared
        p1=i

p=0
minimum=100000000000
y=[]
x=[]
for i in np.arange(0,1,0.01):
    totalChiSquared=calculateChiSquared(simuTotalCharge.Clone(),signalTotalCharge.Clone(),backgroundTotalCharge.Clone(),combiTotalCharge.Clone(),i)
    totalChiSquared+=calculateChiSquared(simuSize.Clone(),signalSize.Clone(),backgroundSize.Clone(),combiSize.Clone(),i)
    totalChiSquared+=calculateChiSquared(simuTotalCharge.Clone(),signalTotalCharge.Clone(),backgroundTotalCharge.Clone(),combiTotalCharge.Clone(),i)
    totalChiSquared+=calculateChiSquared(simuProng.Clone(),signalProng.Clone(),backgroundProng.Clone(),combiProng.Clone(),i)
    x.append(i)
    y.append(totalChiSquared)
    if minimum>totalChiSquared:
        minimum=totalChiSquared
        p=i

print "forste",p
print "tagged",tagged
        
# p5=0
# for i in np.arange(0,1,0.01):
#     totalChiSquared=calculateChiSquared(simuPixel,signalPixel,backgroundPixel,i)
#     if minimum>totalChiSquared:
#         minimum=totalChiSquared
#         p5=i
print "from all",p
print "size",p1
print "prong",p2
print "center",p3
print "total",p4

p= (p1+p2+p3+p4)/4.0
print "combined",p
makeCombinedPlot(simuEnergy,signalEnergy,backgroundEnergy,combiEnergy,1,True,"centerEnergy","keV",2,p)
makeCombinedPlot(simuProng,signalProng,backgroundProng,combiProng,1,True,"prongs","# prongs",5,p)
makeCombinedPlot(simuSize,signalSize,backgroundSize,combiSize,1,True,"size","# pixels",2,p)
makeCombinedPlot(simuTotalCharge,signalTotalCharge,backgroundTotalCharge,combiTotalCharge,1,True,"charge","keV",2,p)


p=0
minimum=100000000000
y=[]
x=[]
for i in np.arange(0,1,0.01):
    totalChiSquared=calculateChiSquared(simuTotalChargeTagged.Clone(),signalTotalChargeTagged.Clone(),backgroundTotalChargeTagged.Clone(),combiTotalChargeTagged.Clone(),i)
    totalChiSquared+=calculateChiSquared(simuSizeTagged.Clone(),signalSizeTagged.Clone(),backgroundSizeTagged.Clone(),combiSizeTagged.Clone(),i)
    totalChiSquared+=calculateChiSquared(simuTotalChargeTagged.Clone(),signalTotalChargeTagged.Clone(),backgroundTotalChargeTagged.Clone(),combiTotalChargeTagged.Clone(),i)
    totalChiSquared+=calculateChiSquared(simuProngTagged.Clone(),signalProngTagged.Clone(),backgroundProngTagged.Clone(),combiProngTagged.Clone(),i)
    x.append(i)
    y.append(totalChiSquared)
    if minimum>totalChiSquared:
        minimum=totalChiSquared
        p=i

print "minimum p",p

ptagged=p*1.0*taggedBackground/(totalBackground)
makeCombinedPlot(simuEnergyTagged,signalEnergyTagged,backgroundEnergyTagged,combiEnergyTagged,1,True,"centerEnergyTagged","keV",10,ptagged)
makeCombinedPlot(simuProngTagged,signalProngTagged,backgroundProngTagged,combiProngTagged,1,True,"prongsTagged","# prongs",30,ptagged)
makeCombinedPlot(simuSizeTagged,signalSizeTagged,backgroundSizeTagged,combiSizeTagged,1,True,"sizeTagged","# pixels",10,ptagged)
makeCombinedPlot(simuTotalChargeTagged,signalTotalChargeTagged,backgroundTotalChargeTagged,combiTotalChargeTagged,1,True,"chargeTagged","keV",10,ptagged)
#plt.plot(x,y)
#plt.show()
