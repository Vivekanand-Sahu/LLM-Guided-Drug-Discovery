import datetime
import shutil

# In silico perturbation function that perturbes all genes mentioned in the list fed as an input to the model. 
# Remember that it uses only the first GPU. For utilizing all the GPUs use the multiGPU .py file. 
def perturb_genes(gene_pert_list):
    output_directory_folder = "/data-hpcwn-pnl03/FXG/Geneformer_archive/Data/In_silico_perturbation_files"
    current_date = datetime.datetime.now()
    datestamp = f"{str(current_date.year)[-2:]}{current_date.month:02d}{current_date.day:02d}{current_date.hour:02d}{current_date.minute:02d}{current_date.second:02d}"
    output_directory_folder = output_directory_folder + '/trials_' + str(datestamp)
    os.makedirs(output_directory_folder+ '/stats')
    pd.DataFrame(columns=['Pert_type', 'Gene_name', 'Shift_to_goal_end', 'Shift_to_alt_end_Scz']).to_csv(output_directory_folder + '/stats' + '/combined_stats.csv', index=False)
    print('for', output_directory_folder)
    
    output_directory = ''
    
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
                                    cell_states_to_model= cell_states_to_model,      # None,cell_states_to_model
                                    state_embs_dict=state_embs_dict,          # None, state_embs_dict
                                    max_ncells= 2000,
                                    emb_layer=0,
                                    forward_batch_size=128,   # reduce this to avoid cuda memory error
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

            

