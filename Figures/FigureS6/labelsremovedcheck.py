#check log files from cgview for label removal
#cgview's stdout & stderror have to redirected to a log file with the same name as for svg file 
#example: java -jar -Xmx1500m ./CGView/cgview.jar -i 485917.6.PATRIC_modified_hit_matrix_genome_coord_485917.6_Pedobacter-heparinus-DSM-2366_NC-013061_5167383_cgview.xml -o test_2Aug21.svg -f svg -h test_2Aug21.html > test_2Aug21.log 2>&1
# The log file is the input for this code

import sys

for i in open(sys.argv[1]):
    if i.strip() != 'The map has been drawn.':
        if 'labels were removed' in i:
            num = int(i.split(' ')[0])
            if num != 0:
                print ('{}: Warning -> {} labels removed!!!'.format(sys.argv[1], str(num)))
            elif num == 0:
                continue
        else:
            continue
    else:
        break
