from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile,gStyle,gPad
gROOT.Reset()
distanceR=4.1
import numpy
import random
import os
import sys
random.seed(3)


histoRaw=TH1D("","",500,0,5000)
def makeDeadList(i):
    listOfDeadPixels=[]
    inputfile="/home/helga/newTimepixFiles/20160528_33umAl_D1_0kV_D2_4kV_E1_4kV_E2_3kV_leadblocks/00_20160528_162324/test27_datadriven_AD/"
    inputfile="/home/helga/TimepixArticle/data/newTimepixFiles/20160528_33umAl_D1_0kV_D2_4kV_E1_4kV_E2_3kV_leadblocks/00_20160528_162324/test27_datadriven_AD/"
   
    while os.stat(inputfile+"clustering"+str(i)+".dat").st_size==0:
        print "we are in a while loop"
        i=random.randint(1,25)
        print "random number",i
    infile= open(inputfile+"clustering"+str(i)+".dat",'r')
    firstLine=infile.readline()
    modeTime=float(firstLine.split()[2])
    for line in open(inputfile+"data_"+str(i)+".dat",'r'):
        columns=line.split()
        time=1900
        #time=random.gauss(1800,250)
        #if float(columns[5])<modeTime+2000 and float(columns[5])>modeTime+500:
        if float(columns[5])<modeTime+time and float(columns[5])>modeTime-550+time:
            deadPixel=[int(columns[0]),int(columns[1])]
            listOfDeadPixels.append(deadPixel)
    return listOfDeadPixels

file=open("datafiles/"+sys.argv[1]+"newresults.txt","w")
def reCluster(pixelsInCluster):
    tmpPixel=pixelsInCluster[0]
    lookForNext=[]
    def findNeigbours(tmpPixel):
        lookForNext=[]
        for i in pixelsInCluster:
            if numpy.sqrt(abs(i[1]-tmpPixel[1])*abs(i[1]-tmpPixel[1])+abs(i[0]-tmpPixel[0])*abs(i[0]-tmpPixel[0]))<distanceR:
                if i[2]<500:
                    toWrite=str(str(i[0])+" "+str(i[1])+"  "+str(i[2])+"\n")
                else:
                    randomEnergy=random.gauss(500,50)
                    toWrite=str(str(i[0])+" "+str(i[1])+"  "+str(randomEnergy)+"\n")
                    #toWrite=str(str(i[0])+" "+str(i[1])+"  "+str("hoy\n"))
                #if i[2]>6:# and i[2]<670:
                file.write(toWrite)
                pixelsInCluster.remove(i)
                lookForNext.append(i)
        return lookForNext
    def findCluster():
        file.write("cluster"+"\n")
        tmpPixel=[]
        tmpPixel.append(pixelsInCluster[0])
        while True:
            tmp=findNeigbours(tmpPixel[0])
            tmpPixel.extend(tmp)
            tmpPixel.remove(tmpPixel[0])
            if len(tmpPixel)==0:
                break
    while True:
        findCluster()
        if len(pixelsInCluster)==0:
            break

listOfDeadPixels=[]
newCluster=[]
event=0
for line in open("datafiles/"+sys.argv[1]+"results.txt","r"):
    columns=line.split()
    if event>1001:
        continue
    if columns[0]=="new":
        file.write("event\n")
        event+=1
        print "new"
        while True:
            print "in while"
            ranNumb=random.randint(1,25)
            print "find random",ranNumb
            listOfDeadPixels=makeDeadList(ranNumb)
            if len(listOfDeadPixels)>1000:
                break
        if len(newCluster)!=0:
            reCluster(newCluster)
            newCluster=[]
    else:
        histoRaw.Fill(float(columns[2]))
        pixel=[int(columns[0]),int(columns[1])]
        #use this if sentence to remove dead pixel
        if pixel not in listOfDeadPixels:
            newCluster.append([int(columns[0]),int(columns[1]),float(columns[2])])
    
file.close()

myFile=TFile("datafiles/histograms"+sys.argv[1]+"TCADFinal.root","RECREATE")
finalWithCut=TH2D("event0","event0",256,0,256,256,0,256)
teller=0
cluster=0
for line in open("datafiles/"+sys.argv[1]+"newresults.txt","r"):
    columns=line.split()
    if columns[0]=="event":
        teller+=1
        cluster=0
        print "event",teller
    elif columns[0]=="cluster":
        cluster+=1
        if finalWithCut.GetEntries()>10:
            finalWithCut.Write()
        name="event"+str(teller)+"cluster"+str(cluster)
        finalWithCut=TH2D(name,name,256,0,256,256,0,256)
    else:
        finalWithCut.Fill(int(columns[0]),int(columns[1]),float(columns[2]))
myFile.Write()

print event

# canvas=TCanvas()
# histoRaw.GetXaxis().SetTitle("energy deposited in pixel [keV]")
# histoRaw.GetYaxis().SetTitle("frequenzy")
# histoRaw.Draw()
# gPad.SetLogy()
# canvas.Print("/home/helga/testbeamNewCleaning/fig/rawEnergy.pdf")



