This folder contains the code to generate Figure S4 in the manuscript.

## Folder Contents

- Example_T9SS_Gliding_motility_hits.csv: Contains the predicted protein components associated with T9SS and gliding motility for an example Bacteroidetes
- Example.gff: Contains the genome coordinates of all the coding sequences for the example Bacteroidetes
- Map_hits_to_gff.py: Contains the code to map proteins to their genome coordinates
- prepare_xml_for_cgview.py: Contains the code to convert .csv file to .xml format
- labelsremovedcheck.py: Contains the code which checks for any protein labels being removed by CGView
 
## Requirements

- python3
- CGView (https://github.com/paulstothard/cgview/tree/master/bin)

## Usage

Generate the genome coordinates of the predicted protein components

```sh
python3 Map_hits_to_gff.py Example_T9SS_Gliding_motility_hits.csv Example.gff
```

Convert the .csv file (File.csv) to .xml (File.xml) format which will be the input for CGView

```sh
python3 prepare_xml_for_cgview.py File.csv
```

Make a copy of the generated .xml file (File.xml) and remove the organism details (File_notitle.xml)

Run the CGView tool and generate the circular plots

```sh
java -jar -Xmx1500m CGView/cgview.jar -i File.xml -x 1,20 -s 20x_1 -e T > 20x_1.log 2>&1
java -jar -Xmx1500m CGView/cgview.jar -i File_notitle.xml -x 1,20 -s 20x_2 -e T > 20x_2.log 2>&1
cd 20x_1
mv png png_org
cp -pr ../20x_2/png .
cd png
rm 1_1.png
cp ../png_org/1_1.png .
cd ../../
python3 labelsremovedcheck.py 20x_1.log

```

