# -*- coding: utf-8 -*-
import re, sys

freqlistfname = sys.argv[1]
lemmalistfname = sys.argv[2]
top_n = int(sys.argv[3])


INF_1 = re.compile(r"(āre|ārī)$")
REMOVE_PRES_1 = re.compile(r"(ō|or)$")

INF_2 = re.compile(r"(ēre|ērī)$")
REMOVE_PRES_2 = re.compile(r"(eō|eor)$")

INF_3 = re.compile(r"(ere|[^īr]ī|[^ēr]ī|[^ār]ī)$")
INF_3i = re.compile(r"(ere|[^īr]ī|[^ēr]ī|[^ār]ī)$")
REMOVE_PRES_3 = re.compile(r"(ō|or)$")
REMOVE_PRES_3i = re.compile(r"(iō|ior)$")

INF_4 = re.compile(r"(īre|īrī)$")
REMOVE_PRES_4 = re.compile(r"(iō|ior)$")


REMOVE_PPART_longa = re.compile(r"(ātus|ātum|ātus\ssum|ātum\ssum)$")
REMOVE_PPART_shorta = re.compile(r"(atus|atum|atus\ssum|atum\ssum)$")
REMOVE_PPART_longe = re.compile(r"(ētus|ētum|ētus\ssum|ētum\ssum)$")
REMOVE_PPART_shorte = re.compile(r"(etus|etum|etus\ssum|etum\ssum)$")
REMOVE_PPART_longi = re.compile(r"(ītus|ītum|ītus\ssum|ītum\ssum)$")
REMOVE_PPART_shorti = re.compile(r"(itus|itum|itus\ssum|itum\ssum)$")
REMOVE_PPART_consonant = re.compile(r"(tus|tum|tus\ssum|tum\ssum)$")
REMOVE_PPART_s = re.compile(r"(s+us|s+um|s+us\ssum|s+um\ssum|xus|xum|xus\ssum|xum\ssum)$")


REMOVE_PREFIX_NOCONTEXT = re.compile(r"^(ab|ad|circum|con|de|dē|dis|ex|ēx|inter|īnter|in|īn|ob|per|prae|pro|re|sub|trans|trāns|trā|super)")
REMOVE_PREFIX_RISKY = re.compile(r"^(a|e|ē)")
REMOVE_PREFIX_C = re.compile(r"^(acc|occ|succ|ecc|ēcc|occ|succ)")
REMOVE_PREFIX_Q = re.compile(r"^(acq)")
REMOVE_PREFIX_F = re.compile(r"^(aff|eff|ēff|off|suff)")
REMOVE_PREFIX_G = re.compile(r"^(agg)")
REMOVE_PREFIX_L = re.compile(r"^(all|coll|ill|īll)")
REMOVE_PREFIX_P = re.compile(r"^(app|comp|opp|supp)")
REMOVE_PREFIX_R = re.compile(r"^(arr|irr|īrr|surr|cor)")
REMOVE_PREFIX_S = re.compile(r"^(ass|sus)")
REMOVE_PREFIX_M = re.compile(r"^(comm|imm|īmm)")
REMOVE_PREFIX_T = re.compile(r"^(att)")
REMOVE_PREFIX_SP = re.compile(r"^(asp)")


lemmas_by_form = {}
counts_by_lemma = {}
counts_by_form = {}

def read_lemmas():
    with open(lemmalistfname, "r") as f:
        lemma = ""
        for line in f:
            if not line.strip():
                continue
            if line[0] != "\t":
                lemma = (line.split("\t")[0].strip(),line.split("\t")[1].strip(),line.split("\t")[2].strip())
            else:
                form = line.split("\t")[1].strip().replace("ā", "a").replace("ē", "e").replace("ī", "i").replace("ō", "o").replace("ū", "u")
                lemmas_by_form[form] = lemma
    return lemmas_by_form

def read_freqlist():
    remove_nums = re.compile(r"\d+")
    i = 0
    with open(freqlistfname, "r") as f:
        for line in f:
            if i >= top_n:
                break
            word = remove_nums.sub("",line.split("\t")[0]).replace("-","").replace("_","").replace("v","u").replace("j","i").strip()
            count = int(line.split("\t")[1].strip())

            if word in lemmas_by_form:
                if lemmas_by_form[word] in counts_by_lemma:
                    counts_by_lemma[lemmas_by_form[word]] += count
                else:
                    counts_by_lemma[lemmas_by_form[word]] = count
                if word in counts_by_form:
                    counts_by_form[word] += count
                else:
                    counts_by_form[word] = count
    return counts_by_lemma, counts_by_form

read_lemmas()
read_freqlist()
#print(lemmas_by_form)

counts_by_lemma = sorted(counts_by_lemma.items(), key=lambda kv: kv[1], reverse=True)[0:top_n]
for lemma, count in counts_by_lemma:
    print(lemma[0]+"\t"+lemma[1]+"\t"+lemma[2])
#
#print(counts_by_form)
#counts_by_form = sorted(counts_by_form.items(), key=lambda kv: kv[1], reverse=True)[0:top_n]
#for lemma, count in counts_by_form:
#    print(lemma[0]+"\t"+lemma[1]+"\t"+lemma[2])
