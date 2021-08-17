#!/bin/bash
mkdir -m 755 cpu
for job_file in $(ls *.fio)
do
      fio ${job_file} --output ${job_file}.txt & mpstat -P ALL 5 20 > cpu/${job_file}CPU.txt
      wait
    
done
