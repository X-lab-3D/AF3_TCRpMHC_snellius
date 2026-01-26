# Activate the conda environment if needed
# source activate alphafold3

# Generate AlphaFold3 JSON input files
python preprocess_and_run.py --mode make_json \
    --input-csv /home/marzellad/AF3_snellius/test/test.csv \
    --output-dir /home/marzellad/AF3_snellius/test/AF3_jsons/ \
    --num-seeds 2 \
    --ID-column PDBID \
    --chainID-columns TCRa TCRb #MHCa MHCb Peptide
