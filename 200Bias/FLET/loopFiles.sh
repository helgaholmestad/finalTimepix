#!/bin/bash 
listOfFiles=("sdevice02M.cmd" "sdevice03M.cmd" "sdevice04M.cmd" "sdevice05M.cmd" "sdevice06M.cmd" "sdevice07M.cmd" "sdevice08M.cmd" "sdevice09M.cmd" "sdevice1M.cmd")
for file in "${listOfFiles[@]}"   #  <-- Note: Added "" quotes.
do
    sdevice $file
done
