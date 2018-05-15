N=0
N_t=0
B=0
B_t=0
prong=0
e=0
size=0

for line in open("datafiles/meta.txt",'r'):
    c=line.split()
    if line.rstrip()=="newCluster":
        N+=1
        if size>69 and prong>0 and e >0.99:
            N_t+=1
    if c[0]=="prong":
        prong=float(c[1])
    if c[0]=="pixels":
        size=float(c[1])
    if c[0]=="error":
        e=float(c[1])



for line in open("reversedDatafiles/meta.txt",'r'):
    c=line.split()
    if line.rstrip()=="newCluster":
        B+=1
        if size> 69 and prong>0 and e >0.99:
            B_t+=1
    if c[0]=="prong":
        prong=float(c[1])
    if c[0]=="pixels":
        size=float(c[1])
    if c[0]=="error":
        e=float(c[1])

        



print N,N_t,B,B_t
