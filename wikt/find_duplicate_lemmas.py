# -*- coding: utf-8 -*-
import re, sys

fname = sys.argv[1]

lemmas_by_pres_and_inf = {}

DEPPRES = re.compile(r"or$")
DEPINF_1 = re.compile(r"(ārī)$")
DEPINF_2 = re.compile(r"(ērī)$")
DEPINF_3 = re.compile(r"([^īr]ī|[^ēr]ī|[^ār]ī)$")
DEPINF_4 = re.compile(r"(īrī)$")


def make_nondeponent(deppres, depinf, depppart):
    pres = DEPPRES.sub("ō",deppres)
    inf = DEPINF_1.sub("āre",depinf)
    inf = DEPINF_2.sub("ēre",inf)
    inf = DEPINF_3.sub("ere",inf)
    inf = DEPINF_4.sub("īre",inf)
    ppart = (depppart.split(" ")[0] + " ").replace("us ","um ").replace("ur ","um ").strip()
    return pres, inf, ppart

with open(fname, "r") as f:
    for line in f:
        if not line.strip():
            continue
        if line[0] == "\t":
            continue
        rawpres = line.split("\t")[0].strip()
        rawinf = line.split("\t")[1].strip()
        rawppart = (line.split("\t")[2] + " ").replace("us ", "um ").strip()
        pres, inf, ppart = make_nondeponent(rawpres, rawinf, rawppart)
        if (pres, inf) not in lemmas_by_pres_and_inf:
            lemmas_by_pres_and_inf[(pres,inf)] = [(rawpres,rawinf,rawppart)]
        else:
            lemmas_by_pres_and_inf[(pres,inf)] .append((rawpres,rawinf,rawppart))

for k,v in lemmas_by_pres_and_inf.items():
    if len(v) > 1:
        print(k)
        for verb in v:
            print("\t", verb)
