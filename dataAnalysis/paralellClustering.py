from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile
gROOT.Reset()
import numpy
import sys
import os
import pp
import time

rootdir="../../../data"
def processFile(filename,outputfile):
    from ROOT import TH1D
    pixelList=[]
    distanceT=20.
    distanceR=4.1
    file=open(outputfile,'w')
    print("working with file",filename)
    def findNeigbours(tmpPixel):
        lookForNext=[]
        for i in pixelListSorted:
            if numpy.sqrt(abs(i[1]-tmpPixel[1])*abs(i[1]-tmpPixel[1])+abs(i[0]-tmpPixel[0])*abs(i[0]-tmpPixel[0]))<distanceR:
                if abs(i[3]-tmpPixel[3])<distanceT:
#                    print "hva er verdiene", np.sqrt(abs(i[1]-tmpPixel[1])*abs(i[1]-tmpPixel[1])+abs(i[0]-tmpPixel[0])*abs(i[0]-tmpPixel[0])),distanceR
                    toWrite=str(str(i[0])+" "+str(i[1])+"  "+str(i[2])+"  "+str(i[3])+"\n")
                    file.write(toWrite)
                    pixelListSorted.remove(i)
                    lookForNext.append(i)
                elif i[3]-tmpPixel[3]>distanceT:
                    break
        return lookForNext
    def findCluster(time):
        file.write("new cluster "+str(time)+"\n")
        tmpPixel=[]
        tmpPixel.append(pixelListSorted[0])
        while True:
            tmp=findNeigbours(tmpPixel[0])
            tmpPixel.extend(tmp)
            tmpPixel.remove(tmpPixel[0])
            if len(tmpPixel)==0:
                break
    l=0
    tempHist=TH1D("temp","temp",40000,0,400000)
    tempHit=[4]
    timeSort=[]
    pixelList=[]
    for line in open(filename):
        columns = line.split()
        if columns[0]=="pix_col" or len(columns)<6:
            continue
        elif float(columns[4])>5.0:
            tempHit=[int(columns[0]),int(columns[1]),float(columns[4]),float(columns[5])]
            pixelList.append(tempHit)
            tempHist.Fill(float(columns[5]))
            timeSort.append(float(columns[5]))
    numpy.asarray(timeSort)
    modeTime=tempHist.GetBinCenter(tempHist.GetMaximumBin())
    print("mode time",modeTime)
    print(len(pixelList))
    indexSort=numpy.argsort(timeSort)
    pixelListSorted=[]
    for i in indexSort:
        if pixelList[i][3]>modeTime+600  and pixelList[i][3]<modeTime+3000:
            l=l+1
            pixelListSorted.append(pixelList[i])
    numberOfPixels=len(pixelListSorted)
    while True:
        #print len(pixelListSorted)
        if numberOfPixels-len(pixelListSorted)>l-2:
            break
        findCluster(modeTime)
        #print len(pixelListSorted)


#clustering algorithm here
def doClustering(filepath):
    output=filepath.replace("data_","clustering")
    processFile(filepath,output)
#doClustering("/home/helga/testbeamNewCleaning/sortedData/46um/bending6000/20151003_46umDeg_all3000V/00_20151003_171600/test27_datadriven_AD/data_1.dat")    

    
theFiles=[]
theDirectories=[]

for subdir, dirs, files in os.walk(rootdir):
    if "last" in subdir:
        continue
    #if not "20160511_33umAl_D1_0kV_D2_3kV_E1_3kV_E2_3kV_25mV" in subdir:
    #    continue
    for file in files:
        if "data_" in file:
            theDirectories.append(subdir)
            theFiles.append(subdir+"/"+file)
ppservers = ()

if len(sys.argv) > 1:
    ncpus = int(sys.argv[1])
    # Creates jobserver with ncpus workers
    job_server = pp.Server(ncpus, ppservers=ppservers)
else:
    # Creates jobserver with automatically detected number of workers
    job_server = pp.Server(ppservers=ppservers)

print("Starting pp with", job_server.get_ncpus(), "workers")

ppservers = ()

start_time = time.time()

jobs=[]

for k in range(len(theFiles)):
    jobs.append(job_server.submit(doClustering,(theFiles[k],),(processFile,),("numpy",)))

# #jobs = [(input, job_server.submit(sum_primes,(input,), (isprime,), ("math",))) for input in inputs]
teller=0
for job in jobs:
    print("teller ", teller)
    teller=teller+1
    print("er vi her")
    job()

print("Time elapsed: ", time.time() - start_time, "s")
job_server.print_stats()
