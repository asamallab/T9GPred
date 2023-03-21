# code for merging the genome coord information from gff file (from Patric) with the output from T9GPred.py program

import pandas as pd
import sys

df = pd.read_csv(sys.argv[1],sep='\t') #output file from T9GPred.py
print (df.shape)

df.dropna(inplace=True)
df['Identifier'] = df['Hits'].map(lambda x: '|'.join(x.strip().split('|')[0:2]))
iden = list(df['Identifier'])
#print (len(iden), len(set(iden))) #485917.6.peg.4130 is getting picked twice
print (df.shape)

gff = pd.read_csv(sys.argv[2],comment='#',header=None,sep='\t') #gff file for the genome from Patric
gff['Identifier'] = gff[8].map(lambda x: x.strip().split(';')[0].replace('ID=',''))
print (gff.shape)

gff_selec = gff[(gff['Identifier'].isin(iden))]
gff_selec = gff_selec[[3,4,6,'Identifier']]
gff_selec = gff_selec[['Identifier',3,4,6]]
gff_selec.columns = ['Identifier','Start','Stop','Direction']
gff_selec.reset_index(drop=True, inplace=True)
print (gff_selec.shape)

df_gff = df.merge(gff_selec,on='Identifier',how='left')
print (df_gff.shape)
df_gff.head()

#FLAG=0
GFLAG, SFLAG = 0, 0
for i in open(sys.argv[2]):
#    if FLAG != 2:
    if '#Genome:' in i:
        tmp1 = i.strip().split('|')
        ptid = tmp1[0].replace('#Genome:','').strip()
        ptname = tmp1[1].strip().replace(' ','-')
        GFLAG+=1
    if '##sequence-region' in i:
        tmp = i.strip().split('\t')
        accn = tmp[1].strip().replace('accn|','').replace('_','-')
        seq_length = tmp[3].strip()
        SFLAG+=1
#    else:
#        break

if  GFLAG == 1 and SFLAG == 1:
    print ('1 line with Genome info & 1 line with sequence-region are present')
    df_gff.to_csv(sys.argv[1].replace('.csv','_genome_coord_{}_{}_{}_{}.csv'.format(ptid,ptname,accn,seq_length)),sep='\t', index=False)
else:
    if GFLAG == 0 or SFLAG == 0:
        print ('Error -> Genome info line or sequence-region line is/are missing!!!')

    if GFLAG > 1 or SFLAG > 1:
        print ('Error -> More than one Genome info line or sequence-region line are found in gff file!!!')

    

