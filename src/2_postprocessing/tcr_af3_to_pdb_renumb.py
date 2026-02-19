import sys
import os
import glob
import warnings
import subprocess
from Bio.PDB import MMCIFParser, PDBIO
from argparse import ArgumentParser

"""
Script converts mmcif to pdb and renumbers them using ANARCI's immunopdb script.

ANARCI github: https://github.com/oxpig/ANARCI
"""

def main(mmcif_path,outputdir, immunopdb):
    """
    This script converts a mmcif to a pdb file and renumbers the TCR structure
    to IMGT numbering appying ANARCI.
    """
    output_pdb = mmcif_to_pdb(mmcif_path,outputdir)
    run_anarci(output_pdb,outputdir)

def run_command(command):
    """
    Helper function to run a command with subprocess.run and handle errors.
    
    Args:
        command (str): The shell command to be executed.
        
    Returns:
        str: The standard output of the command if successful.
    
    Raises:
        subprocess.CalledProcessError: If the command fails.
    """
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running command: {command}")
        print(f"Error message: {e.stderr}")
        raise


def mmcif_to_pdb(mmcif_path,output_dir):
    """
    This function converts mmcif files to pdb. 

    input:  mmcif_path = path to the mmcif file that needs to be converted to pdb.
            output_dir = the directory to place the pdb file.
    
    output: A pdb will be saved in the directory containing the same
            basename as the mmcif and the path will be returned. 
    
    """
    basename = os.path.basename(mmcif_path).split(".")[0]
    pdb_file = f"{basename}.pdb"

    parser = MMCIFParser()
    structure = parser.get_structure("model", mmcif_path)

    output_pdb = os.path.join(output_dir,pdb_file)
    io = PDBIO()
    io.set_structure(structure)
    io.save(output_pdb)

    return output_pdb

def run_anarci(pdb_path,output_dir, immunopdb= immunopdb):
    #shift TCR numbering due to overwriting residue numbers
    command_sel_tcr_reres = f"pdb_reres -500 {pdb_path} > tcr_shifted.pdb"
    run_command(command_sel_tcr_reres)

    basename = os.path.basename(pdb_path)
    output_path = os.path.join(output_dir,basename)

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", module='Bio.PDB')
        subprocess.run([
            "python", immunopdb,
            "-i", "tcr_shifted.pdb",
            "-o", output_path,
            "-s", "imgt",
            "--receptor", "tr"
        ], check=True)
    
    os.remove("tcr_shifted.pdb")

if __name__ == "__main__":

    parser = ArgumentParser(description="Clusters TCR structures based on ProFit RMSD outputs.")
    
    parser.add_argument(
        "--input-dir",
        type=str,
        required=True,
        help="Directory containing RMSD .txt files from ProFit",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="Directory where clustering outputs will be written",
    )
    parser.add_argument(
        "--immunopdb-path",
        type=str,
        help="Path to the ImmunoPDB script of ANARCI",
        default="/projects/0/prjs1135/software/ANARCI/Example_scripts_and_sequences/ImmunoPDB.py"
    )

    args = parser.parse_args()
    immunopdb = args.immunopdb_path
    input_dir = args.input_dir
    output_dir = args.output_dir

    #loop over input dir 
    for path in glob.glob(f"{input_dir}/*"):
        id_output = os.path.basename(path).split(".")[0]
        if  path.endswith(".cif"):
            main(path,output_dir, immunopdb)
