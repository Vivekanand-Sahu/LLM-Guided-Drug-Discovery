# to perturb single or list of genes perturbed simultaneously
genes_list = ['TCF4'] # OR ['TCF4', 'CHRM4']
perturb_type = 'delete' 


import datetime

current_date = datetime.datetime.now()
datestamp = f"{str(current_date.year)[-2:]}{current_date.month:02d}{current_date.day:02d}{current_date.hour:02d}{current_date.minute:02d}{current_date.second:02d}"


genes_ens_ids = list(gene_dict[x] for x in genes_list)
genes = ''
for i in genes_list:
    genes+=i + '_'
genes = genes[:-1]

output_directory = output_directory_folder + '/' + str(perturb_type + 'ing_' + genes + '_' +str(datestamp))
os.makedirs(output_directory)

print(perturb_type, genes_list)

# perturbation function
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
                        forward_batch_size=128,       # change this if you encounter memory issue
                        nproc=1)


# perform perturbation
isp.perturb_data(model_directory,
                  dataset,
                  output_directory,
                  "scz_output_pert")


# function to get perturbed data  statistics
ispstats = InSilicoPerturberStats(mode= "goal_state_shift",
                                  genes_perturbed= genes_ens_ids, 
                                  combos=0,
                                  anchor_gene=None,
                                  cell_states_to_model=cell_states_to_model)


# extracts data from intermediate files and processes stats to output in final .csv
ispstats.get_stats(output_directory,
                   None,
                   output_directory,
                   "output_pert_stats")
