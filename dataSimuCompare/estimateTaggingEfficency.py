import sys

f=float(sys.argv[1])
print f

N=63890.0
N_t=5771

#tu=N_t-N*f*0.0114
tu=N_t-N*f*0.0057
tl=N-f*N

t=tu/tl

print "tagging efficency",t

