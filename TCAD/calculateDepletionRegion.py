from ROOT import gROOT, TCanvas, TH1D,TH2D,TFile
import scipy.integrate as noe
from scipy import exp
import os
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.optimize import curve_fit
import scipy
import math

D=300.0*math.pow(10,-6)
e_0=8.854*math.pow(10,-12)
e_si=11.7*e_0
N_d=pow(10,18)
e=1.602*pow(10,-19)
V=D*D*e*N_d/(2*e_si)
print V
