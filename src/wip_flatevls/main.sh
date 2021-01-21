#!/bin/bash

for qc in 0.7
do    
    for delta in 0.05 0.1 0.2 0.5 
    do
        for eps in 0.1 0.05 0.02
        do
            for p in 3 4 5 
            do
                python3 /home/s1992054/qmd/src/wip_flatevls/run.py $eps $p $qc $delta 
            done
        done
    done
done
