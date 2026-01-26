# Activate the conda environment if needed
# source activate alphafold3

# Submit MSA generation jobs
python preprocess_and_run.py --mode run_MSA \
    --input-csv /home/marzellad/AF3_snellius/test/test.csv \
    --output-dir /home/marzellad/AF3_snellius/test/AF3_jsons/ \
