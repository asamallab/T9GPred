# T9GPred

T9GPred is a command-line based tool for predicting the T9SS components for user submitted protein fasta file of bacterial genomes.

## Table of Contents

- [Installation](#installation)
- [Requirements](#requirements)
- [Usage](#usage)
- [Example](#example)
- [Support](#support)
- [License](#license)

## Installation

Download and uncompress the T9GPred.zip to your project directory.

```sh
unzip T9GPred.zip
```
## Requirements

- Python3 
- Biopython 
- pandas 
- hmmsearch
- Path to the hmmsearch binary file ( update in CONFIG.ini )
- MODELS folder and CONFIG.ini file should be in the same directory as T9GPred_Secretome.py
- SignalP version 5.0
- Phobius version

Install the latest version of hmmer package for hmmsearch (http://hmmer.org/download.html).

## Usage

```sh
python3 T9GPred_Secreted.py -h
```

Shows the detailed usage of T9GPred_Secreted.py.

## Example 

```sh
python3 T9GPred_Secreted.py TEST/example.faa
```
Specify output directory (-d) and output file name (-o) :

```sh
python3 T9GPred.py TEST/example.faa -d TEST/ -o example_output.csv
```

Specify output directory (-d), output file name (-o) and keep all the intermediate files from hmmsearch :

```sh
python3 T9GPred.py TEST/example.faa -d TEST/ -o example_output.csv --keep
```

## Support

Please [open an issue](https://github.com/asamallab/T9GPred/issues/new) for support.

## License

Copyright (c) 2021 Areejit Samal.

Usage is provided under the GNU v3 License. See [LICENSE](https://github.com/asamallab/T9GPred/blob/main/LICENSE) for the full details.

