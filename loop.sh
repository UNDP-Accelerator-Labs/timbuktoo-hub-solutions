#!/usr/bin/env bash

cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null
# ls

# for i in $(seq 0 10);
# do
#     echo "$((i * 10))"
# done

for i in $(seq 0 9)
do
    for j in $(seq $((i * 10)) $(((i + 1) * 10 - 1)));
    do
        # python classification.py data/all_africa.xlsx $j 10
        python classification.py data/zmb_03.xlsx $j 10
    done
done  
