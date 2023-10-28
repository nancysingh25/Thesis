"""
This code reads the filtered_protein_data.json file and ectract only the isofrom id and protein id
store the information in new file namin gprotein data file
"""

from collections import defaultdict
import traceback
import json


# function to read the filtered rpotein_Data_file
def get_protein_data() -> dict or None:
    try:
        f = open('filtered_protein_data.json', "r")
        response_data = json.loads(f.read())

        return response_data
    except:
        traceback.print_exc()


# function to extract the isoform and pdb ids
def id_data() -> dict:
    data = defaultdict(list)
    protein_data = get_protein_data()
    try:
        with open("./protein_data.json", "w") as fh: #opening the file to write the extracted information
            for key, values in protein_data.items():
                if isinstance(values, list):
                    for entry in values:
                        if isinstance(entry, dict) and "isoformIds" in entry.keys(): #checks if the isoformIDS exist in the dict
                            data[key].extend(entry["isoformIds"])
                        elif isinstance(entry, list):
                            for db in entry: #checks if the db key exists in dict
                                if isinstance(db, dict) and "database" in db.keys() and "id" in db.keys():
                                    data[key].append(db["id"]) #adding the ids at the end of the dict
            json.dump(data, fh, indent=4)
    except:
        traceback.print_exc()
    # return data


def main() -> None:
    try:
        id_data()

    except:
        traceback.print_exc()


if __name__ == '__main__':
    main()
