#!/usr/bin/env bash

function run {
    python hough1D.py datafilesJustVolcano/histograms$1TCADjustVolcano.root datafilesJustVolcano/meta$2.txt datafilesJustVolcano/prong$2.txt &
}

run 1 1
run 2 2
run 3 3
run 4 4
run 5 5
run 6 6
run 7 7
run 8 8
run 9 9
run 10 10