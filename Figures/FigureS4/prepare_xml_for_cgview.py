
import sys

seq_length = sys.argv[1].strip().split('_')[-1].replace('.csv','')
accn = sys.argv[1].strip().split('_')[-2].replace('-','_')
oname = sys.argv[1].strip().split('_')[-3].replace('-',' ')
ptid = sys.argv[1].strip().split('_')[-4]

print (ptid, oname, accn, seq_length)

line = []
line.append('<?xml version="1.0" encoding="ISO-8859-1"?>\n')
line.append('<cgview backboneRadius="300" backboneColor="rgb(102,102,102)" backboneThickness="3" featureSlotSpacing="medium" labelLineLength="medium" labelPlacementQuality="better" labelLineThickness="1" rulerPadding="14" tickThickness="2" shortTickThickness="1" arrowheadLength="16" rulerFont="SansSerif, plain, 8" rulerFontColor="rgb(0,0,0)" labelFont="SansSerif, bold-italic, 11" isLinear="false" minimumFeatureLength="0.2" sequenceLength="{}" height="1000" width="1000" globalLabel="true" moveInnerLabelsToOuter="true" featureThickness="8" tickLength="5" useInnerLabels="true" shortTickColor="rgb(30,30,50)" longTickColor="rgb(30,30,50)" zeroTickColor="rgb(255,100,150)" showBorder="true" borderColor="black" backgroundColor="white" tickDensity="0.8">\n\n\n'.format(seq_length))

line.append('<legend position="middle-center" backgroundOpacity="0.8">\n')
line.append('<legendItem textAlignment="center" font="SansSerif, bold-italic, 15" text="{}" />\n'.format(' '.join(oname.split(' ')[:2])))
line.append('<legendItem textAlignment="center" font="SansSerif, bold, 15" text="{}" />\n'.format(' '.join(oname.split(' ')[2:])))
line.append('</legend>\n\n\n')

line.append('<legend position="upper-left" font="SansSerif, plain, 15" backgroundOpacity="0.8">\n')
line.append('<legendItem text="Accession: {}" />\n'.format(accn))
line.append('<legendItem text="Length: {} bp" />\n'.format(seq_length))
line.append('</legend>\n\n\n')

line.append('<legend position="upper-right" textAlignment="left" backgroundOpacity="0.8" font="SansSerif, plain, 15">\n')
line.append('<legendItem text="T9SS mandatory components" drawSwatch="true" swatchColor="rgb(66,30,34)" />\n')
line.append('<legendItem text="Gliding motility mandatory components" drawSwatch="true" swatchColor="rgb(239,163,85)" />\n')
line.append('<legendItem text="T9SS/Gliding motility accessory components" drawSwatch="true" swatchColor="rgb(88,166,166)" />\n')
line.append('</legend>\n\n\n')

pink = ['GldK', 'GldL', 'GldM', 'GldN', 'SprA', 'SprE']
green = ['GldB', 'GldD', 'GldH', 'GldJ', 'SprT']

fdict={
        'forward':[],
        'reverse':[]
        }
for i in open(sys.argv[1]):
    if 'T9SS components' in i:
        continue
    else:
        tmp = i.strip().split('\t')

        strand_sign = tmp[-1].strip()
        if strand_sign == '+':
            strand = 'forward'
        elif strand_sign == '-':
            strand = 'reverse'
        else:
            print ('Error', i)

        start = tmp[-3].strip()
        stop = tmp[-2].strip()

        label = tmp[0].strip().replace(' ','')
        if "/" in label:
            if label == 'GldM/PorM':
                label = 'GldM'
            if label == 'GldN/PorN':
                label = 'GldN'
            if label == 'SprA/Sov':
                label = 'SprA'
            if label == 'SprT/PorT':
                label = 'SprT'
            if label == 'SprF/PorP/CHU_0170':
                label = 'PorP'
            if label == 'GldK/PorK':
                label = 'GldK'
            if label == 'SprE/PorW':
                label = 'SprE'
            if label == 'GldL/PorL':
                label = 'GldL'

        if label in pink:
            fdict[strand].append([strand, start, stop, label,'rgb(66,30,34)'])
        elif label in green:
            fdict[strand].append([strand, start, stop, label,'rgb(239,163,85))'])
        else:
            fdict[strand].append([strand, start, stop, label,'rgb(88,166,166)'])

line.append('<featureSlot showShading="true" strand="direct">\n')
for i in fdict['forward']:
    line.append('<feature color="{}" decoration="clockwise-arrow" label="{}" mouseover="{}; {} to {};" showLabel="true" hyperlink="https://www.patricbrc.org/view/Feature/PATRIC.{}.{}.CDS.{}.{}.{}#view_tab=overview">\n'.format(i[4],i[3],i[3],i[1],i[2],ptid,accn,i[1],i[2],'fwd'))
    line.append('<featureRange start="{}" stop="{}" />\n'.format(i[1],i[2]))
    line.append('</feature>\n')
line.append('</featureSlot>\n\n\n')

line.append('<featureSlot featureThickness="0.5" showShading="true" minimumFeatureLength="0.1" strand="direct">\n')
line.append('<feature color="rgb(102,102,102)" decoration="arc">\n')
line.append('<featureRange start="1" stop="{}">\n'.format(seq_length))
line.append('</featureRange>\n')
line.append('</feature>\n')
line.append('</featureSlot>\n\n\n')

line.append('<featureSlot showShading="true" strand="reverse">\n')
for i in fdict['reverse']:
    line.append('<feature color="{}" decoration="counterclockwise-arrow" label="{}" mouseover="{}; {} to {};" showLabel="true" hyperlink="https://www.patricbrc.org/view/Feature/PATRIC.{}.{}.CDS.{}.{}.{}#view_tab=overview">\n'.format(i[4],i[3],i[3],i[1],i[2],ptid,accn,i[1],i[2],'rev'))
    line.append('<featureRange start="{}" stop="{}" />\n'.format(i[1],i[2]))
    line.append('</feature>\n')
line.append('</featureSlot>\n\n\n')

line.append('</cgview>\n')


fout = open(sys.argv[1].replace('.csv','_cgview.xml'), 'w')

for i in line:
    fout.write(i)
fout.close()
