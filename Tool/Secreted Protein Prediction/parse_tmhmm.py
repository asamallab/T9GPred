#Tue Jul 17 19:24:14 IST 2018 
#!/usr/bin/python3
#Vivek

import pandas as pd
from numpy import zeros
import sys

inp = sys.argv[1]


dfiden = pd.read_csv(inp, comment='#', sep='\t', header=None)
iden =  set(dfiden[0])
print (len(iden))


df = pd.DataFrame(columns=['A','B','C','D','E'])
ind = 0

for line in open(inp):
	tmp1 = line.strip().split()
	if ('TMHMM2.0' in line and 'TMhelix' in line):
		if (int(tmp1[3]) > 70):
    			df.loc[ind] = tmp1
    			ind += 1

df2 = df['A'].value_counts()
df3 = df2.to_frame()
df3.reset_index(inplace=True)
df3.columns = ['ID','TM']

ids_left = [i for i  in iden if i not in list(df2.index)]
df4 = pd.DataFrame({'ID':ids_left,'TM':zeros(len(ids_left))})

df5 = pd.concat([df3,df4],ignore_index=True)
df5['TM'] = df5['TM'].astype(int)

df5.to_csv(inp.replace('.out','_TM.tsv'), sep='\t', index=False)
