import os
import glob
import json
from sklearn.cluster import AgglomerativeClustering
from io import StringIO
import numpy as np
import pandas as pd

"""
Script to cluster the TCRs using the rmsd text file from profit. 
Agglomerative clustering complete linkage is used automatically. 

Input:
    dir_struct = directory where the multi files of profit are located
    dir_rmsd = the directory containing the results of profits rmsd calculation
    output_dir = desired output directory for the results 

Output: 
    text file ordered like the example. The cluster id, cluster size, center model,
    index and average RMSD is provided. Additionally, two folders will be generated 
    (csv and caseids_dict), which will contain json files containing the model paths connected 
    to the csv row/column labels and a csv file containing the rmsd values.

Example:
Cluster 0, cluster size 10: Center = 7na5_rs2_m2.pdb (index 12), avg RMSD = 0.439
Cluster 1, cluster size 3: Center = 7na5_rs4_m3.pdb (index 23), avg RMSD = 0.372
Cluster 2, cluster size 9: Center = 7na5_rs4_m4.pdb (index 22), avg RMSD = 0.502
Cluster 3, cluster size 1: Center = 7na5_rs0_m1.pdb (index 16), avg RMSD = 0.000
Cluster 4, cluster size 2: Center = 7na5_rs4_m2.pdb (index 1), avg RMSD = 0.277

the index indicates the row in the multi file, meaning first row = index 1. 
This is related to .csv returned by this function

Assumptions:    Default setting for the amount of clusters is 5
                Defaults setting linkage method is complete linkage

"""

def cluster_input_tcrs(input_rmsd,input_struct,output_dir,n_clusters,linkage_clus="complete"):
    """
    This method is generated to cluster TCRs into defined groups. The RMSD calculation are obtained 
    from Profit

    Input:  input_rmsd = path to the .txt file generated from profits AllvsAll rmsd calculation.

            input_struc = path to the multi file used to calculate rmsd's. 

            output_dir = The output directory to save the rmsd csv and cluster file

            chainid = the chain ID label of the protein

            n_clusters = the amount of clusters obtained from Agglomerative Clustering with the RMSDs

            linkage_clus = Type of linkage method for clustering, options: ["ward","complete","average","single"].
                            The method is automatically complete linkage.
            
    Output: rmsd_df = a dataframe containing the rmsd matrix of all models, 
                        index and columns are indexed

            cluster_df = a dataframe containing the cluster ID, indexes of each model and file name. 

            a cluster center .txt file containing  per cluster the cluster ID, cluster size,
              centermodel filename, modelindex and average RMSD
    """
    #Runs each function
    rmsd_df, path_dict = rmsd_matrix_profit(input_rmsd,input_struct,output_dir)
    cluster_df = clustering_models(rmsd_df,path_dict,n_clusters,linkage_clus)

    #generate inputfile
    name = os.path.basename(input_struct).split("_")[1].replace(".txt","")
    center_model_cluster(cluster_df,rmsd_df,output_dir,name)

    return rmsd_df, cluster_df


def rmsd_matrix_profit(input_rmsd,input_struct,output_dir):
    """
    Reads the ProFit log and Multi file. These files are used to extract
    the rmsd and structure paths
    
    input: 
        input_rmsd: path to the ProFit log file containing the rmsd values
        input_struct: path to the multi files of ProFit
        output_dir: Description

    output: 
        a csv/pandas dataframe containing the rmsd values 
        a dictionary connecting the row/column ids to a modelpath
    """

    #extract matrix
    with open(input_rmsd,"r") as f:
        file = f.readlines()
        for i,line in enumerate(file):
            if line.startswith("\t"): #searces for the tab at the rmsd matrix output
                break
        f_matrix = file[i:] #save all lines containing the rmsd values

    text = "".join(f_matrix)
    df = pd.read_csv(StringIO(text), sep="\t") #dataframe of the rmsd values
    df = df.set_index(df.columns[0])
    df.index.name = "model"

    #extract the model paths and connect to column ID
    with open(input_struct,"r") as f:
        file_paths = f.readlines()

    #generates dict of model IDs connected to structure path
    path_dict = {i+1:line.replace("\n","") for i, line in enumerate(file_paths)} 

    #make outputpath for the rmsd df
    csv_dir = os.path.join(output_dir,"csv")
    filename = f"{os.path.basename(input_rmsd).split('.')[0]}.csv"
    csv_path = os.path.join(csv_dir,filename)

    #make output dictionary
    id_dir = os.path.join(output_dir,"caseids_dict")
    filename = f"{os.path.basename(input_rmsd).split('.')[0]}.json"
    id_path = os.path.join(id_dir,filename)

    #make output directory and generate .csv and dictionary
    os.makedirs(csv_dir, exist_ok=True)
    os.makedirs(id_dir, exist_ok=True)

    #make csv of df
    df.to_csv(csv_path)

    with open(id_path,"w") as f:
        json.dump(path_dict, f, indent=4)

    return df, path_dict
    


