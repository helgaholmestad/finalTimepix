#!/usr/bin/python
import fileinput
import sys
from math import sqrt,fabs,pi
from random import random,gauss


### ---- deflection for charge when travelling 500 um
###      lets think it's  .2 of the pixel width
dc= .01*.0055


# -------------------------------------------------------------------------------
###       1635 1485    0     5.3
# ---

outfile=open("truthValues.txt","w")
foundFirst=False
#inputfile = 'exam2001.log'
variables=[] 
global eventNumber
eventNumber=0

def readOneFile(file):
    global eventNumber
    foundFirst=False
    variables=[]
    print file
    for L in open(file,"r"):
        print L
        l=  L.strip().split()
        if L.startswith(' --t--'):
            if l[1]=="begin":
                foundFirst=False
                continue
            if l[1]=='new':
                if(len(variables) ==0):
                    continue
                if variables[0]==2.0 and foundFirst==False:
                    print "depth",(1.0-variables[6])*10000
                    print variables
                    #outfile.write(str(eventNumber)+" "+str(variables[1])+"  "+str(variables[3])+ "\n")
                    outfile.write(str(eventNumber)+" "+str((variables[3]+0.704)/1.408*256+0.5)+"  "+str((variables[1]+0.704)/1.408*256+0.5)+ "\n")
                    foundFirst=True
                    eventNumber+=1
                    print "her"
                variables=[]
            else:
                for i in range(1,len(l)):
                    variables.append(float(l[i]))


for  i in ["010","001","002","003","004","005","006","007","008","009"]:
    readOneFile(str("supersimpelTimepixCenter"+i+".log"))
    
#readOneFile(str("supersimpelTimepixCenter001.log"))
                    

# for L in fileinput.input():
#     l=  L.strip().split()
#     if L.startswith(' --t--'):
#         if l[1]=="begin":
#             foundFirst=False
#             continue
#         if l[1]=='new':
#             if(len(variables) ==0):
#                 continue
#             if variables[0]==2.0:# and foundFirst==False:
#                 print "depth",(1.0-variables[6])*10000
#                 print variables
#                 outfile.write(str(eventNumber)+" "+str(variables[1])+"  "+str(variables[3])+ "\n")
#                 #outfile.write(str(eventNumber)+" "+str((variables[1]+0.704)/1.408*256)+"  "+str((variables[3]+0.704)/1.408*256)+ "\n")
#                 foundFirst=True
#                 eventNumber+=1
#                 print "her"
#             variables=[]
#         else:
#             for i in range(1,len(l)):
#                 variables.append(float(l[i]))
          
