# Thesis

This repository contains the code and data pipeline for a Master's thesis focused on extracting, processing, and analyzing protein isoform data from UniProt, with an emphasis on alternative splicing events. The workflow includes web scraping and API usage to fetch data, processing and filtering protein and isoform information, performing sequence alignments, and analyzing structural metrics.

## Overview

The project builds a comprehensive pipeline that:
- Extracts alternative splicing data from UniProt.
- Filters and processes protein isoform information based on specific criteria (e.g., splicing length).
- Downloads FASTA sequence files for isoforms.
- Performs pairwise global sequence alignments using BLOSUM62.
- Analyzes structural comparison metrics (RMSD, GDT, LGA) from modeling tools.

## Pipeline Steps

1. **Data Extraction**
    - `data_extraction_step1.py`: 
      - Fetches alternative splicing data and isoform sequences from UniProt using the API.
      - Filters relevant protein and isoform data.
      - Downloads FASTA files for each isoform.

    - `step2.py`: 
      - Further filters proteins that have alternative splicing events of 4–25 amino acids.
      - Extracts related PDB IDs.

    - `step3.py`: 
      - Processes filtered data to extract and save isoform and protein IDs.

2. **Sequence Alignment**
    - `step4_alignment.py`: 
      - Performs global pairwise alignments for all isoforms of each protein using the BLOSUM62 matrix.
      - Combines FASTA files and outputs alignment results.

3. **Structural Analysis**
    - `analysis_step5.py`:
      - Reads results (RMSD, GDT, LGA) from Excel files.
      - Plots comparative graphs for various structural metrics across modeling tools (Modeller, PHYRE2, ITASSER).

## File Descriptions

- `data_extraction_step1.py`: Main script to extract and process UniProt data; downloads isoform sequences.
- `step2.py`: Filters for proteins with specific alternative splicing events.
- `step3.py`: Extracts isoform IDs and formats data for further processing.
- `step4_alignment.py`: Aligns protein isoform sequences and outputs results.
- `analysis_step5.py`: Visualizes structural similarity scores.
- `uniprot_data.json`, `filtered_protein.json`, etc.: Intermediate data files created during the pipeline.

## Requirements

- Python 3.x
- `requests`, `tqdm`, `pandas`, `seaborn`, `matplotlib`, `biopython`, `openpyxl`

Install with:
```bash
pip install requests tqdm pandas seaborn matplotlib biopython openpyxl
```

## Usage

1. **Extract Data:**
    ```bash
    python data_extraction_step1.py
    ```

2. **Filter and Process:**
    ```bash
    python step2.py
    python step3.py
    ```

3. **Align Sequences:**
    ```bash
    python step4_alignment.py
    ```

4. **Analyze Results:**
    ```bash
    python analysis_step5.py
    ```

## Notes

- Some paths in the scripts are absolute (e.g., `C:/Users/HP/...`). Update these paths as needed for your environment.
- Ensure the required directories (e.g., `fasta_files`, `selected_files`, `alignment`) exist or are created by the scripts.

## License

This repository is for academic and research purposes. Please cite appropriately if used in publications.

---

*For any questions or contributions, please open an issue or contact the repository owner.*
