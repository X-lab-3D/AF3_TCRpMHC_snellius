import json
import os
import glob
from collections import defaultdict
from argparse import ArgumentParser

"""
This function generates scripts and multifiles used for the RMSD calculation 
using the ProFit version 3.3. The multifile path is connected in the script for 
the rmsd calculations. 

The script is designed for TCR RMSD calculations, where IMGT-numbering is used
to align the backbone of TCRs base structure (everything except the CDR loops).

input:  input_dir = directory containing the processed pdbs (.pdb files)
        output_dir = output directory for the profit scripts
        output_dir_multi = the directory to locate the multi files in containing
                            all the model paths.

output: a ProFit script and Multi-file in a txt file. The script will be named
        calc_tcr_rmsd_{PDB ID}.txt ( {} marks a variable id name )
        the multi file will be named multi_{PDB ID}.txt

Assumption:
    The TCRs are IMGT numbered to perform the correct alignment.
    The structure files are in a pdb format         

"""

def generate_multi_file(path_list,output_dir,name_file):
    """
    input:  path_list = list of paths to add in the multifile
            output_dir = the output directory to place the multi structure file for profit.
            name_file = unique identifier to label the output
    """
    output_path = os.path.join(output_dir,f"multi_{name_file}.txt")

    with open(output_path,"w") as f:
        f.write("\n".join(path_list))
    return output_path

def make_pairwise_rmsd_script(structure_file,output_dir,name_file,template_script='./template_TCR_rmsd.txt'):
    """
    input:  structure file = list of paths to add in the multifile
            output_dir = the output directory to place the script for profit.
            name_file = unique identifier to label the output
            template_script = path to the template script for ProFit RMSD calculation
    """

    # generate script to calculate overall
    with open(template_script, "r") as f:
        template = f.read()
        template = template.replace("##MULTIFILE_PLACEHOLDER##", structure_file)

    output_path = os.path.join(output_dir,f"calc_tcr_rmsd_{name_file}.txt")
    with open(output_path, "w") as f:
        f.write(template)


if __name__ == "__main__":

    parser = ArgumentParser(description="Generate ProFit multi-files and RMSD scripts.")
    parser.add_argument(
        "--input-dir","-i",
        default="/projects/0/prjs1135/SwiftTCR/Alphafold/ensemble/processed_tcrs/renumbered",
        help="Directory containing processed .pdb files",

    )
    parser.add_argument(
        "--output-dir","-o",
        default="/projects/0/prjs1135/SwiftTCR/Alphafold/ensemble/scripts/clustering",
        help="Directory to write ProFit scripts",
    )
    parser.add_argument(
        "--output-dir-multi","-m",
        default="/projects/0/prjs1135/SwiftTCR/Alphafold/ensemble/scripts/clustering/profit_input",
        help="Directory to write ProFit multi-files",
    )
    parser.add_argument(
        "--template-script","-t",
        default="./templates/template_TCR_rmsd.txt",
        help="Path to the template script for ProFit RMSD calculation",
    )

    args = parser.parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir
    output_dir_multi = args.output_dir_multi
    template_script = args.template_script

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(output_dir_multi, exist_ok=True)

    groups = defaultdict(list)

    
    for path in glob.glob(f"{input_dir}/*"):
        if path.endswith(".pdb"):
            name_file = os.path.basename(path)
            pdb_id = name_file[:4]
            groups[pdb_id].append(path)

    for pdb_id, paths in groups.items():
        output_mult = generate_multi_file(paths,output_dir_multi,pdb_id)
        make_pairwise_rmsd_script(output_mult,output_dir,pdb_id,template_script)