#!/bin/bash
for delta in 'seq 0.01 0.1 0.5'
do
    for alpha in 'seq 1 3.14 0.2' 
    do
        for eps in 0.1 0.05
        do
            for p in 3 4 5 
            do
                python3 /home/s1992054/QMD/src/wip_flatevls/run.py $delta $alpha $eps $p & 
            done
        done
    done
done
