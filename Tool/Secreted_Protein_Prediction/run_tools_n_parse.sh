#!/bin/bash

filename=$(echo $1 | awk -F'/' '{print $NF}')


echo $1 $filename

outdir=$2

mkdir $outdir

# To run the tools, please provide the absolute path in place of <path>
#phobius
/<path>/phobius/phobius.pl -short $1 > $outdir/$(echo $filename | sed 's/.fasta/_phobius.out/g') 2> $outdir/$(echo $filename | sed 's/.fasta/_phobius.log/g') &
#pids+=" $!"

#tmhmm
/<path>/tmhmm-2.0c/bin/tmhmm $1 > $outdir/$(echo $filename | sed 's/.fasta/_tmhmm.out/g') 2> $outdir/$(echo $filename | sed 's/.fasta/_tmhmm.log/g') &
#pids+=" $!"

#signalp
/<path>/signalp -org gram- -format short -fasta $1 -stdout > $outdir/$(echo $filename | sed 's/.fasta/_signalp.out/g') 2> $outdir/$(echo $filename | sed 's/.fasta/_signalp.log/g') &
#pids+=" $!"

#echo $pids
wait
# $pids
echo "All tools run are complete."

#parsing

#phobius
awk '{print $1"\t"$2}' $outdir/$(echo $filename | sed 's/.fasta/_phobius.out/g') | sed 's/ID/TM/g' | sed 's/SEQENCE/ID/g' > $outdir/$(echo $filename | sed 's/.fasta/_phobius_TM.tsv/g') 
awk '{print $1"\t"$3}' $outdir/$(echo $filename | sed 's/.fasta/_phobius.out/g') | sed 's/SEQENCE/ID/g' | sed 's/TM/SP/g' > $outdir/$(echo $filename | sed 's/.fasta/_phobius_SP.tsv/g') 

#signalp
python3 parse_signalp5.py $outdir/$(echo $filename | sed 's/.fasta/_signalp.out/g')

#tmhmm
python3 parse_tmhmm.py $outdir/$(echo $filename | sed 's/.fasta/_tmhmm.out/g')


