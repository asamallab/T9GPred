# T9GPred

T9GPred is a computational tool for predicting protein components associated with T9SS and gliding motility in Bacteroidetes.

## Folder Contents
- T9GPred.py: Contains code for prediction of T9SS and gliding motility in Bacteroidetes.
- MODELS: Contains 28 HMM profiles generated in this study. 
- CONFIG.ini: Contains the path for HMM profiles and HMMsearch tool.
- Example.fasta: Contains the proteome of an example Bacteroidetes in fasta format.

## Requirements

- Python3
- hmmsearch (http://hmmer.org/download.html)
- Path to the hmmsearch binary file (update in CONFIG.ini)
- MODELS folder and CONFIG.ini file should be in the same directory as T9GPred.py.

## Usage

```sh
python3 T9GPred.py -h
```

Shows the detailed usage of T9GPred.

## Example 

```sh
python3 T9GPred.py Example.fasta
```
Specify output directory (-d) and output file name (-o) :

```sh
python3 T9GPred.py Example.fasta -d TEST/ -o Example_output.csv
```

Specify output directory (-d), output file name (-o) and keep all the intermediate files from hmmsearch :

```sh
python3 T9GPred.py Example.fasta -d TEST/ -o Example_output.csv --keep
```

## Support

Please [open an issue](https://github.com/asamallab/T9GPred/issues/new) for support.


