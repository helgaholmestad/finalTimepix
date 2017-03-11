from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile
gROOT.Reset()
import numpy as np
import sys
print sys.argv
import os
import os.path
import re
import hough1D
pixelList=[]
distanceT=20.
distanceR=6.1

#rootdir="/home/helga/timepixForwardFull/20160508_Al52_0kV-3kV-4kV-3kV"
#rootdir="/home/helga/testbeamNewCleaning/sortedData/"
#rootdir='/home/helga/backgroundData2015'
rootdir="/home/helga/inputfiles/scanReversedDetector"
#clustering algorithm here


def findPurity(pattern):
    pattern=str(pattern)
    if os.path.isfile(str("reversedDatafiles/"+pattern+"sumOfSquares.txt")):
        os.remove(str("reversedDatafiles/"+pattern+"sumOfSquares.txt"))
    if os.path.isfile(str("reversedDatafiles/"+pattern+"meta.txt")):
        os.remove(str("reversedDatafiles/"+pattern+"meta.txt"))
    if os.path.isfile(str("reversedDatafiles/"+pattern+"taggedClusters.txt")):
        os.remove(str("reversedDatafiles/"+pattern+"taggedClusters.txt"))
    if os.path.isfile(str("reversedDatafiles/"+pattern+"prongs.txt")):
        os.remove(str("reversedDatafiles/"+pattern+"prongs.txt"))
    
    counter=0
    for subdir, dirs, files in os.walk(rootdir):
        if not pattern in subdir:
            continue
        for file in files:
            if os.path.isfile(subdir+"/"+file) and "histograms" in file and ".root" in file and "test27" in subdir and not "~" in file:
                hough1D.hough(str(subdir+"/"+file),pattern,"reversedDatafiles")

findPurity(sys.argv[1])
