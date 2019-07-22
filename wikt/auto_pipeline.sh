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

#python3 reverse_sort.py $outputdir/first_raw.txt ../stats/verb_lemmacounts.txt $outputdir/first_lemmas_revsort.txt 3
#python3 reverse_sort.py $outputdir/second_raw.txt ../stats/verb_lemmacounts.txt $outputdir/second_lemmas_revsort.txt 3
#python3 reverse_sort.py $outputdir/third_raw.txt ../stats/verb_lemmacounts.txt $outputdir/third_lemmas_revsort.txt 3
#python3 reverse_sort.py $outputdir/fourth_raw.txt ../stats/verb_lemmacounts.txt $outputdir/fourth_lemmas_revsort.txt 3
#cat $outputdir/first_lemmas_revsort.txt $outputdir/second_lemmas_revsort.txt $outputdir/third_lemmas_revsort.txt $outputdir/fourth_lemmas_revsort.txt > $outputdir/lemmas_revsort_raw.txt

###### ### ## #
####
###
### manually add spaces to lemmas_revsort_raw.txt and save as lemmas_revsort_spaced.txt
###
####
###### ### ## #

###### ### ## #
####
###
### run the following two and make corrections to lemmas_revsort_spaced.txt until correct
### copy final version of lemma_revsort_baselemmas.txt to baselemmas_clean_all.txt
###
####
###### ### ## #
#python3 sum_basecounts.py $outputdir/lemmas_revsort_spaced.txt $outputdir/lemmas_revsort_counts.txt
#python3 extract_baselemmas.py $outputdir/lemmas_revsort_counts.txt $outputdir/lemmas_revsort_baselemmas.txt $outputdir/lemmas_mismatches.txt

#Then run these to make frequency-trimmed outputs
python3 get_freq_baselemmas.py outputs/baselemmas_clean_all.txt outputs/baselemmas_top100.txt 100
python3 get_freq_baselemmas.py outputs/baselemmas_clean_all.txt outputs/baselemmas_top500.txt 500
python3 get_freq_baselemmas.py outputs/baselemmas_clean_all.txt outputs/baselemmas_top1000.txt 1000

python3 extract_simple_freqs.py outputs/baselemmas_top1000.txt outputs/latin_top400.txt 400
