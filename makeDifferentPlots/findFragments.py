from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile,TStyle,TLegend,TPave,TPaveStats,TPad,TPaveLabel,gStyle,gPad,TPaletteAxis
gROOT.Reset()


proton =0
neutron=0
pionspluss=0
pionsminus=0
pionszero=0
alpha=0
helium3=0
triton=0
deteron=0
heavy=0
numberOfEvents=0
histogram=TH1D("multi","",7,0,7)

for line in open("../fragmentsStudy/exam2001.log"):
#for line in open("exam2001.log"):
    columns = line.split()
    if(len(columns)>0 and columns[0]=="oo"):
        if(int(columns[1])==13):
            histogram.Fill(0)
            print "pionpluss",columns[2]
            pionspluss+=1
        elif(int(columns[1])==14):
            histogram.Fill(0)
            print "pionminus",columns[2]
            pionsminus+=1
        elif(int(columns[1])==23):
            print "pionzero",columns[2]
            pionszero+=1
        elif(int(columns[1])==1):
            histogram.Fill(1)
            proton+=1
            print "proton",columns[2]
        elif(int(columns[1])==8):
            neutron+=1
            print "neutron",columns[2]
    
    elif(len(columns)>0 and columns[0]=="-h-"):
        if(int(columns[1])==7):
            heavy+=1
            histogram.Fill(6)
            print "ion",columns[2]
        if(int(columns[1])==6):
            alpha+=1
            histogram.Fill(5)
            print "alpha",columns[2]
        if(int(columns[1])==5):
            histogram.Fill(3)
            helium3+=1
            print "helium",columns[2]
        if(int(columns[1])==4):
            histogram.Fill(4)
            triton+=1
            print "triton",columns[2]
        if(int(columns[1])==3):
            histogram.Fill(2)
            deteron+=1
            print "deteron",columns[2]


histogram.GetXaxis().SetBinLabel(1,"pions")

histogram.GetXaxis().SetBinLabel(2,"proton")

histogram.GetXaxis().SetBinLabel(3,"deuteron")

histogram.GetXaxis().SetBinLabel(4,"triton")

histogram.GetXaxis().SetBinLabel(5,"helium-3")

histogram.GetXaxis().SetBinLabel(6,"alpha")

histogram.GetXaxis().SetBinLabel(7,"heavier ")
histogram.GetYaxis().SetTitleSize(0.05)

histogram.GetXaxis().SetLabelSize(0.045)
histogram.GetYaxis().SetLabelSize(0.045)



histogram.Scale(1.0/100)

histogram.GetYaxis().SetTitle("Average multiplicity")

#histogram.GetYaxis().SetTitleOffset(0.6)

#histogram.GetYaxis().SetLabelSize(0.055)

histogram.GetXaxis().SetLabelSize(0.08)


can =TCanvas()
can.SetLeftMargin(0.1)
histogram.GetYaxis().SetTitleOffset(0.7)
gStyle.SetOptStat("");
histogram.Draw("hist")
can.Print("../../../fig/multiplicity.pdf")

print "proton", proton
print "alpha", alpha
print "helium3", helium3
print "triton",triton
print "deteron",deteron
print "heavy ", heavy

