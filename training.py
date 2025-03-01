# Defining the classifier
cc = Classifier(classifier="cell",
                cell_state_dict = {"state_key": "condition", "states": "all"},
                filter_data=filter_data_dict,
                training_args=training_args,
                max_ncells=None,
                freeze_layers = 3,
                num_crossval_splits = 1,          
                forward_batch_size=128,           # It is the inference batch size (not training). changing this if you have cuda error
                nproc=16,
                ray_config = def_ray_config, 
                split_sizes={"train": 0.7, "valid": 0.2, "test": 0.1},
                ngpu=torch.cuda.device_count())   # number of GPUs to be used


# prepares the training, val, test datasets
cc.prepare_data(input_data_file=input_data_file,
                output_directory=output_dir,
                output_prefix=output_prefix,
                split_id_dict=train_test_id_split_dict 
               )

# training and validation 
all_metrics = cc.validate(model_directory="/data-hpcwn-pnl03/FXG/Geneformer_archive/geneformer_libs/Geneformer_VS",
                          prepared_input_data_file=f"{output_dir}/{output_prefix}_labeled_train.dataset",
                          id_class_dict_file=f"{output_dir}/{output_prefix}_id_class_dict.pkl",
                          output_directory=output_dir,
                          output_prefix=output_prefix,
                          split_id_dict=train_valid_id_split_dict,
                          n_hyperopt_trials=n_hyperopt_trials
                          )
