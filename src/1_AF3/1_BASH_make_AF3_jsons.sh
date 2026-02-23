# Activate the conda environment if needed
# source activate alphafold3

# Generate AlphaFold3 JSON input files
python preprocess_and_run.py --mode make_json \
    --input-csv /home/marzellad/AF3_TCRpMHC_snellius/test/test.csv \
    --output-dir /projects/0/prjs1135/AF3_TCR_pipeline_test/AF3_jsons/ \
    --num-seeds 5 \
    --ID-column PDBID \
    --chainID-columns A B #M N P #Column ID has to be pdb-standard, one-letter uppercase
