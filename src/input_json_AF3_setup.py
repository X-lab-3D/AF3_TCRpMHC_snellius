import os
import json
import pandas as pd
import numpy as np
from numpy import random

"""
Convert protein sequences (TCRs, pMHCs, or full TCR–pMHC complexes) into AF3-compatible JSON input files.

input:  a csv file containing the sequences and pdbid (var=input_file), a output directory.

Assumptions:    The column names of the csv are TCRa, TCRb.
                Current code runs on random seed settings to generate 5 TCR json files.
                The chain IDs are hardcoded and vary per function (TCRpMHC follows swifttcr standards).


"""

def add_protein_chain(seq, chain_id):
    """
    Inputs :
    seq : str
        One letter amino acid sequence of the protein chain.
    chain_id : str
        Single-character chain identifier used by AlphaFold3.

    Output: Dictionary formatted for AlphaFold3 JSON input containing the
        protein chain ID and amino acid sequence.
    """
    return {
        "protein": {
            "id": chain_id,
            "sequence": seq,
        }
    }

def generate_json_AF3_for_tcr(seq_tcra,seq_tcrb,ID,output_dir,seednumber=1):
    """
    Inputs:
    seq_tcra : str
        One letter amino acid sequence of the TCR alpha chain.
    seq_tcrb : str
        One letter amino acid sequence of the TCR beta chain.
    ID : str
        Unique identifier used as the AlphaFold3 job name and JSON filename.
    output_dir : str
        Directory path where the AlphaFold3 input JSON file is written.
    seednumber : int or None, optional
        Random seed for AlphaFold3 inference. If a numeric value is provided,
        it is used directly. If None, a random seed is generated (range = 1 - 10000).

    Output:
    Writes a single AlphaFold3-compatible JSON file to disk containing
    two protein chains (A: TCR alpha, B: TCR beta).

    """
    #template for Alphafold3 submission json file designed for AF3. 
    if isinstance(seednumber, (int, float)):
        af3_setup = {
            "name": ID,
            "modelSeeds": [seednumber],
            "sequences": [],
            "dialect": "alphafold3",  # Or "alphafold3" based on your need
            "version": 1
        }
    else:
        rng = np.random.default_rng()
        random_number = int(rng.integers(10000))
        af3_setup = {
            "name": ID,
            "modelSeeds": [random_number],
            "sequences": [],
            "dialect": "alphafold3",  # Or "alphafold3" based on your need
            "version": 1
        }

    af3_setup["sequences"].append(add_protein_chain(seq_tcra, "A"))
    af3_setup["sequences"].append(add_protein_chain(seq_tcrb, "B"))

    #generate unique json file
    filename = f"{ID}.json"
    output_path = os.path.join(output_dir,filename)

    with open(output_path, 'w') as f:
        f.write(json.dumps(af3_setup, indent=2))

def generate_json_AF3_for_pMHC(seq_mhca,seq_mhcb,seq_pep,ID,output_dir,seednumber=1):
    """
    Inputs:
    seq_mhca : str
        One letter amino acid sequence of the MHC alpha chain.
    seq_mhcb : str
        One letter amino acid sequence of the MHC beta chain.
    seq_pep : str
        One letter amino acid sequence of the peptide chain.
    ID : str
        Unique identifier used as the AlphaFold3 job name and JSON filename.
    output_dir : str
        Directory path where the AlphaFold3 input JSON file is written.
    seednumber : int or None, optional
        Random seed for AlphaFold3 inference. If a numeric value is provided,
        it is used directly. If None, a random seed is generated (range = 1 - 10000).

    Output:
    Writes a single AlphaFold3-compatible JSON file to disk containing
    two protein chains (A: TCR alpha, B: TCR beta).

    """

    if isinstance(seednumber, (int, float)):
        af3_setup = {
            "name": ID,
            "modelSeeds": [seednumber],
            "sequences": [],
            "dialect": "alphafold3",  # Or "alphafold3" based on your need
            "version": 1
        }
        rng = np.random.default_rng()
        random_number = int(rng.integers(10000))
        af3_setup = {
            "name": ID,
            "modelSeeds": [random_number],
            "sequences": [],
            "dialect": "alphafold3",  # Or "alphafold3" based on your need
            "version": 1
        }

    # checks if the MHC beta sequence is a string
    if isinstance(seq_mhcb, str):
        af3_setup["sequences"].append(add_protein_chain(seq_mhca, "M"))
        af3_setup["sequences"].append(add_protein_chain(seq_mhcb, "N"))
        af3_setup["sequences"].append(add_protein_chain(seq_pep, "P"))

    elif not isinstance(seq_mhcb, str):
        af3_setup["sequences"].append(add_protein_chain(seq_mhca, "M"))
        af3_setup["sequences"].append(add_protein_chain(seq_pep, "P"))


    #generate unique json file
    filename = f"{ID}.json"
    output_path = os.path.join(output_dir,filename)

    with open(output_path, 'w') as f:
        f.write(json.dumps(af3_setup, indent=2))

