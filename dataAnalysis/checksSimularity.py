import sys
def isSimular(test,number):
    lineNumber=0
    for line in open(sys.argv[1]):
        if test==line and lineNumber!=number:
            print "fant likt",test
        lineNumber+=1

lineNumber=0
for line in open(sys.argv[1]):
    isSimular(line,lineNumber)
    lineNumber+=1
