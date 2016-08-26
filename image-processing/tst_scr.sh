#!/bin/bash

for filename in test_images/*; 
do "python3 recognize.py -i ${filename} -p"; 
done
