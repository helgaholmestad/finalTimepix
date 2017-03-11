#!/usr/bin/env bash

function run {
    python GaussianBlurTCAD.py ../runningFLUKA/supersimpelTimepixCenter$1_fort.22 $2 &
}

run 001 1
run 002 2
run 003 3
run 004 4
run 005 5
run 006 6
run 007 7
run 008 8
run 009 9
run 010 10
