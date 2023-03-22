#! /usr/bin/python3

import glob
import os
import sys
import argparse
import configparser
from Bio import SeqIO
import pandas as pd
import shutil
from functools import reduce
import datetime

parser = argparse.ArgumentParser(description='Predict T9SS protein in user submitted protein sequences in fasta format.',epilog='For more details please contact: Areejit Samal [asamal@imsc.res.in]')
parser.add_argument('input', metavar='proteins.fasta', type=str, help='Input protein fasta file')
parser.add_argument('-d','--outdir', action='store', type=str, default="./", help='Output directory for writing the outfile(s)')
parser.add_argument('-o','--outfile', action='store', type=str, help='Output file name')
parser.add_argument('-k','--keep', action='store_true', help='Keep output files from hmmsearch in the output directory.')


args = parser.parse_args()
input_file = args.input

filename=input_file.split('/')[-1].replace('.faa','').replace('.fasta','')

outdir=args.outdir

keep=args.keep

if args.outfile is None:
    outfile='{}_hit_matrix.csv'.format(outdir+'/'+filename)
else:
    outfile=outdir+'/'+args.outfile

# input file should have .faa or .fasta extension
if not(input_file.endswith('.fasta')):
    print ('Please input a fasta file with .fasta extension')
    sys.exit()


# Checking with experimenetally characterized protein sequences
expiden = {}
with open ('combined_102.fasta') as exp:
    for record in SeqIO.parse(exp,'fasta'):
        expiden[record.id] = str(record.seq)


# Getting the protein identifier from input fasta
idens = []
inpiden = {} # created this additional dictionary just to compare in th next for loop
with open (input_file) as inp:
    for record in SeqIO.parse(inp,'fasta'):
        idens.append(record.id)
        inpiden[record.id] = str(record.seq)

# Check which protein sequence from the input file is already present in the experimental sequence
expseq= []
for protein in inpiden.keys():
    if inpiden[protein] in expiden.values():
        expseq.append(protein) #expseq contains all the proteins which are experimentally characterized


read_config = configparser.ConfigParser()
read_config.read("CONFIG.ini")
HMMSEARCH_BINARY_PATH = read_config.get("Paths", "HMMSEARCH_BINARY_PATH")
MODELS_PATH = read_config.get("Paths", "MODELS_PATH")

# HMM models for three CTD types 
MODELS = [f for f in os.listdir(MODELS_PATH) if os.path.isfile(os.path.join(MODELS_PATH, f)) and f.endswith('.hmm')]

#Running the tools (signalp, phobius and TMHMM) and parsing of the tools output
os.system('./run_tools_n_parse.sh {} {}'.format(input_file, outdir))

# deleting files/folders associated with runs from TMHMM
tm_tmp = glob.glob('TMHMM_*')
for i in tm_tmp:
    shutil.rmtree (i)


# Checking the output and log file from running the tools
def check_out_log_file(input_file, outdir):
    '''
    Check if the log files and tools output files are correct.
    '''
    Flag_log = 0
    tools = []
    for ele in glob.glob(outdir+'/'+'*.log'):
        lines = open(ele).readlines()
        if 'phobius' in ele:
            length = 0
            for k in lines:
                if 'uninitialized value $predstr' in k: # this is a phobius waring which can be ingnored
                    length = length
                else:
                    length = length+1
            if length != 3:
                Flag_log = 1
                tools.append('phobius')
        else:
            if len(lines) !=0:
                Flag_log = 1
                tools.append(ele.split('.')[0].split('_')[-1])
    Flag_out = 0
    
    for ele in glob.glob(outdir+'/'+'*.out'):
        lines = open(ele).readlines()
        if 'signalp' in ele:
            if len(lines)-2 != len(idens):
                Flag_out = 1
                tools.append('signalp')
        elif 'phobius' in ele:
            if len(lines)-1 != len(idens):
                Flag_out = 1
                tools.append('phobius')
        elif 'TMHMM' in ele:
            count = 0
            for line in open(ele):
                if 'Length:' in line:
                    count = count+1
                else:
                    count = count
            if count != len(idens):
                Flag_out = 1
                tools.append('TMHMM')
    return(Flag_log, Flag_out, tools)

Flag_log,Flag_out,tools = check_out_log_file(input_file, outdir)
if (any([Flag_log == 1, Flag_out == 1])):
    print ('Error in running {}'.format(', '.join(list(set(tools)))))
    sys.exit()

print (datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
print ('Using python installed at {}\n'.format('/'.join(os.__file__.split('/')[:-1])))
print ('Using hmmsearch installed at {}\n'.format(HMMSEARCH_BINARY_PATH))
print ('Using {} HMM models for predicting T9SS CTD from {}\n'.format(len(MODELS), MODELS_PATH))
print ('Output directory is {}\n'.format(outdir))
print ('Output file is {}\n'.format(outfile))
print ('Intermediate *.log and *.out files from hmmsearch are deleted: {}\n'.format(str(not(keep))))


files = sorted(glob.glob(outdir+'/'+'*.tsv'))
#print(files)
dfs = [0]*len(files)
names = []
for i in range(len(files)):
    names.append('_'.join(files[i].replace('.tsv','').split('_')[-2:]))
    dfs[i] = pd.read_csv(files[i],sep = '\t')
df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['ID'],how='outer'), dfs)
df_merged.columns = ['ID']+names
df_merged['phobius_SP'].replace({'Y':1,'N':0}, inplace=True)
df1 = pd.DataFrame(df_merged[['ID','signalp_SP','phobius_SP','signalp_TP','phobius_TM','tmhmm_TM']])

