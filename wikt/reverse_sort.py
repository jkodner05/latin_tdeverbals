# -*- coding: utf-8 -*-
import re, sys
from wikt_utils import *

lemmafname = sys.argv[1]
freqfname = sys.argv[2]
reversesortedfname = sys.argv[3]
freqcutoff = int(sys.argv[4])

FIND_DEP = re.compile(r"or$")
VOWEL_RED = re.compile(r"([^aeiouāēīōū])[ie]([qrtpsdfghklzcvbnm][aeiouāēīōū])")
VOWEL_RED2 = re.compile(r"([^aeiouāēīōū])ae([qrtpsdfghklzcvbnm][aeiouāēīōū])")


def make_lemma_to_reversed(lemmafname, freqwords):
    lemma_to_reversed = {}

    with open(lemmafname, "r") as fin:
        for line in fin:
            components = vuji(line).split("\t")
            pres = components[0]
            inf = components[1]
            perf = components[2]
            pptc = components[3]
            redpres = VOWEL_RED.sub(r"\1a\2", pres)
            redpres = VOWEL_RED.sub(r"\1a\2", redpres)
            redpres = VOWEL_RED.sub(r"\1a\2", redpres)
            redpres = VOWEL_RED.sub(r"\1a\2", redpres)
            revpres = FIND_DEP.sub("ō",redpres)[::-1]
            lemma_to_reversed[(pres, inf, perf, pptc)] = revpres

    with open(reversesortedfname, "w") as fout:
        sortedrev = sorted(lemma_to_reversed.items(), key=lambda kv : kv[1], reverse=True)
        count = 0
        for lemma in sortedrev:
            freq = is_freq(lemma[0][0], freqwords)
            if  is_freq(lemma[0][0], freqwords):
                count += 1
#                print("\t".join(lemma[0]))
                fout.write(str(freq)+"\t"+"\t".join(lemma[0])+"\n")
        fout.write(str(freq)+"\t"+str(count)+"\n")
#        print(count)
    return


def main():
    freqwords = read_freqlist(freqfname, freqcutoff)
    make_lemma_to_reversed(lemmafname, freqwords)

if __name__ == "__main__":
    main()
