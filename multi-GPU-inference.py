# Select the correct kernel.
# Before running this file ensure to define: 

# set the following parameters #########
gpu_list = [2,3,4,5,6,7]  # Adjust this to the number of GPUs you have

dataset="/data-hpcwn-pnl03/FXG/Geneformer_archive/Data/Tokenized_dataset/output_tokenize_balanced_scz_dataset_upsample_all_scz_indv_no_add_features.dataset"  # tokenized data

model_directory = ''

gene_pert_list = ['CHRM4', 'DRD2', 'HTR2A', 'GPR88', 'KCNC1', 'GPR158', 'CHRM1', 'DRD3', 'TCF4']  # provide a list or ['all'] for perturbing all genes

########


import torch
import os
import pandas as pd

from multiprocessing import Pool, set_start_method
import pandas as pd
import datetime
import shutil

from geneformer import InSilicoPerturber
from geneformer import InSilicoPerturberStats
from geneformer import EmbExtractor


cell_states_to_model={"state_key": "condition", 
                      "start_state": "Scz", 
                      "goal_state": "Ctrl",
                      "alt_states": ["Scz"]}

filter_data_dict={"subType":['GABA neurons', 'GLUT neurons']} 


# Actual function
def perturb_genes(gene_pert_list, device_number, state_embs_dict, output_directory_folder):
    
    torch.cuda.set_device(device_number)

    current_date = datetime.datetime.now()
    datestamp = f"{str(current_date.year)[-2:]}{current_date.month:02d}{current_date.day:02d}{current_date.hour:02d}{current_date.minute:02d}{current_date.second:02d}"
    output_directory_folder = output_directory_folder + '/trials_' + str(device_number)+ '_' + str(datestamp)
    os.makedirs(output_directory_folder+ '/stats')
    pd.DataFrame(columns=['Pert_type', 'Gene_name', 'Shift_to_goal_end', 'Shift_to_alt_end_Scz']).to_csv(output_directory_folder + '/stats' + '/combined_stats.csv', index=False)
    print('output_directory_folder', output_directory_folder)
    
    df = pd.read_csv('/data-hpcwn-pnl03/FXG/Geneformer_archive/Data/In_silico_perturbation_files/unique_genes.csv') 
    df = df[~df['symbol'].str.startswith(('MIR', 'MT-'), na=False)]
    gene_dict = pd.Series(df.ensembl_id.values, index=df.symbol).to_dict()
    
    output_directory = 'Nothing'
    
    for s in gene_pert_list:
        for perturb_type in ["delete", "overexpress"]:
            try:
                print(perturb_type, s)
                current_date = datetime.datetime.now()
                datestamp = f"{str(current_date.year)[-2:]}{current_date.month:02d}{current_date.day:02d}{current_date.hour:02d}{current_date.minute:02d}{current_date.second:02d}"
                genes_ens_ids = list(gene_dict[x] for x in [s])
                genes = ''
                for i in [s]:
                    genes+=i + '_'
                genes = genes[:-1]

                output_directory = output_directory_folder + '/' + str(perturb_type + '_' + genes + '_' +str(datestamp))
                os.makedirs(output_directory)

                isp = InSilicoPerturber(perturb_type=perturb_type, 
                                    perturb_rank_shift=None,
                                    genes_to_perturb= genes_ens_ids, 
                                    combos=0,
                                    anchor_gene=None,
                                    model_type="CellClassifier",
                                    num_classes=2,
                                    emb_mode="cell",
                                    cell_emb_style="mean_pool",
                                    filter_data=filter_data_dict,
                                    cell_states_to_model= cell_states_to_model,    
                                    state_embs_dict=state_embs_dict,         
                                    max_ncells= 2000,
                                    emb_layer=0,
                                    forward_batch_size=160,
                                    nproc=1)

                isp.perturb_data(model_directory,
                              dataset,
                              output_directory,
                              "scz_output_pert")

                ispstats = InSilicoPerturberStats(mode= "goal_state_shift",
                                              genes_perturbed= genes_ens_ids, 
                                              combos=0,
                                              anchor_gene=None,
                                              cell_states_to_model=cell_states_to_model)

                ispstats.get_stats(output_directory,
                                   None,
                                   output_directory_folder + '/stats',
                                   str(perturb_type + '_' + genes + '_' + str(datestamp)))

                for file_name in os.listdir(output_directory_folder + '/stats'):
                    if file_name.startswith(('delete', 'overexpress')):
                        parts = file_name.split('_')
                        file_path = os.path.join(output_directory_folder + '/stats', file_name)
                        df = pd.read_csv(file_path)
                        new_row = {
                                    'Pert_type': parts[0],
                                    'Gene_name': parts[1],
                                    'Shift_to_goal_end': df['Shift_to_goal_end'].iloc[0],
                                    'Shift_to_alt_end_Scz': df['Shift_to_alt_end_Scz'].iloc[0]
                                }
                        # Append the new row to combined_stats.csv
                        combined_df = pd.DataFrame([new_row])
                        combined_df.to_csv(output_directory_folder + '/stats' + '/combined_stats.csv', mode='a', 
                                           header=not os.path.exists(output_directory_folder + '/stats' + '/combined_stats.csv'), 
                                           index=False)
                        os.remove(file_path)                 # CAUTION

            except Exception as e:
                print(f"An error occurred: {e}")

            finally:
                if os.path.exists(output_directory):
                    shutil.rmtree(output_directory)      # CAUTION
                    
