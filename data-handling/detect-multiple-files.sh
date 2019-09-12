#! /bin/bash

FILES=/home/nsbruce/Documents/RFI/460DATA/*

for f in $FILES
do
    echo "Processing $f"
    python SearchFile.py $f
done