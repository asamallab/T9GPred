#! /usr/bin/python3

import os
import sys
import datetime
import argparse
import configparser

parser = argparse.ArgumentParser(description='Predict T9SS protein in user submitted protein sequences in fasta format.',epilog='For more details please contact: Areejit Samal [asamal@imsc.res.in]')
parser.add_argument('input', metavar='proteins.fasta', type=str, help='Input protein fasta file')
parser.add_argument('-d','--outdir', action='store', type=str, default="./", help='Output directory for writing the outfile(s)')
parser.add_argument('-o','--outfile', action='store', type=str, help='Output file name')
parser.add_argument('-k','--keep', action='store_true', help='Keep output files from hmmsearch in the output directory.')

args = parser.parse_args()
input_file = args.input

filename=input_file.split('/')[-1].replace('.faa','').replace('.fasta','')

outdir=args.outdir.split('/')[0]+'/'

if args.outfile is None:
    outfile='{}_hit_matrix.csv'.format(outdir+filename)
else:
    outfile=outdir+args.outfile

keep=args.keep

if not(any([input_file.endswith('.faa'), input_file.endswith('.fasta')])):
    print ('Please input a fasta file with .fasta or .faa extension')
    sys.exit()

read_config = configparser.ConfigParser()
read_config.read("CONFIG.ini")
HMMSEARCH_BINARY_PATH = read_config.get("Paths", "HMMSEARCH_BINARY_PATH")
MODELS_PATH = read_config.get("Paths", "MODELS_PATH")
MANDATORY_T9SS = read_config.get("T9SS_MAND","MANDATORY_T9SS").split(',')
MANADATORY_Gliding = read_config.get("Motility_MAND","MANADATORY_Gliding").split(',')

MODELS=[f for f in os.listdir(MODELS_PATH) if os.path.isfile(os.path.join(MODELS_PATH, f)) and f.endswith('.hmm')]
if len(MODELS) !=28:
    print ('Warning!!! MODELS files missing for T9SS prediction\n\n')

mandatoryT={}
mandatoryG={}

for f in MODELS:
    tmp=f.strip()
    if tmp in MANDATORY_T9SS:
        mandatoryT[tmp]=1
    else:
        mandatoryT[tmp]=0
    if tmp in MANADATORY_Gliding:
        mandatoryG[tmp]=1
    else:
        mandatoryG[tmp]=0


print (datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
print ('Using python installed at {}\n'.format('/'.join(os.__file__.split('/')[:-1])))
print ('Using hmmsearch installed at {}\n'.format(HMMSEARCH_BINARY_PATH))
print ('Using {} HMM models for predicting T9SS genes from {}\n'.format(len(MODELS), MODELS_PATH))
print ('Output directory is {}\n'.format(outdir))
print ('Output file is {}\n'.format(outfile))
print ('Intermediate *.log and *.out files from hmmsearch are deleted: {}\n'.format(str(not(keep))))

def T9GPred(inp):
    
    # code for running the hmmsearch
    for k in mandatoryT.keys():
        cmd='{} --cut_ga --tblout {}.out {} {} > {}.log '.format(HMMSEARCH_BINARY_PATH, outdir+filename+'_'+k.replace('.hmm',''), MODELS_PATH+k, inp, outdir+filename+'_'+k.replace('.hmm',''))
        os.system(cmd)

    # code for selecting outfiles with hits
    fileswithhits=[]
    fout=open(outfile,'w')
    fout.write('protein components\tHits\tE-value\tScore\n')
    for k in mandatoryT.keys():
        outfiles=outdir+filename+'_'+k.replace('.hmm','')+'.out'
        tmp = [i.strip() for i in open(outfiles) if i[0] != '#']
        if len(tmp) > 0:
            fileswithhits.append(k)
            for j in tmp:
                tmp2=j.strip().split()
                component = k.replace('.hmm','')
                if component == 'CHU_0134' or component == 'CHU_2981':
                    component_clean = component.strip()
                elif component == 'SprF_PorP_CHU_0170':
                    component_clean = 'SprF / PorP / CHU_0170'
                else:
                    component_clean = component.replace('_',' / ').strip()
                tmp3='\t'.join([component_clean,tmp2[0],tmp2[4],tmp2[5]])
                fout.write(tmp3+'\n')
        else:
            fout.write(k.replace('.hmm','')+'\n')
            continue
    
    mlT=set(sorted([k for k in mandatoryT.keys() if mandatoryT[k] == '1']))
    mlG=set(sorted([k for k in mandatoryG.keys() if mandatoryG[k] == '1']))

    if len(set(fileswithhits).intersection(mlT)) == len(mlT):
        fout.write('\n# T9SS present, all mandatory components were identified.\n')
        if len(set(fileswithhits).intersection(mlG)) == len(mlG):
            fout.write('\n# Gliding motility is predicted, all mandatory componenets were identified.\n')
        else:
            fout.write('\n# Gliding motility is not present, some or all manadatory componenets were not identified.\n')
    else:
        fout.write('\n# T9SS not present, some or all mandatory components were not identified.\n')
    
    fout.close()
    
    if not(keep):
        tmpfiles = os.listdir(outdir)
        for item in tmpfiles:
            if item.endswith(".out") or item.endswith(".log"):
                os.remove(os.path.join(outdir, item))


T9GPred(input_file)

outfilechk = os.listdir(outdir)
FLAG=0
for item in outfilechk:
    if item == outfile.replace(outdir,''):
        print ('Success.')
        FLAG=1
        break
    else:
        continue
if FLAG==0:
    print ('Error!!! Output file not found, Run Failed!')
