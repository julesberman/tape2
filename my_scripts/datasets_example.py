import numpy as np
import os
import pickle
import datasets as ds
def read_dataset(model: str, task: str, split: str,  basepath='./data'):
    """
        Reads a data file -> return dict from id -> representation (which will vary based on model)
        PARAMS
            basepath: path to the data folder 
            model = ['elmo', 'unirep', 'transformer', 'raw', 'label']
            split = ['train', 'valid', 'test']
            task = ['secondary_structure', 'remote_homology', 'stability', 'fluorescence']
    """

    path_to_file = f'{basepath}/{model}/{task}/{task}_{split}.p'
    data = np.load(path_to_file, allow_pickle=True)
    
    return data

# elmo_data = read_dataset('elmo', 'remote_homology', 'test')
# raw_data = read_dataset('raw', 'remote_homology', 'test')

def get_dataset(task, path, split):
    if task == 'secondary_structure': return ds.SecondaryStructureDataset(path, split)
    if task == 'remote_homology': return ds.RemoteHomologyDataset(path, split)
    if task == 'stability': return ds.StabilityDataset(path, split)
    if task == 'fluorescence': return ds.FluorescenceDataset(path, split)


# RHD = ds.RemoteHomologyDataset(SOURCE_DATA_PATH, 'train') 
# SD = ds.StabilityDataset(SOURCE_DATA_PATH, 'train')
# FD = ds.FluorescenceDataset(SOURCE_DATA_PATH, 'train')
# SSD = ds.SecondaryStructureDataset(SOURCE_DATA_PATH, 'train')

def rewrite_data(task):
    for split in ['train', 'valid', 'test']:
        print(task + " " + split)
        elmo_data = read_dataset('elmo', task, split)
        dataset = get_dataset(task, './data/raw', split)
        print(len(dataset))
        print(len(elmo_data))
        new_elmo_dict = dict()
        label_dict = dict()
        raw_dict = dict()

        dup_counter = 0 
        dups = set()
        for index in range(len(dataset)):

            amino_acids, token_ids, input_mask, label, id_ = dataset[index]
            id_str = id_.decode("utf-8") 
            
            # if there is a duplicate, just delete and ignore
            if id_str in dups:
                dup_counter += 1
                continue
            if id_str in new_elmo_dict:
                dups.add(id_str)
                dup_counter += 1
                del new_elmo_dict[id_str]
                del label_dict[id_str]
                del raw_dict[id_str]
                continue

            try:
                elmo_seq = elmo_data[str(index)]
            except:
                print("excpet on index: " + str(index))
                print(len(amino_acids))
                continue

            if(elmo_seq.shape[0] != len(amino_acids)):
                print(str(index) + " err on " + k)
                print(elmo_seq.shape, len(raw_seq))

            label_dict[id_str] = label
            raw_dict[id_str] = amino_acids      
            new_elmo_dict[id_str] = elmo_seq

        print("dups: ", dup_counter)
        # write elmo data
        filename = f'./data/newelmo/{task}/{task}_{split}.p'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "wb") as f:
            pickle.dump(new_elmo_dict, f)

        # write raw data
        filename = f'./data/newraw/{task}/{task}_{split}.p'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "wb") as f:
            pickle.dump(raw_dict, f)

        # write label data
        filename = f'./data/label/{task}/{task}_{split}.p'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "wb") as f:
            pickle.dump(label_dict, f)



# # SANITY CHECK
def sanity_check(task, model):
    for split in ['train', 'valid', 'test']:
        print("SANITY CHECK")
        print(model + " " + task + " " + split)
        dataset = get_dataset(task, './data/raw', split)
        elmo_data = read_dataset(model, task, split)
        label_data = read_dataset('label', task, split)
        raw_data = read_dataset('newraw', task, split)

        key_errs = 0
        for index in range(len(dataset)):
            amino_acids, token_ids, input_mask, label, key_bytes = dataset[index]
            key = key_bytes.decode("utf-8") 

            try:
                elmo_seq = elmo_data[key]
            except:
                key_errs += 1
                print("except on elmo_data: ", key)
                continue

            emb_shape = elmo_seq.shape[0]
            # just for unirep
            if model == 'unirep':
                emb_shape = elmo_seq.shape[0] - 2

            if emb_shape != len(amino_acids):
                print(key)
                print('elmo_seq.shape[0] != len(amino_acids)')
                print(elmo_seq.shape[0], len(amino_acids))

            if emb_shape != len(raw_data[key]):
                print(key)
                print('elmo_seq.shape[0] != len(amino_acids)')
                print(elmo_seq.shape[0], len(amino_acids))

            if hasattr(label, "__len__"):
                cond = np.array_equal(label_data[key], label)
            else:
                cond = label_data[key] == label
            if not cond:
                print('label_data[key] != label')
                print(label_data[key], label)
        
        print("key errs ", key_errs)


task = 'stability'

# rewrite_data(task)
sanity_check(task, 'unirep')
sanity_check(task, 'newelmo')