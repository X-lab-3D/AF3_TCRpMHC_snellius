# !/bin/bash

# use --input-dir, --output-dir and --output-dir-multi to specify the directories for the input pdbs, output scripts and output multi files respectively.

python make_profit_script.py --input-dir /projects/0/prjs1135/AF3_TCR_pipeline_test/processed_tcrs/renumbered \
    --output-dir /projects/0/prjs1135/AF3_TCR_pipeline_test/clustering \
    --output-dir-multi /projects/0/prjs1135/AF3_TCR_pipeline_test/clustering/profit_input
