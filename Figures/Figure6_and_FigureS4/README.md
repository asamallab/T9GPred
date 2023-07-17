# Figure 6

This folder contains the R scripts to generate the Figure 6 and Figure S4 in the manuscript.

## Requirements
- R version 4.2.1
- RStudio 2022.12.0+353 (https://posit.co/products/open-source/rstudio/)

R packages:
- dplyr
- ggplot2
- readr
- ggpubr
- rstatix

## Folder Contents

- Sequence_length_CTD_statistics_402.txt: Contains the information on the sequence length and number ratio of the predicted secreted proteins of different CTD types for 402 <i>Bacteroidetes</i> strains predicted to have T9SS.
- Sequence_length_CTD_statistics_629.txt: Contains the information on the sequence length and number ratio of the predicted secreted proteins of different CTD types for 629 strains identified from ~34,000 completely sequenced bacteria.
- Sequence_length_comparison.R: Contains the code to plot the sequence length comparison between the gliding and non-gliding <i>Bacteroidetes</i> strains.
- Secreted_protein_comparison.R: Contains the code to plot the distributions of predicted secreted proteins (ratio) between gliding and non-gliding <i>Bacteroidetes</i> strains.

## Usage

Open the .R files using RStudio.
The RScripts contain inline comments explaining each aspect of the code.
- To generate Figure 6, use Sequence_length_CTD_statistics_402.txt as the input file.
- To generate Figure S4, use Sequence_length_CTD_statistics_629.txt as the input file.

