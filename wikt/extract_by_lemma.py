# -*- coding: utf-8 -*-
import re, sys

lemmafname = sys.argv[1]
conjugation = sys.argv[2]
freqlist = sys.argv[3]
lemmaoutfname = sys.argv[4]
schangeoutfname = sys.argv[5]
top_n = int(sys.argv[6])


INF_1 = re.compile(r"(āre|ārī)$")
REMOVE_PRES_1 = re.compile(r"(ō|or)$")

INF_2 = re.compile(r"(ēre|ērī)$")
REMOVE_PRES_2 = re.compile(r"(eō|eor)$")

INF_3 = re.compile(r"(ere|ī)$")
INF_3i = re.compile(r"(ere|ī)$")
REMOVE_PRES_3 = re.compile(r"(ō|or)$")
REMOVE_PRES_3i = re.compile(r"(iō|ior)$")

INF_4 = re.compile(r"(īre|ī)$")
REMOVE_PRES_4 = re.compile(r"(iō|ior)$")


REMOVE_PPTC_longa = re.compile(r"(ātus|ātum|ātus\ssum|ātum\ssum)$")
REMOVE_PPTC_shorta = re.compile(r"(atus|atum|atus\ssum|atum\ssum)$")
REMOVE_PPTC_longe = re.compile(r"(ētus|ētum|ētus\ssum|ētum\ssum)$")
REMOVE_PPTC_shorte = re.compile(r"(etus|etum|etus\ssum|etum\ssum)$")
REMOVE_PPTC_longi = re.compile(r"(ītus|ītum|ītus\ssum|ītum\ssum)$")
REMOVE_PPTC_shorti = re.compile(r"(itus|itum|itus\ssum|itum\ssum)$")
REMOVE_PPTC_consonant = re.compile(r"(tus|tum|tus\ssum|tum\ssum)$")
REMOVE_PPTC_s = re.compile(r"(s+us|s+um|s+us\ssum|s+um\ssum|xus|xum|xus\ssum|xum\ssum)$")


REMOVE_PREFIX_NOCONTEXT = re.compile(r"^(ab|ad|ante|circum|con|cōn|de|dē|dis|dī|ex|ēx|inter|īnter|in|īn|ob|ōb|per|prae|pro|prō|re|sub|trans|trāns|trā|super)")
REMOVE_PREFIX_RISKY = re.compile(r"^(a|ā|e|ē)")
REMOVE_PREFIX_C = re.compile(r"^(acc|occ|succ|ecc|ēcc|occ|ōcc|succ|susc)")
REMOVE_PREFIX_Q = re.compile(r"^(acq)")
REMOVE_PREFIX_F = re.compile(r"^(aff|eff|ēff|off|ōff|suff|dif)")
REMOVE_PREFIX_G = re.compile(r"^(agg)")
REMOVE_PREFIX_L = re.compile(r"^(all|coll|cōll|ill|īll|pell)")
REMOVE_PREFIX_P = re.compile(r"^(app|comp|cōmp|opp|supp)")
REMOVE_PREFIX_R = re.compile(r"^(arr|irr|īrr|surr|cor|cōr)")
REMOVE_PREFIX_S = re.compile(r"^(ass)")
REMOVE_PREFIX_M = re.compile(r"^(comm|cōmm|imm|īmm)")
REMOVE_PREFIX_T = re.compile(r"^(att)")
REMOVE_PREFIX_SP = re.compile(r"^(asp)")


def strip_form(raw):
    form = REMOVE_PREFIX_SP.sub("sp", raw)
    form = REMOVE_PREFIX_T.sub("t", form)
    form = REMOVE_PREFIX_M.sub("m", form)
    form = REMOVE_PREFIX_S.sub("s", form)    
    form = REMOVE_PREFIX_R.sub("r", form)
    form = REMOVE_PREFIX_P.sub("p", form)
    form = REMOVE_PREFIX_L.sub("l", form)    
    form = REMOVE_PREFIX_G.sub("g", form)
    form = REMOVE_PREFIX_F.sub("f", form)
    form = REMOVE_PREFIX_Q.sub("q", form)
    form = REMOVE_PREFIX_C.sub("c", form)
    form = REMOVE_PREFIX_C.sub("c", form)
    form = REMOVE_PREFIX_NOCONTEXT.sub("",form)
    form = REMOVE_PREFIX_RISKY.sub("",form)
    if len(form) < 3 and form != "eo" and form != "do" and form != "eō" and form != "dō":
        return raw
    return form


def read_freqlist():
    remove_nums = re.compile(r"\d+")
    freq_words = set([])
    i = 0
    with open(freqlist, "r") as f:
        for line in f:
#            if i >= top_n:
#                break
            word = remove_nums.sub("",line.split("\t")[1]).replace("-","").replace("_","").replace("v","u").replace("j","i") + " "
            if "tor " in word or "tio " in word:
#                print("SKIPPING\t", word)
                continue
            word = word.strip()
            if len(word) >= 2 and ((word[-1] == "o") or (word[-1] == "r" and word[-2] == "o")): #~verbs 
                old_word = word
                word = strip_form(word)
                freq_words.add(word)
                i += 1
#    print("GOT THE TOP " + str(i) + " VERBS")
    return freq_words


def is_freq(candidate, freq_words):
    candidate = candidate.replace("ā", "a").replace("ē", "e").replace("ī", "i").replace("ō", "o").replace("ū", "u")
    return candidate in freq_words


