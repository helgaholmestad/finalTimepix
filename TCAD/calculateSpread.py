import sys
import numpy as np
from math import exp
from math import sqrt

D=2*12.0*36.0/(12.0+36.0)
#D=12.0
D=D*10000.0*10000.0/1000000000.0
t=float(sys.argv[1])
r=sqrt(2*D*t)

print r
