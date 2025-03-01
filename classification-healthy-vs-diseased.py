# classification healthy vs diseased

import datetime
from geneformer import Classifier
import torch
import ray
from ray import tune
import pandas as pd


current_date = datetime.datetime.now()
datestamp = f"{str(current_date.year)[-2:]}{current_date.month:02d}{current_date.day:02d}{current_date.hour:02d}{current_date.minute:02d}{current_date.second:02d}"
datestamp_min = f"{str(current_date.year)[-2:]}{current_date.month:02d}{current_date.day:02d}"

output_prefix = "classify"
output_dir = f"/data-hpcwn-pnl03/FXG/Geneformer_archive/Data/classification/{datestamp}"
!mkdir $output_dir

print(datestamp,output_dir,output_prefix)

filter_data_dict= {"subType":['GABA neurons', 'GLUT neurons']}            # set the filter on your data to be considered for all the tasks 
input_data_file="/data-hpcwn-pnl03/FXG/Geneformer_archive/Data/Tokenized_dataset/output_tokenize_balanced_scz_dataset_upsample_all_scz_indv_no_add_features.dataset"     # this is the tokenized dataset you will using 


def Ind_split_Classification():
  # this is the split of individuals. You can find better split by performing some data analysis
  train_ids = [ 'MB0', 'MB6', 'MB10', 'MB14',  'MB8', 'MB8-2', 'MB12', 'MB23', 
               'MB7', 'MB9', 'MB11',  'MB15', 'MB17', 'MB21', 'MB18-2', 'MB51', 'MB57', 'MB53']
  eval_ids = ['MB22', 'MB54', 
               'MB13', 'MB16', 'MB55']
  test_ids = ['MB56', 
               'MB19']
  train_test_id_split_dict = {"attr_key": "individual",
                              "train": train_ids+eval_ids,
                              "test": test_ids}
  
  train_valid_id_split_dict = {"attr_key": "individual",
                              "train": train_ids,
                              "eval": eval_ids}
  
  # hyperparameters used for training
  training_args = {
      "num_train_epochs": 1,                          
      "learning_rate": 0.000996769 ,                          
      "lr_scheduler_type":"polynomial",                  
      "warmup_steps": 467 ,
      "weight_decay": 0.606852 ,        
      "per_device_train_batch_size": 8,              
      "seed": 9, #73,
  }
  
  def_ray_config = None
  n_hyperopt_trials = 0



def Indv_split_Hyperparameter_Tuning():
  # this is the split of individuals. You can find better split by performing some data analysis
  train_ids = [ 'MB0', 'MB6', 'MB10', 'MB14',  'MB8', 'MB8-2', 'MB12', 'MB23', 
               'MB7', 'MB9', 'MB11',  'MB15', 'MB17', 'MB21', 'MB18-2', 'MB51', 'MB57', 'MB53']
  eval_ids = ['MB22', 'MB54', 
               'MB13', 'MB16', 'MB55']
  test_ids = ['MB56', 
               'MB19']
  train_test_id_split_dict = {"attr_key": "individual",
                              "train": train_ids+eval_ids,
                              "test": test_ids}
  
  train_valid_id_split_dict = {"attr_key": "individual",
                              "train": train_ids,
                              "eval": eval_ids}
  
  training_args = None
  
  # the range of values for each hyperparameter that you want to consider duing hyperparameter trials
  def_ray_config = {
      "num_train_epochs": tune.choice([1]),                       
      "learning_rate": tune.loguniform(1e-6, 1e-3),
      "weight_decay": tune.uniform(0.2, 0.7),
      "lr_scheduler_type": tune.choice(["cosine", "polynomial"]),
      "warmup_steps": tune.randint(100, 2000),
      "seed": tune.randint(0, 10),
      "per_device_train_batch_size": tune.choice(
          [8, 16]
      ),                                       
  }
  
  n_hyperopt_trials = 100

def Homo_split_Classification():
  train_test_id_split_dict = None
  train_valid_id_split_dict = None
  
  # hyperparameters used for training
  training_args = {
      "num_train_epochs": 1,                          
      "learning_rate": 0.000996769 ,                          
      "lr_scheduler_type":"polynomial",                 
      "warmup_steps": 467 , 
      "weight_decay": 0.606852 ,        
      "per_device_train_batch_size": 8,              
      "seed": 9, 
  }
  
  def_ray_config = None
  n_hyperopt_trials = 0


def Homo_split_Hyperparameter_Tuning():
  train_test_id_split_dict = None
  train_valid_id_split_dict = None
  
  training_args = None
  
  # the range of values for each hyperparameter that you want to consider duing hyperparameter trials
  def_ray_config = {
      "num_train_epochs": tune.choice([1]),                       
      "learning_rate": tune.loguniform(1e-6, 1e-3),
      "weight_decay": tune.uniform(0.2, 0.7),
      "lr_scheduler_type": tune.choice(["cosine", "polynomial"]),
      "warmup_steps": tune.randint(100, 2000),
      "seed": tune.randint(0, 10),
      "per_device_train_batch_size": tune.choice(
          [8, 16]
      ),                                        
  }
  
  n_hyperopt_trials = 100
