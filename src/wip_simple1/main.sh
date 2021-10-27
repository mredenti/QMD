#!/bin/bash

for delta in 0.05 0.1 0.2 0.5 
do
  for eps in $(seq 0.1 0.02 5)
  do
    for p in 1 1.5 2 2.5 3 3.5 4 4.5 5 5.5 6 
    do
      python3 ~QMD/src/wip_simple1/run.py $delta 0.5 $eps $p &  
    done
  done
done
