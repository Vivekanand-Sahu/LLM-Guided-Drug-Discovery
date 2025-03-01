import datetime
from geneformer import Classifier
import torch

# If using saved model, define these parameters, can use the variables defined above

# output_prefix = "classify"
# output_dir = ''
# filter_data_dict=  # example {"subType":['GABA neurons', 'GLUT neurons']}            # set the filter on your data to be considered for all the tasks 
# input_data_file= # example "/home/ALKERMES/sahu_vivekanand/Data/scz_data/output_tokenize_balanced_scz_dataset_upsample_all_scz_indv.dataset"     # this is the tokenized dataset you will using 
# output_prefix = ''
# model_directory = ''

#OR

# If using Currently trained model
model_directory=f"{output_dir}/{datestamp_min}_geneformer_cellClassifier_{output_prefix}/ksplit1"
