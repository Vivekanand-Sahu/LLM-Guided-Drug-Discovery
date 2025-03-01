# If using saved model, define these parameters, can use the variables defined above

# output_prefix = "classify"
# output_dir = ''
# filter_data_dict=  # example {"subType":['GABA neurons', 'GLUT neurons']}            # set the filter on your data to be considered for all the tasks 
# input_data_file= # example "/home/ALKERMES/sahu_vivekanand/Data/scz_data/output_tokenize_balanced_scz_dataset_upsample_all_scz_indv.dataset"     # this is the tokenized dataset you will using 
# output_prefix = ''
# model_directory = ''


from geneformer import EmbExtractor

# initiate EmbExtractor
embex = EmbExtractor(model_type="CellClassifier",
                     num_classes=2,
                     filter_data=filter_data_dict, 
                     max_ncells=10000,
                     emb_layer=0,
                     emb_label=["condition"], # viz embeddings on this parameter 
                     labels_to_plot=["condition"], # viz embeddings on this parameter 
                     forward_batch_size=200,
                     nproc=16)


embs = embex.extract_embs(model_directory,
                          input_data_file,
                          "/data-hpcwn-pnl03/FXG/Geneformer_archive/Data/embeddings", # output directory
                          "output_prefix_emb_plot" # output file name
                         )

# UMAP for embeddings
embex.plot_embs(embs=embs,
                plot_style="umap",
                output_directory="/data-hpcwn-pnl03/FXG/Geneformer_archive/Data/embeddings",  
                output_prefix="output_prefix_plot",
               max_ncells_to_plot = 1000)


# Heatmap for embeddings
embex.plot_embs(embs=embs, 
                plot_style="heatmap",
                output_directory="/data-hpcwn-pnl03/FXG/Geneformer_archive/Data/embeddings",  
                output_prefix="output_prefix_plot_heat")
