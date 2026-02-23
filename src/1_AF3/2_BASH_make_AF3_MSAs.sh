# Activate the conda environment if needed
# source activate alphafold3

# Submit MSA generation jobs
python preprocess_and_run.py --mode run_MSA \
    --input-csv /home/marzellad/AF3_TCRpMHC_snellius/test/test.csv \
    --output-dir /projects/0/prjs1135/AF3_TCR_pipeline_test/AF3_jsons/ \
    --tcrpmhc-specific