def clustering_models(rmsd_df,path_dict,n_clusters,m_linkage):
    """
    This function clusters the models based on RMSD with agglomerative clustering.
    Assumption: the columns ids and index ids are integers.

    Input:  rmsd_df = a dataframe containing all the paired rmsd values
                        with a label in the columns and rows corresponding to a dictionary with paths.

            path_dict = a dictionary containing the column/index IDs coupled to a modelpath

            n_clusters = the amount of clusters you want to obtain

            m_linkage = the linkage method applied during Agglomerative
                            clustering, options: ["ward","complete","average","single"]

    output: cluster_df = a dataframe containing the following the models index (model_index),
                            cluster (cluster_id) and the file name (id_file)

    """

    rmsd_df.columns = rmsd_df.columns.astype(int)
    rmsd_df.index = rmsd_df.index.astype(int)


    distance_matrix = rmsd_df.to_numpy()
    # clustering
    cluster = AgglomerativeClustering(
        n_clusters=n_clusters, 
        metric='precomputed', 
        linkage=m_linkage
    ).fit(distance_matrix)

    if isinstance(path_dict, dict):
        # check the column matches
        column_ids = sorted([c_id for c_id in rmsd_df.columns])
        for column_id in column_ids:
            if path_dict[column_id]:
                continue
            else:
                print(f"dictionary has a mismatch: {column_id}")
                print(f"Provided dictionary: {path_dict}")

    ids_model = [os.path.basename(path_dict[key]) for key in rmsd_df.index]

    cluster_df = pd.DataFrame({
        "model_index": rmsd_df.index,
        "cluster_id": cluster.labels_,
        "id_file":ids_model})
    
    return cluster_df

def center_model_cluster(cluster_df,rmsd_df,output_dir,name):
    """
    This function determines the center model of the given cluster and rmsd dataframes.
    Generating a .txt file containing the cluster IDs, cluster sizes, cluster centers name,
    indexes and average RMSD. 

    input :     cluster_df = a dataframe containing these columns = ["model_index","cluster_id","id_file"],
                                which includes the models index, cluster label and filename/label model

                rmsd_df = a dataframe containing all paired RMSD values in a matrix with columns and
                            indexes containing the models index.

                output_dir = the output directory to save the cluster file
    """
    
    labels = cluster_df["cluster_id"].unique() #cluster number

    cluster_models = {}
    #extract model file names 
    for l in labels:
        df_new = cluster_df[cluster_df["cluster_id"] == l] #df per cluster
        m_clus = df_new["id_file"].to_numpy() #file names
        ind_m = df_new["model_index"].to_numpy() #index of the multifile
        cluster_models[l] = {"ID":m_clus,"index":ind_m}

    cluster_dfs = {}

    #generate the df per cluster
    for cluster_id, cluster_data in cluster_models.items():
        cluster_sub_df = pd.DataFrame({
            "index": cluster_data["index"],
            "ID": cluster_data["ID"]
        })
        cluster_dfs[cluster_id] = cluster_sub_df

    cluster_centers = {}

    for cluster_id, cluster_data in cluster_models.items():
        indices = cluster_data["index"]

        # Extract the submatrix of RMSDs for this cluster
        submatrix = rmsd_df.loc[indices, indices] #loc searches the label
        print(submatrix)

        # Compute average distance of each model to others (per row)
        mean_rmsd = submatrix.mean(axis=1)

        # Returns index label of the minimum
        center_index = mean_rmsd.idxmin()

        # Get corresponding ID
        center_id = cluster_data["ID"][np.where(cluster_data["index"] == center_index)[0][0]]

        cluster_centers[cluster_id] = {
            "center_index": center_index,
            "center_ID": center_id,
            "mean_RMSD": mean_rmsd[center_index],
            "cluster_size":len(submatrix)
        }

    output_file = os.path.join(output_dir,f"{name}.txt")

    # Display results
    with open(output_file, "w") as f:
        for cid in sorted(cluster_centers.keys()):
            info = cluster_centers[cid]
            f.write(
                f"Cluster {cid}, cluster size {info['cluster_size']}: "
                f"Center = {info['center_ID']} (index {info['center_index']}), "
                f"avg RMSD = {info['mean_RMSD']:.3f}\n"
            )

if __name__ == "__main__":


    parser = ArgumentParser(description="Clusters TCR structures based on ProFit RMSD outputs.")
    parser.add_argument(
        "--dir-struct",
        type=str,
        required=True,
        help="Directory containing multi_*.txt structure files",
    )
    parser.add_argument(
        "--dir-rmsd",
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
        "--n-clusters",
        type=int,
        default=5,
        help="Number of agglomerative clusters (default: 5)",
    )
    parser.add_argument(
        "--linkage",
        type=str,
        default="complete",
        choices=["ward", "complete", "average", "single"],
        help="Linkage method for clustering (default: complete)",
    )

    args = parser.parse_args()

    dir_struct = args.dir_struct
    dir_rmsd = args.dir_rmsd
    output_dir = args.output_dir

    rmsd_files = glob.glob(os.path.join(dir_rmsd, "*.txt"))
    struct_files = glob.glob(os.path.join(dir_struct, "multi_*.txt"))

    print(f"[DEBUG] Found {len(rmsd_files)} RMSD files")
    print(f"[DEBUG] Found {len(struct_files)} STRUCT files")

    for rmsd_file in rmsd_files:
        fname = os.path.basename(rmsd_file)
        parts = fname.replace(".txt", "").split("_")

        if len(parts) < 4:
            print(f"[SKIP] Unexpected RMSD filename: {fname}")
            continue

        pdb = parts[-1]   # altijd laatste deel → 1ao7
        print(f"[DEBUG] Processing RMSD: {fname} → PDB = {pdb}")

        matched = False
        for struct_file in struct_files:
            sname = os.path.basename(struct_file)
            s_pdb = sname.replace("multi_", "").replace(".txt", "")

            if s_pdb == pdb:
                print(f"[DEBUG] Match found: {sname}")
                cluster_input_tcrs(
                    rmsd_file,
                    struct_file,
                    output_dir,
                    n_clusters=args.n_clusters,
                    linkage_clus=args.linkage
                )
                matched = True
                break

        if not matched:
            print(f"[WARNING] No STRUCT match for {fname}")
