import os
import json
import pandas as pd
import numpy as np
from numpy import random


def create_parser():
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate <-num-seeds> AlphaFold3 JSON input files for each case (row) in the input CSV file."
    )

    parser.add_argument(
        "--input-csv", "-i",
        type=str,
        required=True,
        help="CSV file containing the cases and their sequences.",
    )

    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        required=True,
        help="Directory to save the generated AlphaFold3 JSON input files.",
    )

    parser.add_argument(
        "--num-seeds", "-n",
        type=int,
        default=5,
        help="Number of different runs (each using a different random seed) for each input case (i.e. each CSV row)."
    )

    parser.add_argument(
        "--ID-column", "-d",
        type=str,
        default="TCRa",
        help="Column name for case ID in the CSV file."
    )

    parser.add_argument(
        "--chainID-columns", "-c",
        type=str,
        nargs='+',
        default=["TCRa", "TCRb"],
        help="Column name(s) for chain IDs in the CSV file. Can provide multiple column names.")

    return parser.parse_args()

def add_protein_chain(chain_id, seq):
    """
    Inputs :
        chain_id : str
            Single-character chain identifier used by AlphaFold3.
        seq : str
            One letter amino acid sequence of the protein chain.

    Output: Dictionary formatted for AlphaFold3 JSON input containing the
        protein chain ID and amino acid sequence.
    """
    return {
        "protein": {
            "id": chain_id,
            "sequence": seq,
        }
    }

def make_AF3_json(chains_dict, ID, output_dir, seednumber=None):
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
        Defaults to None.

    Output:
        Writes a single AlphaFold3-compatible JSON file to disk containing
        two protein chains (A: TCR alpha, B: TCR beta).

    """
    #If no seednumber is provided, generate a random one
    if not isinstance(seednumber, (int, float)):
        rng = np.random.default_rng()
        seednumber = int(rng.integers(10000))

    #Template for Alphafold3 submission json file designed for AF3.
    af3_setup = {
        "name": ID,
        "modelSeeds": [seednumber],
        "sequences": [],
        "dialect": "alphafold3",  # Or "alphafold3" based on your need
        "version": 1
    }

    #Add chain IDs and sequences to the json structure
    for chain_ID, seq in chains_dict.items():
        af3_setup["sequences"].append(add_protein_chain(chain_ID, seq))

    #generate unique json file
    filename = f"{ID}.json"
    output_path = os.path.join(output_dir,filename)

    with open(output_path, 'w') as f:
        f.write(json.dumps(af3_setup, indent=2))

if __name__ == "__main__":

    args = create_parser()
    #Load data
    df = pd.read_csv(args.input_csv)

    #Make output directory
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    #save the unique TCRs and pMHC
    #unique_pMHC = {}
    cases = {}

    #Find all unique TCR sequences in the data (and pMHC can be done)
    for case in df.iloc():
        cases[case[args.ID_column]] = {x : case[x] for x in args.chainID_columns}

    #generate the TCR AF3 submission files
    for i in range(args.num_seeds):
        for case_ID, chains_dict in cases.items():
            make_AF3_json(chains_dict, f"{case_ID}_rs{i}", args.output_dir, seednumber=None)
    print(f"All done! JSON files generated in {args.output_dir}")