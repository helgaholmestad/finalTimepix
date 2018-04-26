N=0
N_t=0
B=0
B_t=0

for line in open("datafiles/meta.txt",'r'):
    if line.rstrip()=="newCluster":
        N+=1
    if line.rstrip()=="trough":
        N_t+=1

for line in open("reversedDatafiles/meta.txt",'r'):
    if line.rstrip()=="newCluster":
        B+=1
    if line.rstrip()=="trough":
        B_t+=1


print N,N_t,B,B_t
