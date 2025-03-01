# Function to plot the overexpression and deletion shift scores. Plot only a limited number of genes.

import matplotlib.pyplot as plt
import numpy as np

def plot_shift_to_goal_end(data):
    """
    Plots the Shift_to_goal_end for gene deletion and overexpression.
    
    Parameters:
    - data: A dictionary containing 'Gene_name', 'delete', and 'overexpress' keys with corresponding values.
    """
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bar_width = 0.35
    index = np.arange(len(data["Gene_name"]))
    
    # Plotting the bars
    bars_delete = ax.bar(index, data["delete"], bar_width, label='Delete', color='r')
    bars_overexpress = ax.bar(index + bar_width, data["overexpress"], bar_width, label='Overexpress', color='b')
    
    # Adding labels, title, and legend
    ax.set_xlabel('Gene Name')
    ax.set_ylabel('Shift to Goal End')
    ax.set_title('Shift to Goal End for Gene Deletion and Overexpression')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(data["Gene_name"])
    ax.legend()
    
    # Displaying the plot
    plt.tight_layout()
    plt.show()

    
import csv

def create_data_dict_from_csv(file_path):
    """
    Reads a CSV file and creates a dictionary with gene names as keys
    and their respective 'delete' and 'overexpress' values for 'Shift_to_goal_end'.
    
    Parameters:
    - file_path: The path to the CSV file.
    
    Returns:
    - A dictionary with keys 'Gene_name', 'delete', and 'overexpress'.
    """
    data = {
        "Gene_name": [],
        "delete": [],
        "overexpress": []
    }
    
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            gene_name = row['Gene_name']
            shift_to_goal_end = float(row['Shift_to_goal_end'])
            
            if row['Pert_type'] == 'delete':
                data["Gene_name"].append(gene_name)
                data["delete"].append(shift_to_goal_end)
            elif row['Pert_type'] == 'overexpress':
                # Assuming gene names are already added by the 'delete' rows
                data["overexpress"].append(shift_to_goal_end)
    
    return data

# Mention the .csv file name here
file_path = ''         # the csv files will always have the same name called combined_stats.csv
data = create_data_dict_from_csv(file_path)

# Calling the function to plot the data
plot_shift_to_goal_end(data)
