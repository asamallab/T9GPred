# Sun Dec 22 16:03:22 IST 2019

import pandas as pd
import sys


inp = sys.argv[1]

df = pd.read_csv(inp, sep='\t', comment='#', header=None, usecols=[0,1])

df['SP'] = df[1].replace({'OTHER':0, 'SP(Sec/SPI)':1, 'LIPO(Sec/SPII)':0, 'TAT(Tat/SPI)':0})
df['LP'] = df[1].replace({'OTHER':0, 'SP(Sec/SPI)':0, 'LIPO(Sec/SPII)':1, 'TAT(Tat/SPI)':0})
df['TP'] = df[1].replace({'OTHER':0, 'SP(Sec/SPI)':0, 'LIPO(Sec/SPII)':0, 'TAT(Tat/SPI)':1})
df['OTHERS'] = df[1].replace({'OTHER':1, 'SP(Sec/SPI)':0, 'LIPO(Sec/SPII)':0, 'TAT(Tat/SPI)':0})

df_sp = df[[0,'SP']]
df_sp.columns = ['ID','SP']

df_lp = df[[0,'LP']]
df_lp.columns = ['ID','LP']

df_tp = df[[0,'TP']]
df_tp.columns = ['ID','TP']

df_others = df[[0,'OTHERS']]
df_others.columns = ['ID','OTHERS']

df_sp.to_csv(inp.replace('.out','_SP.tsv'), sep='\t', index=False)
df_lp.to_csv(inp.replace('.out','_LP.tsv'), sep='\t', index=False)
df_tp.to_csv(inp.replace('.out','_TP.tsv'), sep='\t', index=False)
df_others.to_csv(inp.replace('.out','_Others.tsv'), sep='\t', index=False)
