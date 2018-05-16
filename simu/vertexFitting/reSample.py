import numpy as np
data=[]
for line in open("toResample.tex","r"):
    data.append(float(line.strip()))
data=np.array(data)
data = data[np.isfinite(data)]
l=len(data)

result=[]

for i in range(1000):
    sample=np.random.choice(data,l)
    sample.sort()
    #print sample
    #break
    result.append(sample[int(l*0.68)])

result=np.array(result)

print np.std(result)
