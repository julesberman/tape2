from tqdm import tqdm
from Bio.SeqIO.FastaIO import Seq, SeqRecord
from tape.datasets import LMDBDataset
from pathlib import Path
import math
import pickle

lmdbdir = './data/raw'

for path in Path(lmdbdir).rglob('*.lmdb'):
    dataset = LMDBDataset(path)
    filepath = str(path).replace('lmdb', 'p')
    seq_dict = dict()
    id_fill = math.ceil(math.log10(len(dataset)))
    for i, element in enumerate(tqdm(dataset)):
        id_ = element.get('id', str(i).zfill(id_fill))
        if isinstance(id_, bytes):
            id_ = id_.decode()
        primary = element['primary']
        seq_dict[id_] = primary
      data = np.load(path_to_file, allow_pickle=True)      
    with open(filepath, 'wb') as f:
        pickle.dump(seq_dict, f)
