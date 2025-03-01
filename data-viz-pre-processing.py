# data pre-processing

import anndata
import scanpy as sc
import matplotlib.pyplot as plt


# Select the correct dataset
adata = anndata.read_h5ad('/data-hpcwn-pnl03/FXG/Geneformer_archive/Data/scRNA_dataset/Previous_datasets/BATIUK_SCZ.h5ad')

adata.var

print(list(adata.obs["orig.ident"].unique()))


import matplotlib.pyplot as plt
import pandas as pd

# Get the unique identifiers
unique_ids = adata.obs["orig.ident"].unique()

# Initialize a list to store the counts
count_data = []


# --------------------------------------------------------------------------------------------------

# Iterate over the unique identifiers and collect the counts
for i in unique_ids:
    counts = adata.obs[adata.obs["orig.ident"] == i]["condition"].value_counts()
    count_data.append(counts)

# Convert the list of series into a DataFrame
df_counts = pd.DataFrame(count_data, index=unique_ids).fillna(0)

# Plotting
ax = df_counts.plot(kind='bar', stacked=False, color=['blue', 'orange'], figsize=(10, 6))

# Adding labels and title
ax.set_xlabel('orig.ident')
ax.set_ylabel('Cell Count')
ax.set_title('Cell Counts for Ctrl and Scz Conditions')

# Adding a legend
ax.legend(title='Condition')

# Display the plot
plt.show()


# --------------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt

def plot_condition_counts(adata, type):
    """
    Plots the counts of 'Ctrl' and 'Scz' conditions for each reading in the series.

    Parameters:
    adata : AnnData
        Annotated data matrix.
    type : str
        Column name in adata.obs to group by.
    """
    # Prepare data for plotting
    ctrl_counts = []
    scz_counts = []
    series = list(adata.obs[type].unique())
    
    for a in series:
        counts = adata.obs[adata.obs[type] == a]["condition"].value_counts()
        #print(counts)
        ctrl_counts.append(counts.get("Ctrl", 0))
        scz_counts.append(counts.get("Scz", 0))
    
    # Plot the data
    x = range(len(series))  # X-axis: indices of readings
    
    plt.figure(figsize=(12, 8))
    
    bar_width = 0.4
    overlap_offset = 0.2
    
    bars_ctrl = plt.bar(x, ctrl_counts, width=bar_width, label='Ctrl', align='center', color='blue')
    bars_scz = plt.bar([i + overlap_offset for i in x], scz_counts, width=bar_width, label='Scz', align='center', color='red')
    
    # Add text annotations to each bar
    for bar in bars_ctrl:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, int(yval), va='bottom')  # Adjust va for position
    
    for bar in bars_scz:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, int(yval), va='bottom')  # Adjust va for position
    
    plt.xlabel('Readings')
    plt.ylabel('Number of cells')
    plt.title('Counts of Ctrl and Scz conditions for each reading')
    plt.xticks([i + overlap_offset / 2 for i in x], series, rotation='vertical')
    plt.yscale("log")
    plt.legend()
    
    plt.tight_layout()
    plt.show()

plot_condition_counts(adata, "cellTypeL2")
plot_condition_counts(adata, "cellType")
#plot_condition_counts(adata, "orig.ident")

# --------------------------------------------------------------------------------------------------


# Plot UMAP
sc.pl.umap(adata, color=['condition'], show=True)  # Replace 'cell_type' with your actual annotation

sc.pl.umap(adata, color=['cellType'], show=True)  # Replace 'cell_type' with your actual annotation

sc.pl.umap(adata, color=['cellTypeL2'], show=True)  # Replace 'cell_type' with your actual annotation

sc.pl.umap(adata, color=['orig.ident'], show=True)  # Replace 'cell_type' with your actual annotation

splatter2 = adata[adata.obs["cellTypeL2"].isin(["GLUT neurons","GABA neurons"])]

sc.pl.umap(splatter2, color=['orig.ident'], show=True)

splatter2 = adata[adata.obs["condition"].isin(["Ctrl"])]

sc.pl.umap(splatter2, color=['orig.ident'], show=True)

splatter2 = adata[adata.obs["condition"].isin(["Scz"])]

sc.pl.umap(splatter2, color=['orig.ident'], show=True)


# --------------------------------------------------------------------------------------------------

