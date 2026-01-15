import glob
import os
import shutil

model_dir = "/projects/0/prjs1135/SwiftTCR/Alphafold/ensemble/output_af3"
output_dir = "/projects/0/prjs1135/SwiftTCR/Alphafold/ensemble/processed_tcrs/all_tcrs"


for dir1 in glob.glob(f"{model_dir}/*"):
    basename = os.path.basename(dir1)
    for dir2 in glob.glob(f"{dir1}/*"):
        model_id = os.path.basename(dir2).split("-")[-1]
        af_id = os.path.basename(dir2)
        for path in glob.glob(f"{dir2}/*"):
            if path.endswith(".cif"):
                name = f"{basename}_m{model_id}.cif"
                destination_path = os.path.join(output_dir, name)
                shutil.copy(path,destination_path)