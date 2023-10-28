"""
This code extract the alternative splicing data from Uniprot. It also fetch the
fasta sequence file from the Uniprot API for the alternative isoforms
"""

from collections import defaultdict
from tqdm import tqdm

import traceback
import requests
import json
import os

#this function is used to merge the two dictionaris for PDB ids and isoforms ids
def merge_defaultdicts(d, d1):
    for k, v in d1.items():
        if k in d:
            d[k].append(d1[k])
        else:
            d[k] = d1[k]
    return d

#This function calls the Uniprot id and based on the primary accession id it fetch the sequence of the isoform
# and writes in a fasta file

def fetch_fasta(isoform_id) -> bool:
    try:
        response = requests.get("https://rest.uniprot.org/uniprotkb/%s.fasta" % isoform_id).text
        if response:
            with open("./fasta_files/%s.fasta" % isoform_id, "w") as fh:
                fh.write(response)
        else:
            return False
    except:
        traceback.print_exc()
    return True

#this function read the isoform data and extraxt the isoform id from it and return the ids as a isoform list
def get_protein_isoform_ids(isoform_data) -> list:
    isoforms = []
    try:
        for entry in isoform_data:
            isoforms.extend(entry["isoformIds"])
    except:
        traceback.print_exc()
    return isoforms

#This function calls the fetch_fasta fucnction and get_protein_isoform_ids first it checks if the isoform id is in the
# list which is returnde from fet_protein_ids and then it extract the file for the isoform
def extract_fasta_files(protein_isoforms) -> None:
    missing_sequences = []
    try:
        with tqdm(total=len(protein_isoforms.keys())) as pbar:
            for accession_id, isoform_data in protein_isoforms.items():
                isoforms = get_protein_isoform_ids(isoform_data)
                for isoform_id in isoforms:
                    #if isoform_id.endswith("-1"): isoform_id = accession_id
                    if not fetch_fasta(isoform_id):
                        missing_sequences.append(isoform_id)
                pbar.update(1)
        if missing_sequences:
            print("Sequences for %s isoforms are missing!" % len(missing_sequences))
            print("FASTA file for %s total isoforms could not be successfully extracted!" % len(missing_sequences))
            with open("./missing_isoform_sequences_test.json", "w") as fh:
                json.dump(missing_sequences, fh, indent=4)
    except:
        traceback.print_exc()

#this function extract the PDB data related to the isoforms based on primary accession number
def pdb_data(protein_data) -> dict:
    pdb_data = defaultdict(list)
    try:
        for protein in protein_data:
            accession_id = protein["primaryAccession"]

            # extract the PDB ids.
            if "uniProtKBCrossReferences" in protein.keys():
                for pdb in protein["uniProtKBCrossReferences"]:
                    if "database" in pdb.keys() and pdb["database"] == 'PDB':
                        pdb_data[accession_id].append(pdb)
    except:
        traceback.print_exc()
    return pdb_data

#this function filterred data based on primary accession number
# and then only isoform ids are stored in the dictionary in the end.
def filter_relevant_data(protein_data) -> dict:
    filtered_data = defaultdict(list)
    try:
        for protein in protein_data:
            accession_id = protein["primaryAccession"]

            # For now, we only filter isoforms. Similarly, other important information could be extracted.
            if "comments" in protein.keys():
                for comment in protein["comments"]:
                    if "isoforms" in comment.keys():
                        filtered_data[accession_id].extend(comment["isoforms"])
    except:
        traceback.print_exc()
    return filtered_data

#extracting the data of alternative splicing from Uniprot if protein_data file doesnot exists
#it call the UNiprot API to get the information and creates a protein_data file
def get_protein_data() -> dict or None:
    response_data = None
    try:
        if os.path.exists("./uniprot_data.json"):
            response_data = json.loads(open("./uniprot_data.json").read())
        else:
            response = requests.get(
                "https://rest.uniprot.org/uniprotkb/stream?format=json&query=var_seq%20AND%20%28model_organism%3A9606%29%20AND%20%28proteins_with%3A1%29%20AND%20%28proteins_with%3A5%29")
            if response.text:
                response_data = json.loads(response.text)

                # Storing this for backup purposes to use it later when needed.
                with open("./uniprot_data.json", "w") as fh:
                    json.dump(response_data, fh, indent=4)
            else:
                print("API Endpoint failed!")

        return response_data
    except:
        traceback.print_exc()


def main() -> None:
    try:
        print("Extracting initial protein data (var_seq) from UNIPROT...")
        protein_data = get_protein_data()
        if protein_data and "results" in protein_data.keys():
            print("Proteins successfully fetched, extracting isoform ids now...")
            filtered_protein_data = filter_relevant_data(protein_data["results"])
            pdb_id = pdb_data(protein_data["results"])
            relevant_data = merge_defaultdicts(filtered_protein_data, pdb_id)
            if relevant_data:
                with open("./filtered_protein.json", "w") as fh:
                    json.dump(filtered_protein_data, fh, indent=4)
            print("All set! Let's download FASTA Sequence files for %s Proteins." % (len(filtered_protein_data.keys())))
            extract_fasta_files(filtered_protein_data)
    except:
        traceback.print_exc()


if __name__ == '__main__':
    main()
