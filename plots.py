# redefining classifier
cc = Classifier(classifier="cell",
                cell_state_dict = {"state_key": "condition", "states": "all"},
                forward_batch_size=200, # change this if you encounter Cuda memory error
                nproc=16)

# results on test set
all_metrics_test = cc.evaluate_saved_model(
        model_directory=model_directory,       
        id_class_dict_file=f"{output_dir}/{output_prefix}_id_class_dict.pkl",
        test_data_file=f"{output_dir}/{output_prefix}_labeled_test.dataset",
        output_directory=output_dir,
        output_prefix=output_prefix,
    )

# plotting conf matrix 
cc.plot_conf_mat(
        conf_mat_dict={"Geneformer": all_metrics_test["conf_matrix"]},
        output_directory=output_dir,
        output_prefix=output_prefix,
        custom_class_order=["Scz", "Ctrl"]
                           )

# plotting heatmap on confidence scores
cc.plot_predictions(
    predictions_file=f"{output_dir}/{output_prefix}_pred_dict.pkl",
    id_class_dict_file=f"{output_dir}/{output_prefix}_id_class_dict.pkl",
    title="condition",
    output_directory=output_dir,
    output_prefix=output_prefix,
    #custom_class_order=["Ctrl","Scz"],
)



# plotting ROC
import numpy as np
import matplotlib.pyplot as plt

# Extracting the data from the dictionary
mean_tpr = np.array(all_metrics_test["all_roc_metrics"]['mean_tpr'])
mean_fpr = np.array(all_metrics_test["all_roc_metrics"]['mean_fpr'])
all_roc_auc = all_metrics_test["all_roc_metrics"]['all_roc_auc']


# Plotting the ROC curve
plt.figure(figsize=(8, 6))
plt.plot(mean_fpr, mean_tpr, color='b', lw=2, label=f'ROC curve (area = {all_roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='gray', linestyle='--')

# Adding labels and title
plt.xlabel('False Positive Rate', fontsize=10)
plt.ylabel('True Positive Rate', fontsize=10)
plt.title('Receiver Operating Characteristic', fontsize=12)

# Setting font size for ticks
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)

# Adding legend
plt.legend(loc='lower right', fontsize=8)

# Displaying the plot
plt.show()



all_metrics_test



