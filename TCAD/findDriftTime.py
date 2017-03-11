from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile
gROOT.Reset()
import sys
import numpy as np
from math import exp
from math import sqrt

z=float(sys.argv[1])
w=675
#mobility of holes
m=450*10000.0*10000.0/1000000000.0
#h=12.0*10000.0*10000.0/1000000000.0
Vd=200
V=200

insideLnKyrre=(w*(Vd+V))/(2*Vd*z+w*(V-Vd))
insideLn=1.0-(z/w)*(2*Vd)/(V+Vd)

print insideLn
print insideLnKyrre
time=-(w*w/(2*m*Vd))*np.log(insideLn)
print time

D=12.0
D=D*10000.0*10000.0/1000000000.0
t=time
r=sqrt(2*D*t)
print r
