# T9GPred

T9GPred is a computational tool for predicting the proteins secreted via T9SS from an input proteome.

<img src="Computational pipeline for secreted protein prediction.png">

## Folder Contents
- T9GPred_Secretome.py: Contains code for prediction of proteins secreted via T9SS from an input proteome
- MODELS: Contains 3 HMM profiles for CTD types genarted in this study 
- CONFIG.ini: Contains the path for HMM profiles and hmmsearch tool
- run_tools_n_parse.sh: Contains code to run SignalP, Phobius, TMHMM tool
- parse_signalp5.py: Contains code to parse the output from signalP
- parse_tmhmm.py: Contains code to parse the output from tmhmm
- Example.fasta: Contains the proteome of an example <i>Bacteroidetes</i> strain in fasta format
- combined_102.fasta: Contains the sequences of 102 experimentally characterized proteins secreted via T9SS

## Requirements

- python3 
- SignalP version 5.0 (https://services.healthtech.dtu.dk/services/SignalP-5.0/)
- Phobius version 1.01 (https://phobius.sbc.su.se/)
- TMHMM version 2.0 (https://services.healthtech.dtu.dk/services/TMHMM-2.0/)
- hmmsearch (http://hmmer.org/download.html)
- Path to the hmmsearch binary file (update in CONFIG.ini)

Python Packages:
- Biopython 
- pandas

MODELS folder and CONFIG.ini file should be in the same directory as T9GPred_Secretome.py



Please provide the absolute path of SignalP, Phobius and TMHMM in run_tools_n_parse.sh script file

## Usage

```sh
python3 T9GPred_Secretome.py -h
```

Shows the detailed usage of T9GPred_Secretome.py.

## Example 

```sh
python3 T9GPred_Secretome.py Example.fasta
```
Specify output directory (-d) and output file name (-o) :

```sh
python3 T9GPred_Secretome.py Example.fasta -d TEST/ -o Example_output.csv
```

Specify output directory (-d), output file name (-o) and keep all the intermediate files from hmmsearch :

```sh
python3 T9GPred_Secretome.py Example.fasta -d TEST/ -o Example_output.csv --keep
```

## Support

Please [open an issue](https://github.com/asamallab/T9GPred/issues/new) for support.


