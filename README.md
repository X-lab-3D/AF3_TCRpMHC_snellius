# Ensemble Models

Pipeline including AlphaFold3 spedup version (using TCRmodel2 database) and ProFit rmsd calculation and clustering.

## Contents
- Alphafold3 run on snellius:
    -**./AF3**:</br>
        -**preprocess_and_run.py**: Module containing the functions to: Generate the AlphaFold3 JSON files, run the MSA and run the AF3 inference.</br>
            - mode: "make_json", "run_MSA", "run_inference" </br>
            - input: CSV with IDs and sequences of the cases to run </br>
            - output: depending on the mode, JSON files, MSAs and AF3 models.</br>
    -**./AF3/templates**:</br>
        - **template_data_process*.sh**: performs Alphafold3 dataprocessing (MSAs and template search) step.</br>
            - path: ./job </br>
            - output results: The defined output directory </br>
        - **template_inference_a100.sh**: performs Alphafold3 inference step with the dataprocessing input files </br>
            - path: ./job </br>

- Post-processing: 
    - **copy_and_name_models_af3.py**: copies tcr model from each folder and rename based on folder + model ID (before: model.cif)
        - path: ./processing
    - **tcr_af3_to_pdb_renumb.py**: converts .cif tcr files into IMGT renumbered .pdb files
        - path: ./processing

- clustering TCRs:
    !!! Assumes the structures are coherently (IMGT) numbered and needs a profit template with zones
    - **make_script_profit.py**: generates a ProFit script and a multi file for each unique pdb_id. (preperation RMSD calculations)
        - ./clustering
        - **calc_tcr_rmsd_{PDBID}.txt**: the generated ProFit scripts, used in run_rmsd_calc.sh
            - ./clustering
        - **multi_{PDBID}.txt**: a ProFits multi file contains all the paths for a specific PDB ID used in the ProFit scripts.
            - ./clustering/profit_input
    - **run_rmsd_calc.sh**: calculates the pairwise rmsd and saves the log of ProFit in a specified directory. 
        - ./clustering
    - **cluster_tcr_profit.py**: Uses the ProFit log files and Multifiles to cluster the TCRs and outputs a clustering text file.
        - ./clustering
    - **copy_centermodels.py**: script to copy the center models stated in the clustering text file with a new name (<PDBID>_c*.pdb) into a different directory
        - .clustering

```
# File with a list of paths to all the TCR pdb files to cluster (per case)
MULTI /projects/0/prjs1135/SwiftTCR/Alphafold/ensemble/scripts/clustering/profit_input/multi_7l1d.txt

# selects alignment atoms
ATOMS N,CA,C,O

# alignment zones with ANACRI/IMGT-numbered TCRs (both chains are included)
ZONE -26
ZONE 39-55
ZONE 66-104
ZONE 118-

# Calculate all vs all rmsd for all the chains in the models
ALLVSALL
```