import numpy as np
import pickle
from pathlib import Path

source_path = "./data/unirep/stability"
for path in Path(source_path).rglob('*.npz'):

    pickle_file = str(path).replace('npz', 'p')
    seq_dict = dict()

    data = np.load(path, allow_pickle=True)
    print(path)
    dups = set()
    dup_count = 0
    for id in data.files:
        if id in dups:
            dup_count += 1
            continue
        if id in seq_dict:
            del seq_dict[id]
            dups.add(id)
            dup_count += 1
            continue
        seq = data[id].item()['seq']
        if seq.shape[0] > 1000:
            print(seq.shape)
            continue
        seq_dict[id] = seq

    print("dups: ", dup_count)

    with open(pickle_file, 'wb') as f:
        pickle.dump(seq_dict, f)
