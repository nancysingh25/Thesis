"""
Function calculates the pairwise alignment globally and uses the BLOSUM62 matrix and stores the output in fasta file
for every protein.
"""
import json
import traceback
from Bio import SeqIO
import os
from Bio import pairwise2
from Bio.SubsMat import MatrixInfo as matlist
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from itertools import combinations

#function to read the protein data file
def read_id_data() -> dict or None:
    try:
        f = open('selected_data.json', "r")
        response_data = json.loads(f.read())

        return response_data
    except:
        traceback.print_exc()


matrix = matlist.blosum62


# Callback function for the BLOSUM62 matrix
def matrix_get(aa1, aa2):
    if (aa1, aa2) in matrix:
        val = matrix[(aa1, aa2)]
    elif (aa2, aa1) in matrix:
        val = matrix[(aa2, aa1)]
    else:
        val = 0
    return val

#function which does the pairwise alignemnt
def align(pair):
    # takes the alignment parameters and clls the global alignment
    alignment = pairwise2.align.globalcs(pair[0].seq, pair[1].seq, matrix_get, -10, -0.5)[0]
    # returns the alignment for each pair
    yield SeqRecord(Seq(alignment[0]), id=pair[0].id, name=pair[0].name,
                    description=f"Score={alignment[2]}")
    yield SeqRecord(Seq(alignment[1]), id=pair[1].id, name=pair[1].name,
                    description=f"Score={alignment[2]}")

#function to writes the alignment output in fasta files with the primary accession number of protein the file name
def out_alignment(data):
    for key in data.keys():
        #opening the file with primary accesion number as the file name
        with open(f"C:/Users/HP/Documents/thesis/selected_files/alignment/output_{key}.fasta", "w") as output:
            size = os.path.getsize(f"C:/Users/HP/Documents/thesis/selected_files/{key}_combined.fasta")
            if size < 100000:
                #so that every protein align with each other only once
                for pair in combinations(
                        SeqIO.parse(f"C:/Users/HP/Documents/thesis/combined_fasta/{key}_combined.fasta", "fasta"), 2):
                    SeqIO.write(align(pair), output, "fasta") #wriitng the output to the output fasta file as seqrRecord.

#function to combining fasta files in one for isoform of the same protein
def combining_files(data):
    for key, values in data.items():
        #checks if the fasta file with the combined name for the protein exist in the folder or not
        FILE_NAME = f"C:/Users/HP/Documents/thesis/selected_files/{key}_combined.fasta"
        #if file does not exist in the folder it opens the file with the name and write fasta sequnecs to it
        with open(FILE_NAME, 'a+') as output_fas:
            for value in values:
                if os.path.exists(f"./fasta_files/{value}.fasta"):
                    output_fas.write(open(f"./fasta_files/{value}.fasta", "r").read())
                    output_fas.write("\n")


def main() -> None:
    try:

        data = read_id_data()
        # combining_files(data)
        out_alignment(data)
    except:
        traceback.print_exc()


if __name__ == '__main__':
    main()
