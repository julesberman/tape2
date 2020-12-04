import argparse
import math
from tqdm import tqdm
from Bio.SeqIO.FastaIO import Seq, SeqRecord
from tape.datasets import LMDBDataset
from pathlib import Path
parser = argparse.ArgumentParser(description='Convert an lmdb file into a fasta file')
parser.add_argument('lmdbdir', type=str, help='The dir with lmdb files to convert')
args = parser.parse_args()


for path in Path(args.lmdbdir).rglob('*.lmdb'):
    dataset = LMDBDataset(path)
    id_fill = math.ceil(math.log10(len(dataset)))
    print(id_fill)
    fastafile = str(path).replace('lmdb', 'fasta')
    with open(fastafile, 'w') as outfile:
        for i, element in enumerate(tqdm(dataset)):
            id_ = element.get('id', str(i).zfill(id_fill))
            if isinstance(id_, bytes):
                id_ = id_.decode()

            primary = element['primary']
            seq = Seq(primary)
            record = SeqRecord(seq, id_, description=path.name.replace('.lmdb', ''))
            outfile.write(record.format('fasta'))


