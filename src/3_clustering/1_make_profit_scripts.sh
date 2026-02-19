# !/bin/bash

# use --input-dir, --output-dir and --output-dir-multi to specify the directories for the input pdbs, output scripts and output multi files respectively.

bash make_script_profit.py --input-dir /projects/0/prjs1135/SwiftTCR/Alphafold/ensemble/processed_tcrs/renumbered \
    --output-dir /projects/0/prjs1135/SwiftTCR/Alphafold/ensemble/scripts/clustering \
    --output-dir-multi /projects/0/prjs1135/SwiftTCR/Alphafold/ensemble/scripts/clustering/profit_input