def generate_json_AF3_for_TCRpMHC(seq_tcra,seq_tcrb,seq_mhca,seq_mhcb,seq_pep,ID,output_dir,seednumber=1):

    #template for Alphafold3 submission json file designed for AF3. 
    if isinstance(seednumber, (int, float)):
        initial = [{'name': '', 'modelSeeds': [seednumber], 'sequences': [], 'dialect': 'alphafold3', 'version': 1}]
    else:
        rng = np.random.default_rng()
        random_number = int(rng.integers(10000))
        initial = [{'name': '', 'modelSeeds': [random_number], 'sequences': [], 'dialect': 'alphafold3', 'version': 1}]

    input_seq_a = {'protein': {"id": "D",'sequence': '', 'count': 1}}
    input_seq_b = {'protein': {"id": "E",'sequence': '', 'count': 1}}
    input_seq_ma = {'protein': {"id": "A",'sequence': '', 'count': 1}}
    input_seq_mb = {'protein': {"id": "B",'sequence': '', 'count': 1}}
    input_seq_p = {'protein': {"id": "C",'sequence': '', 'count': 1}}

    #fill in the template structure for AF3
    input_seq_a['protein']['sequence'] = seq_tcra
    input_seq_b['protein']['sequence'] = seq_tcrb
    input_seq_ma['protein']['sequence'] = seq_mhca
    input_seq_mb['protein']['sequence'] = seq_mhcb
    input_seq_p['protein']['sequence'] = seq_pep

    #append to the initial setup file
    initial[0]["sequences"].append(input_seq_a)
    initial[0]["sequences"].append(input_seq_b)
    initial[0]["sequences"].append(input_seq_ma)
    initial[0]["sequences"].append(input_seq_mb)
    initial[0]["sequences"].append(input_seq_p)
    initial[0]["name"] = ID

    #generate unique json file
    filename = f"{ID}.json"
    output_path = os.path.join(output_dir,filename)

    with open(output_path, 'w') as f:
        json.dump(initial, f)

if __name__ == "__main__":
    #main data
    input_file = "/projects/0/prjs1135/TCR_assembly_benchmark/1_data/sequences_benchmark_final.csv"
    df = pd.read_csv(input_file)

    #output directory
    output_dir = "/projects/0/prjs1135/TCR_assembly_benchmark/3_docking_runs/input_AF3/TCR"

    #save the unique TCRs and pMHC
    #unique_pMHC = {}
    unique_TCR = {}

    #Find all unique TCR sequences in the data (and pMHC can be done)
    for case in df.iloc():
        unique_TCR[case.PDBID] = {"TCRa":case.TCRa, "TCRb":case.TCRb}
        #unique_pMHC[split_ID[1]] = {"MHC":case.MHC, "MHC_b":case.MHC_b, "pep":case.peptide}

    #generate the TCR AF3 submission files
    for i in range(5):
        for key in unique_TCR:
            generate_json_AF3_for_tcr(unique_TCR[key]["TCRa"], unique_TCR[key]["TCRb"],f"{key}_rs{i}",output_dir, seednumber=None)
