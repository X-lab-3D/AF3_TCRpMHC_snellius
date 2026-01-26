# Activate the conda environment if needed
# source activate alphafold3

# Submit AF3 inference jobs
python preprocess_and_run.py --mode run_inference \
    --input-csv /home/marzellad/AF3_snellius/test/test.csv \
    --output-dir /home/marzellad/AF3_snellius/test/AF3_jsons/ \
