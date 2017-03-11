 #!/bin/bash
for i in `seq 1 10`;
do
    python hough1D.py datafilesOriginal/histogramsTCADRaw$i.root $i
done   
