#this code extract the protein Uniprot ids which only have alternative splicing length of 4-25 aa

from collections import defaultdict
import traceback
import requests
import json
import os

#function to extract the data of proteins with alternative splicing events 4-25 aa
def pdb_data(protein_data) -> dict:
    pdb_data = defaultdict(list)
    try:
        for protein in protein_data:
            accession_id = protein["primaryAccession"]

            # extract the PDB ids.
            if "features" in protein.keys():

                for a_s in protein["features"]: #features stored the alternative splicing sequnece infromation
                    if a_s["type"] == 'Alternative sequence':
                        if "location" in a_s.keys():

                            if a_s['location']['start'] and a_s['location']['end']: #based on the difference of alternative splicng start and end positon
                                #difference is calculated
                                start = a_s['location']['start']['value']
                                end = a_s['location']['end']['value']
                                difference = end - start
                                if difference in range(1, 25): #if the difference is in the range of 4-25 it was stored in pdb_data dic
                                    pdb_data[accession_id]
    except:
        traceback.print_exc()
    return pdb_data

#Function to check if the protein data file is available, if not it call the uniprot API to extract the alternative splicng
#information.
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
            pdb_id = pdb_data(protein_data["results"])

            with open("./alternative_splicing_event.json", "w") as fh:
                json.dump(pdb_id, fh, indent=4)


    except:
        traceback.print_exc()


if __name__ == '__main__':
    main()
