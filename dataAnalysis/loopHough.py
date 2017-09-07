from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile
#gROOT.Reset()
import numpy as np
import sys
print sys.argv
import os
import os.path
import re
#pixelList=[]
#distanceT=20.
#distanceR=6.1
#import subprocess
import hough1D

#rootdir="/home/helga/timepixForwardFull/20160508_Al52_0kV-3kV-4kV-3kV"
#rootdir="/home/helga/testbeamNewCleaning/sortedData/"
#rootdir='/home/helga/backgroundData2015'
rootdir='../../../data/newTimepixFiles'
#clustering algorithm here


def findPurity(pattern):
    print "Hei"
    pattern=str(pattern)
    if os.path.isfile(str("datafiles/"+pattern+"sumOfSquares.txt")):
        os.remove(str("datafiles/"+pattern+"sumOfSquares.txt"))
    if os.path.isfile(str("datafiles/"+pattern+"meta.txt")):
        os.remove(str("datafiles/"+pattern+"meta.txt"))
    if os.path.isfile(str("datafiles/"+pattern+"taggedClusters.txt")):
        os.remove(str("datafiles/"+pattern+"taggedClusters.txt"))
    if os.path.isfile(str("datafiles/"+pattern+"prongs.txt")):
        os.remove(str("datafiles/"+pattern+"prongs.txt"))    
    counter=0
    for subdir, dirs, files in os.walk(rootdir):
        if not pattern in subdir:
            continue
        for file in files:
            if os.path.isfile(subdir+"/"+file) and "histograms" in file and ".root" in file and "test27" in subdir and not "~" in file:
                print "er vi her"
                hough1D.hough(str(subdir+"/"+file),pattern,"datafiles")
         
print "HEI!!"
findPurity(sys.argv[1])

#findPurity("20160702_33umAl_D1_0kV_D2_3kV_E1_3kV_E2_3kV")
