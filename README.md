# LLM-Guided-Drug-Discovery

## Overview
Use of LLM model to identify the drug discovery. 

Human body is made of cells and cells consists of many genes. 
Whenever a person is affected by a disease, one or more of the 25k genes start behaving abnormally. 
To cure the disease, we need to find the correct set of abnormal genes and treat it using the corresponding chemical drugs.

But to find the correct genes out of 25k genes takes 4-7 years of time. 
Also, if the correct genes is not filtered in the initial steps, the drugs does not show efficacy in the clinical trials. This arise the need of a fast and measurable gene selection method. 

![Purpose](https://github.com/Vivekanand-Sahu/LLM-Guided-Drug-Discovery/blob/main/files/Screenshot%202025-02-28%20at%2010.11.54%E2%80%AFPM.png)

We can start with training the LLM model on a huge dataset consisting of cells from all the parts of the body. 
Then we can fine tune the LLM model to specialize on the disease for which we want to find a drug. 
For example, If we want to find the drug for Schizophrenia disease, Since I know that it is a brain disease. I will fine tune my model only on brain cells data.
Finally, we can perform in silico gene experiments to identify the drug target genes. 


![Process](https://github.com/Vivekanand-Sahu/LLM-Guided-Drug-Discovery/blob/main/files/Screenshot%202025-02-28%20at%2010.12.56%E2%80%AFPM.png)

LLMs are known for its ability to understand sequence data. 
It achieves this ability by the mechanism called MLM where it learns to predict the masked words using the context in which the neighboring words were used in other sentences.

Similarly, we can train a LLM model to learn the cell sequences consisting of genes to identify diseased and healthy cells.


![Pretraining](https://github.com/Vivekanand-Sahu/LLM-Guided-Drug-Discovery/blob/main/files/Screenshot%202025-02-28%20at%2010.12.18%E2%80%AFPM.png)

Here, is the functioning of the Fine Tuned Geneformer model. For every cell given as an input to the fine-tuned Geneformer, we obtain task-specific cell embeddings. 
These are high-dimensional vector representations of the cells that encapsulate essential gene features and relationships within the data. These embeddings are crucial for accurate cell classification and further analysis.

![training](https://github.com/Vivekanand-Sahu/LLM-Guided-Drug-Discovery/blob/main/files/Screenshot%202025-02-28%20at%2010.14.29%E2%80%AFPM.png)
In-silico gene perturbation allows us to simulate the effects of a dose on a gene and see it s corresponding effect on the disease state.
For example, if we delete gene 3 in a cell initially classified as healthy and this causes the cell to shift to a diseased state, it suggests that gene 3 plays a role in maintaining health and we can have a drug that will reduce the effect of gene 3. 
Conversely, if we overexpress gene 4 in a cell initially classified as diseased and this causes the cell to shift to a healthy state, it implies that having a drug that can enhance this gene activity could cure the disease. 


Applying this mechanism, we can build a framework to for any particular disease. 

![Experiments](https://github.com/Vivekanand-Sahu/LLM-Guided-Drug-Discovery/blob/main/files/Screenshot%202025-02-28%20at%2010.12.31%E2%80%AFPM.png)


### Steps
1. Clone the basic Geneformer repository:

    ```bash
git lfs install
git clone https://huggingface.co/ctheodoris/Geneformer
    ```

2. Navigate to the project directory:

    ```bash
    cd LLM-Guided-Drug-Discovery
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Load your dataset (format: `arrow`, `h5ad`, etc.).
2. Run the model with the following command:

    ```bash
    python training.py --input_file your_dataset.csv --output_file results.csv
    ```

3. Use the following example for invoking the custom features:

    ```bash
    python in_silico_perturbation.py --dataset your_dataset.csv --feature method_1/2/3
    ```



# Results

## Confusion matrix
<img src="https://github.com/Vivekanand-Sahu/LLM-Guided-Drug-Discovery/blob/main/Results/Screenshot%202025-02-28%20at%2010.19.37%E2%80%AFPM.png" width="500"/>

## AUC-ROC

<img src="https://github.com/Vivekanand-Sahu/LLM-Guided-Drug-Discovery/blob/main/Results/Screenshot%202025-02-28%20at%2010.19.54%E2%80%AFPM.png" width="500"/>

## UMAP

<img src="https://github.com/Vivekanand-Sahu/LLM-Guided-Drug-Discovery/blob/main/Results/Screenshot%202025-02-28%20at%2010.20.54%E2%80%AFPM.png" width="600"/>

## Perturbation Experiment on different genes

<img width="500" alt="image" src="https://github.com/user-attachments/assets/88897d60-73f7-4468-9010-e6ad55b01b9a" />

## Business impact

![Business-impact](https://github.com/Vivekanand-Sahu/LLM-Guided-Drug-Discovery/blob/main/Results/Screenshot%202025-02-28%20at%2010.14.39%E2%80%AFPM.png)