def main():
    freq_words = read_freqlist()
    fwlist = list(freq_words)
    fwlist.sort()
    #for w in fwlist:
    #    print(w)
    #exit()

    INF = INF_1
    REMOVE_PRES = REMOVE_PRES_1
    if conjugation == "1":
        INF = INF_1
        REMOVE_PRES = REMOVE_PRES_1
    elif conjugation == "2":
        INF = INF_2
        REMOVE_PRES = REMOVE_PRES_2
    elif conjugation == "3":
        INF = INF_3
        REMOVE_PRES = REMOVE_PRES_3
    elif conjugation == "3i":
        INF = INF_3i
        REMOVE_PRES = REMOVE_PRES_3i
    elif conjugation == "4":
        INF = INF_4
        REMOVE_PRES = REMOVE_PRES_4


    form_map = {}
    verblist = []
    with open(lemmafname,"r") as fin:
        verbs = set([])
        for line in fin:
            components = line.replace("v","u").replace("j","i").split("\t")
            pres = components[0]
            inf = components[1]
            perf = components[2]
            pptc = components[3]

            old_pres = pres
            old_inf = inf
            old_perf = perf
            old_pptc = pptc
            new_pres = strip_form(pres)
            new_inf = strip_form(inf)
            new_perf = strip_form(perf)
            new_pptc = strip_form(pptc)

            if (new_pres != pres or new_perf != perf) and (new_pptc != pptc or pptc == "-"):
                pres = new_pres
                inf = new_inf
                perf = new_perf
                pptc = new_pptc
            if (pres,inf,perf,pptc) not in form_map:
                form_map[(pres,inf,perf,pptc)] = [(old_pres,old_inf,old_perf,old_pptc)]
            else:
                form_map[(pres,inf,perf,pptc)].append((old_pres,old_inf,old_perf,old_pptc))
            if is_freq(new_pres, freq_words):# and INF.findall(inf):
    #            if old_pres != pres:
    #                print("REPLACED", old_pres, old_pptc, "\t", new_pres, new_pptc)
                verbs.add((pres,inf,perf,pptc))

#    print(verbs)
#    exit()
    verblist = list(verbs)
    verblist.sort()
    with open(lemmaoutfname, "w") as fout:
        for key, derivs in form_map.items():
            if key[3] != "-":
                lemmapparts = "\t".join(key)
                print(lemmapparts)
                fout.write(lemmapparts+"\n")
                for pparts in derivs:
                    derivpparts = "\t".join(pparts)
                    print("\t" + derivpparts)
                    fout.write("\t"+derivpparts+"\n")
            fout.write("\n")


    print("\n\n")
    print("STEM CHANGES")
    print("")

    with open(schangeoutfname, "w") as fout:
        for key, derivs in form_map.items():
            pres = key[0]
            inf = key[1]
            perf = key[2]
            pptc = key[3]
            pres_i = pres[:-2].replace("a","i").replace("ā","ī") + pres[-2:]
            inf_i = inf.replace("a","i").replace("ā","ī")
            perf_i = perf.replace("a","i").replace("ā","ī")
            perf_e = pptc.replace("a","e").replace("ā","ē")
            pptc_i = pptc.replace("a","i").replace("ā","ī")
            pptc_e = pptc.replace("a","e").replace("ā","ē")

            if pres_i == pres:
                continue

            if (pres_i, inf_i, pptc_i) in form_map or (pres_i, inf_i, pptc_e) in form_map:
                lemmapparts = "\t".join(key)
                print(lemmapparts)
                fout.write(lemmapparts+"\n")
                for pparts in derivs:
                    derivpparts = "\t".join(pparts)
                    print(derivpparts) 
                    fout.write(derivpparts+"\n") 
                if (pres_i, inf_i, perf, pptc_i) in form_map:
                    for pparts in form_map[pres_i, inf_i, perf, pptc_i]:
                        derivpparts = "\t".join(pparts)
                        print("\t" + derivpparts)
                        fout.write("\t"+derivpparts+"\n")
                elif (pres_i, inf_i, perf_i, pptc_i) in form_map:
                    for pparts in form_map[pres_i, inf_i, perf_i, pptc_i]:
                        derivpparts = "\t".join(pparts)
                        print("\t" + derivpparts)
                        fout.write("\t"+derivpparts+"\n")
                elif (pres_i, inf_i, perf_e, pptc_i) in form_map:
                    for pparts in form_map[pres_i, inf_i, perf_e, pptc_i]:
                        derivpparts = "\t".join(pparts)
                        print("\t" + derivpparts)
                        fout.write("\t"+derivpparts+"\n")
                elif (pres_i, inf_i, perf, pptc_e) in form_map:
                    for pparts in form_map[pres_i, inf_i, perf, pptc_i]:
                        derivpparts = "\t".join(pparts)
                        print("\t" + derivpparts)
                        fout.write("\t"+derivpparts+"\n")
                elif (pres_i, inf_i, perf_i, pptc_e) in form_map:
                    for pparts in form_map[pres_i, inf_i, perf_i, pptc_i]:
                        derivpparts = "\t".join(pparts)
                        print("\t" + derivpparts)
                        fout.write("\t"+derivpparts+"\n")
                elif (pres_i, inf_i, perf_e, pptc_e) in form_map:
                    for pparts in form_map[pres_i, inf_i, perf_e, pptc_i]:
                        derivpparts = "\t".join(pparts)
                        print("\t" + derivpparts)
                        fout.write("\t"+derivpparts+"\n")

    
if __name__ == "__main__":
    main()
