#!/bin/bash
python_file="A.py"
output_file="A.out"
python3 "$python_file"
rm "$output_file"
python3 "$python_file" > "$output_file"