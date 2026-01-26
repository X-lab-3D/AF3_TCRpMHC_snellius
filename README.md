# Ensemble Models

This folder contains all the scripts and documents used to generate and process 
the Alphafold3 models related to the ensemble approach. Detailed information about 
the functions are added in the scripts.

## Contents
- Alphafold3 run on snellius:
    - **input_json_AF3_setup.py**: generates the Alphafold3 input json files for TCR with a random seed between 1-10000. 
                                    input is a .csv file
        - path: ./pre-processing
        - output results: ./input_af3
    - **data_process_tcr_run*.sh**: performs Alphafold3 dataprocessing (MSAs and template search) step.
        - path: ./job
        - output results: The defined output directory
    - **inf_a100_tcr.sh**: performs Alphafold3 inference step with the dataprocessing input files
        - path: ./job
- Post-processing: 
    - **copy_and_name_models_af3.py**: copies tcr model from each folder and rename based on folder + model ID (before: model.cif)
        - path: ./processing
    - **tcr_af3_to_pdb_renumb.py**: converts .cif tcr files into IMGT renumbered .pdb files
        - path: ./processing
- clustering TCRs:
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
    - **copy_centermodels.py**: script to copy the center models stated in the clustering text file with a new name (PDBID_c*.pdb) into a different directory
        - .clustering



TODO: data_process_tcr_run make so 1 run = 1 case. remove multiple files, loop over 1 passing argument to submit.