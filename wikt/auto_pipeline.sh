#!/bin/bash 

#System specific
htmldir1=../../data/wikt/first
htmldir2=../../data/wikt/second
htmldir3=../../data/wikt/third
htmldir4=../../data/wikt/fourth

freqlist=../../wikt/latin_lemma_most_common.txt
freqlist=../stats/verb_lemmacounts.txt

outputdir="outputs"

#outputs go here
mkdir -p $outputdir

#extract and collect the principle parts from the html files
#python3 verbs_to_tab.py $htmldir1 $outputdir/first_raw.txt
#python3 verbs_to_tab.py $htmldir2 $outputdir/second_raw.txt
#python3 verbs_to_tab.py $htmldir3 $outputdir/third_raw.txt
#python3 verbs_to_tab.py $htmldir4 $outputdir/fourth_raw.txt

python3 extract_by_lemma.py $outputdir/first_raw.txt 1 $freqlist $outputdir/first_lemmas_raw.txt $outputdir/first_stemchanges.txt 1000
python3 extract_by_lemma.py $outputdir/second_raw.txt 2 $freqlist $outputdir/second_lemmas_raw.txt $outputdir/second_stemchanges.txt 1000
python3 extract_by_lemma.py $outputdir/third_raw.txt 3 $freqlist $outputdir/third_lemmas_raw.txt $outputdir/third_stemchanges.txt 1000
python3 extract_by_lemma.py $outputdir/third_raw.txt 3i $freqlist $outputdir/thirdio_lemmas_raw.txt $outputdir/thirdio_stemchanges.txt 1000
python3 extract_by_lemma.py $outputdir/fourth_raw.txt 4 $freqlist $outputdir/fourth_lemmas_raw.txt $outputdir/fourth_stemchanges.txt 1000

