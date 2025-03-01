# tokenization

from geneformer import TranscriptomeTokenizer

# Include features from the scRNA data that you want to include in your tokenized dataset in the format: "col name in scRNA data" : "col name in tokenized data"
tk = TranscriptomeTokenizer(custom_attr_name_dict = {"cellTypeL2":"subType",          # features to keep
                                                     #"orig.ident": "individual", 
                                                     "cellType": "cellType", 
                                                     "condition": "condition",
                                                     # "nCount_RNA": "nCount_RNA",
                                                     # "percent.mt":"percent_mt",
                                                     # "nFeature_RNA":"nFeature_RNA",
                                                     # "Age" : "Age",
                                                     # "Gender":"Gender"
                                                    }, nproc=16)

tk.tokenize_data( '/data-hpcwn-pnl03/FXG/Geneformer_archive/Data/scRNA_dataset',  # All the .h5ad files in this directory will be tokenized. Keep only the file you want to tokenize.
                 "/data-hpcwn-pnl03/FXG/Geneformer_archive/Data/Tokenized_dataset", # output directory where the tokenized file will be saved
                 "output_tokenize_balanced_scz_dataset_upsample_all_scz_indv_no_indv_ids", # output file name, give unique name to your tokenized file to avoid overlap
                 file_format="h5ad")
