#!/usr/bin/env bash

cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null
ls
for i in $(seq 21 30);
do
    python classification.py data/all_africa.xlsx $i 10
done