for i in df1.columns[1:]:
    df1[i] = df1[i].fillna(0)
    df1[i] = df1[i].astype('int')

df1['SP'] = df1['signalp_SP'] + df1['phobius_SP'] >= 1

df1['TM'] = df1['phobius_TM'] + df1['tmhmm_TM'] >= 1
df2 = pd.DataFrame(df1[(df1['SP'] == True) & (df1['signalp_TP'] == 0) & (df1['TM'] == False)].reset_index(drop = True))




passed_idens = sorted(list(df2['ID']))
f1 = open(outdir+'/'+'passed_identifiers.fasta','w')
for record in SeqIO.parse(input_file,'fasta'):
    if record.id in expseq:
        continue
    else: 
        for ele in passed_idens:
            if record.id == ele:
                if len(record.seq) <= 120:
                    f1.write('>'+record.id+'\n'+str(record.seq)+'\n')
                else:
                    ctd = str(record.seq[-120:])
                    f1.write('>'+record.id+'\n'+ctd+'\n')
f1.close()

# running the HMMsearch for three CTD types
for k in MODELS:
    if k == 'TypeC.hmm':
        cmd = '{} --cut_ga --tblout {}.out {} {} > {}.log '.format(HMMSEARCH_BINARY_PATH, outdir+'/'+filename+'_'+k.replace('.hmm',''), MODELS_PATH+k, outdir+'/'+'passed_identifiers.fasta', outdir+'/'+filename+'_'+k.replace('.hmm',''))
    else:
        cmd = '{} -E 1e-6 --tblout {}.out {} {} > {}.log '.format(HMMSEARCH_BINARY_PATH, outdir+'/'+filename+'_'+k.replace('.hmm',''), MODELS_PATH+k, outdir+'/'+'passed_identifiers.fasta', outdir+'/'+filename+'_'+k.replace('.hmm',''))
    os.system(cmd)


ctdmapping = {}
for i in MODELS:
    ctdmapping[i.replace('.hmm','')] = []

fileswithhits=[]
fout=open(outfile,'w')

fout.write('Type of evidence\tCTD Types\tHits\tE-value\tScore\n')
fout.write('Experimental'+'\t'+''+', '.join(expseq)+'\n')

for k in MODELS:
    outfiles=outdir+'/'+filename+'_'+k.replace('.hmm','')+'.out'
    tmp = [i.strip() for i in open(outfiles) if i[0] != '#']
    if len(tmp) > 0:
        fileswithhits.append(k)
        for j in tmp:
            tmp2=j.strip().split()
            component = k.replace('.hmm','')
            tmp3='Computational'+'\t'+'\t'.join([component,tmp2[0],tmp2[4],tmp2[5]])
            fout.write(tmp3+'\n')
            ctdmapping[component].append(tmp2[0])
    else:
        fout.write(k.replace('.hmm','')+'\n')
        continue
fout.close()

# Deleting the intermediate files
if not(keep):
    tmpfiles = os.listdir(outdir)
    for item in tmpfiles:
        if item.endswith(".out") or item.endswith(".log") or item.endswith(".tsv") or item.endswith(".fasta"):
            os.remove(os.path.join(outdir, item))



typeA_hits = set(ctdmapping['TypeA'])
typeB_hits = set(ctdmapping['TypeB'])
typeC_hits = set(ctdmapping['TypeC'])

file = open(outdir+'/'+'CTD_type_statistics.csv','w')

file.write('Total identifiers'+'\t'+str(len(idens))+'\n')
file.write('TypeA hits'+'\t'+str(len(typeA_hits))+'\n')
file.write('TypeB hits'+'\t'+str(len(typeB_hits))+'\n')
file.write('TypeC hits'+'\t'+str(len(typeC_hits))+'\n')

file.write('TypeA TypeB intersection'+'\t'+str(len(typeA_hits.intersection(typeB_hits)))+'\n')
file.write('TypeB TypeC intersection'+'\t'+str(len(typeB_hits.intersection(typeC_hits)))+'\n')
file.write('TypeA TypeC intersection'+'\t'+str(len(typeA_hits.intersection(typeC_hits)))+'\n')
file.close()


outfilechk = os.listdir(outdir)
FLAG=0
for item in outfilechk:
    if item == outfile.replace(outdir+'/',''):
        print ('Success.')
        FLAG=1
        break
    else:
        continue
if FLAG==0:
    print ('Error!!! Output file not found, Run Failed!')

