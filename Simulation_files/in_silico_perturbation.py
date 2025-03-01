#If using saved model, define these parameters, can use the variables defined above

# output_prefix = "classify"
# output_dir = ''
# filter_data_dict=  # example {"subType":['GABA neurons', 'GLUT neurons']}            # set the filter on your data to be considered for all the tasks 
# input_data_file= # example "/home/ALKERMES/sahu_vivekanand/Data/scz_data/output_tokenize_balanced_scz_dataset_upsample_all_scz_indv.dataset"     # this is the tokenized dataset you will using 
# output_prefix = ''
# model_directory = ''


from geneformer import InSilicoPerturber
from geneformer import InSilicoPerturberStats
from geneformer import EmbExtractor

# Defining cell states
cell_states_to_model={"state_key": "condition", 
                      "start_state": "Scz", 
                      "goal_state": "Ctrl",
                      "alt_states": ["Scz"]}

output_directory_folder = "/data-hpcwn-pnl03/FXG/Geneformer_archive/Data/In_silico_perturbation_files"
dataset=input_data_file

# creating the embedding extrctor
embex = EmbExtractor(model_type="CellClassifier",
                     num_classes=2,
                     filter_data=filter_data_dict,
                     max_ncells=10000, #1000
                     emb_layer=0,
                     summary_stat="exact_mean",
                     forward_batch_size=120,
                     nproc=16)     

# Extract exact mean or exact median cell state embedding positions from input data and save as results in output_directory.
state_embs_dict = embex.get_state_embs(cell_states_to_model,
                                       model_directory,
                                       dataset,
                                       output_directory_folder,
                                       "output_enc")
import pandas as pd

# Importing the list of unique genes present in the dataset
df = pd.read_csv('/data-hpcwn-pnl03/FXG/Geneformer_archive/Data/In_silico_perturbation_files/unique_genes.csv') 
print(df.shape)

# Ignore genes starting from 'MIR' and 'MT-'
df = df[~df['symbol'].str.startswith(('MIR', 'MT-'), na=False)]
print(df.shape)

# Create the dictionary
gene_dict = pd.Series(df.ensembl_id.values, index=df.symbol).to_dict()