def combine_nested_csv_files(main_folder):
    csv_data = []

    # Loop through each subfolder in the main folder
    for subfolder in os.listdir(main_folder):
        subfolder_path = os.path.join(main_folder, subfolder)

        # Check if it is a folder
        if os.path.isdir(subfolder_path):
            # Loop through the nested subfolders
            for nested_subfolder in os.listdir(subfolder_path):
                nested_subfolder_path = os.path.join(subfolder_path, nested_subfolder)

                # Check if the nested subfolder is a folder
                if os.path.isdir(nested_subfolder_path):
                    # Check for CSV files inside the nested subfolder
                    for filename in os.listdir(nested_subfolder_path):
                        if filename.endswith('.csv'):
                            file_path = os.path.join(nested_subfolder_path, filename)
                            # Read the CSV file and append to the list
                            csv_data.append(pd.read_csv(file_path))

    # Combine all the CSV files into a single DataFrame
    combined_df = pd.concat(csv_data, ignore_index=True)

    return combined_df

# Distribute the workload across GPUs
def run_on_all_gpus(gpu_list, gene_pert_list, state_embs_dict, output_directory_folder):
    # Split the gene list into chunks, one per GPU
    gene_chunks = [gene_pert_list[i::len(gpu_list)] for i in range(len(gpu_list))]

    # Set up multiprocessing with spawn method for CUDA compatibility
    set_start_method('spawn', force=True)

    # Create a pool of processes, each assigned to a different GPU
    with Pool(processes=len(gpu_list)) as pool:
        pool.starmap(perturb_genes, [(gene_chunks[i], gpu_list[i], state_embs_dict, output_directory_folder) for i in range(len(gpu_list))])

# Example usage
if __name__ == "__main__":
    df = pd.read_csv('/data-hpcwn-pnl03/FXG/Geneformer_archive/Data/In_silico_perturbation_files/unique_genes.csv') 
    df = df[~df['symbol'].str.startswith(('MIR', 'MT-'), na=False)]
    gene_dict = pd.Series(df.ensembl_id.values, index=df.symbol).to_dict()
    
    current_date = datetime.datetime.now()
    datestamp = f"{str(current_date.year)[-2:]}{current_date.month:02d}{current_date.day:02d}{current_date.hour:02d}{current_date.minute:02d}{current_date.second:02d}"
    
    output_directory_folder = f'/data-hpcwn-pnl03/FXG/Geneformer_archive/Data/In_silico_perturbation_files/M-GPU_trials_{datestamp}'
    os.makedirs(output_directory_folder)
    
    embex = EmbExtractor(model_type="CellClassifier",
                         num_classes=2,
                         filter_data=filter_data_dict,
                         max_ncells=1000, #1000
                         emb_layer=0,
                         summary_stat="exact_mean",
                         forward_batch_size=128,
                         nproc=16)     
    state_embs_dict = embex.get_state_embs(cell_states_to_model,
                                           model_directory,
                                           dataset,
                                           "/data-hpcwn-pnl03/FXG/Geneformer_archive/Data/In_silico_perturbation_files",
                                           "output_enc")
    if gene_pert_list == ['all']:
        gene_pert_list = list(gene_dict.keys())  
        
    try:
        run_on_all_gpus(gpu_list, gene_pert_list, state_embs_dict, output_directory_folder)
        print('Done')
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print('Here')
        combined_df = combine_nested_csv_files(output_directory_folder)
        combined_df.to_csv(output_directory_folder+'/final_' + str(datestamp) + '.csv', index=True)

        
    
    























