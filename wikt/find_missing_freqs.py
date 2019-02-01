# -*- coding: utf-8 -*-
import re, sys

freqsfname = sys.argv[1]
lemmasfname = sys.argv[2]

freqwords = set([])
lemmas = set([])

with open(freqsfname, "r") as f:
    for line in f:
        freqwords.add(line.strip())

with open(lemmasfname, "r") as f:
    for line in f:
        if line[0] == "\t":
            continue
        lemma = line.split("\t")[0].strip().replace("ā", "a").replace("ē", "e").replace("ī", "i").replace("ō", "o").replace("ū", "u")
        lemmas.add(lemma)

match = 0
nomatch = 0
got_options = 0
for freqword in freqwords:
    if freqword not in lemmas:
        print(freqword)
        options = False
        for lemma in lemmas:
            if freqword in lemma:
                print("\t" + lemma)
                options = True
        if options:
            got_options += 1
        nomatch += 1
    else:
        match += 1
        
print(match)
print(nomatch)
print(got_options)
