#!/bin/bash
#SBATCH --job-name=ensemble
#SBATCH --nodes=1
#SBATCH --cpus-per-task 16
#SBATCH --partition=rome
#SBATCH --time=01:00:00

"""
This script is used to calculate the RMSD values with ProFit version 3.3

Input:
    input_dir = folder containing the scripts and multifiles for profit
    output_dir = output directory of the rmsd outputs
    profit_bin = a path to the profit bin using profit version 3.3 (http://www.bioinf.org.uk/software/profit/)

Assumption: The .txt files in the directory are ProFit scripts

Output:
    The output is a text file containing the log of ProFit, with the rmsd calculations
"""

INPUT_DIR=$1
#"/projects/0/prjs1135/SwiftTCR/Alphafold/ensemble/scripts/clustering"
OUTPUT_DIR=$2
#"/projects/0/prjs1135/SwiftTCR/Alphafold/ensemble/processed_tcrs/rmsd"
PROFIT_BIN=$3
#"/home/ddiepenbroek/ProFitV3.3/bin"

mkdir -p "$OUTPUT_DIR"

cd "$PROFIT_BIN" || exit 1

for input_script in "$INPUT_DIR"/*.txt; do
    [ -e "$input_script" ] || continue

    base_name=$(basename "$input_script" .txt)

    # Remove 'calc' from the filename
    clean_name="${base_name//calc/}"

    ./profit < "$input_script" > "${OUTPUT_DIR}/${clean_name}_final.txt" #saves the log of ProFit
    echo "The file is saved at ${OUTPUT_DIR}/${clean_name}_final.txt" 
done


