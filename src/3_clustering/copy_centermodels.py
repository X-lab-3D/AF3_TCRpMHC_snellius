import os
import glob
import shutil
import re
import json
from argparse import ArgumentParser

"""
script copies the center models of the clustering text file obtained from cluster_tcr_profit.py.
The model will renamed to pdbid_c* (c* = the cluster number).

input:
    cluster_dir = path to the output directory of the clustering text files. (example /7l1d.txt)
    output_dir = path to the directory to save the cluster centers.

Assumptions: the first four characters of the .pdb name contains the PDB ID. 
"""

def copy_center_models_from_txt(cluster_txt, path_dict_json, output_dir):
    """
    Copies cluster center models to an output directory, renaming them with their cluster ID.

    cluster_txt : path to cluster_centers.txt
    path_dict_json : JSON file containing {model_index: full_path}
    output_dir : directory where the center models will be copied
    """

    os.makedirs(output_dir, exist_ok=True)

    # Load path dictionary
    with open(path_dict_json, "r") as f:
        path_dict = json.load(f)

    path_dict = {int(key): path for key, path in path_dict.items()}  # keys as integers

    # Regex to extract cluster ID and model index
    pattern = re.compile(r"Cluster (\d+).*Center = .* \(index (\d+)\)")

    with open(cluster_txt, "r") as f:
        for line in f:
            match = pattern.search(line) #search for pattern in .txt
            if match:
                cluster_id = int(match.group(1)) #save clusterid
                model_index = int(match.group(2)) #save the index of model

                if model_index not in path_dict:
                    print(f"Warning: model index {model_index} not found in path_dict")
                    continue

                model_path = path_dict[model_index] #search path with model index
                # New name using cluster ID (optional: include original filename)
                orig_name = os.path.basename(model_path).split("_")[0]
                new_name = f"{orig_name}_c{cluster_id}.pdb"

                new_path = os.path.join(output_dir, new_name)
                shutil.copy2(model_path, new_path)
                print(f"Copied {model_path} -> {new_path}")

if __name__ == "__main__":

    parser = ArgumentParser(description="Copies the center of each cluster to an output directory, renaming them with their cluster ID.")
    parser.add_argument(
        "--cluster-dir",
        type=str,
        required=True,
        help="Directory containing multi_*.txt structure files",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="Directory containing RMSD .txt files from ProFit",
    )
    args = parser.parse_args()
    #cluster_dir = "/projects/0/prjs1135/SwiftTCR/Alphafold/ensemble/processed_tcrs/cluster_files" #filename example /7l1d.txt
    
    #output_dir = "/projects/0/prjs1135/SwiftTCR/SwiftTCR/input_tcr"
    cluster_dir = args.cluster_dir
    output_dir = args.output_dir
    path_dir = os.path.join(cluster_dir,"caseids_dict")
    
    for file in glob.glob(f"{cluster_dir}/*"):
        pdb = os.path.basename(file).split(".")[0]
        for path_dict in glob.glob(f"{path_dir}/*"):
            pdb_d = os.path.basename(path_dict).split("_")[2]
            if pdb_d == pdb:
                copy_center_models_from_txt(file, path_dict, output_dir)

