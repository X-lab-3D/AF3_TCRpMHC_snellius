# Ensemble Models

This folder contains all the scripts and documents used to generate and process 
the Alphafold3 models related to the ensemble approach.

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
        - path: 
- clustering TCRs:
    - ** **: 
