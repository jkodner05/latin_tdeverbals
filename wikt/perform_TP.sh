#!/bin/bash 

python3 get_freq_baselemmas.py outputs/baselemmas_clean_all.txt outputs/baselemmas_top100.txt 100
python3 get_freq_baselemmas.py outputs/baselemmas_clean_all.txt outputs/baselemmas_top500.txt 500
python3 get_freq_baselemmas.py outputs/baselemmas_clean_all.txt outputs/baselemmas_top1000.txt 1000

python3 perform_TP.py outputs/baselemmas_top100.txt
python3 perform_TP.py outputs/baselemmas_top500.txt
python3 perform_TP.py outputs/baselemmas_top1000.txt
