#!/usr/bin/env bash

cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null
ls
for i in $(seq 81 90);
do
    python classification.py data/all_africa.xlsx $i 10
done