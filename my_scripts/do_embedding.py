import os
import datasets as ds
import elmo.seqvec_embedder as emb
from pathlib import Path
import pickle
import numpy as np
import tape.training as tt

SOURCE_DATA_PATH = "./data/raw"

# # secondary_structure
# # sequence to sequence, datasets: ['train', 'valid', 'casp12', 'ts115', 'cb513']
# SSD = ds.SecondaryStructureDataset(SOURCE_DATA_PATH, 'train')

# # remote_homology
# # multiclass y ∈ {1,...,1195}, datasets: ['train', 'valid', 'test_fold_holdout', 'test_family_holdout', 'test_superfamily_holdout']
# RHD = ds.RemoteHomologyDataset(SOURCE_DATA_PATH, 'train') 

# # stability
# # regression, datasets: ['train', 'valid', 'test']
# SD = ds.StabilityDataset(SOURCE_DATA_PATH, 'train')

# # fluorescence
# # regression, datasets: ['train', 'valid', 'test']
# FD = ds.FluorescenceDataset(SOURCE_DATA_PATH, 'train')


# tasks = ['secondary_structure', 'remote_homology', 'stability', 'fluorescence']
tasks = ['remote_homology']
splits = ['train', 'valid', 'test']

def data_set_to_seq_dict(dataset: ds.Dataset, id_prepend=''):
    seq_dict = dict()
    for index in range(len(dataset)):
        amino_acids, token_ids, input_mask, fold_label = dataset[index]
        seq_dict[id_prepend+str(index)] = amino_acids
    
    return seq_dict

def elmo_emb_dataset(task: str, split: str):

    dataset = ds.Dataset()
    if task == "secondary_structure": dataset = ds.SecondaryStructureDataset(SOURCE_DATA_PATH, split)
    elif task == "remote_homology": dataset = ds.RemoteHomologyDataset(SOURCE_DATA_PATH, split)
    elif task == "stability": dataset = ds.StabilityDataset(SOURCE_DATA_PATH, split)
    elif task == "fluorescence": dataset = ds.FluorescenceDataset(SOURCE_DATA_PATH, split)
    else: 
        print("no data set for task " + task)
        return 

    # set up file
    filename = task + "_" + split
    filepath = "./elmo/" + task + "/" + filename + ".p"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # do emb
    print("Embedding dataset " + filename)
    seq_dict = data_set_to_seq_dict(dataset)
    emb_dict = emb.get_embeddings(seq_dict, verbose=True)
    
    print('Writing embeddings to: {}'.format(filepath))
    with open(filepath, 'wb') as f:
        pickle.dump(emb_dict, f)

def elmo_emb_all_datasets():
    for task in tasks:
        for split in splits:
            elmo_emb_dataset(task, split)



def unirep_emb_all_datasets():
    for task in tasks:
        for split in splits:
            print(task, split)
            model = 'unirep'
            input_file = SOURCE_DATA_PATH + "/" + task + "/" + task + "_" + split + ".fasta"
            output_file = model + "/" + task + "/" + task + "_" + split + ".npz"
            pretained = 'babbler-1900'
            tokenizer = 'unirep'
            tt.run_embed(model, input_file, output_file, pretained,
                         tokenizer=tokenizer, full_sequence_embed=True)


def transformer_emb_all_datasets():
    print("run transformer_emb_all_datasets")
    for task in tasks:
        for split in splits:
            print(task, split)
            model = 'transformer'
            input_file = SOURCE_DATA_PATH + "/" + task + "/" + task + "_" + split + ".fasta"
            output_file = model + "/" + task + "/" + task + "_" + split + ".npz"
            pretained = 'bert-base'
            tt.run_embed(model, input_file, output_file, pretained, full_sequence_embed=True)


if __name__ == "__main__":
    transformer_emb_all_datasets()
