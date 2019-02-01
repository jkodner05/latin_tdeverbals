# -*- coding: utf-8 -*-
import re, sys

lemmasfname = sys.argv[1]
conjugation = sys.argv[2]


INF_1 = re.compile(r"(āre|ārī)$")
REMOVE_PRES_1 = re.compile(r"(ō|or)$")

INF_2 = re.compile(r"(ēre|ērī)$")
REMOVE_PRES_2 = re.compile(r"(eō|eor)$")

INF_3 = re.compile(r"(ere|ī|)$")
INF_3i = re.compile(r"(ere|ī)$")
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


INF = INF_1
REMOVE_PRES = REMOVE_PRES_1
NOT_INFS = []
NOT_PRESS = []
if conjugation == "1":
    INF = INF_1
    REMOVE_PRES = REMOVE_PRES_1
elif conjugation == "2":
    INF = INF_2
    REMOVE_PRES = REMOVE_PRES_2
elif conjugation == "3":
    INF = INF_3
    REMOVE_PRES = REMOVE_PRES_3
    NOT_INFS = [INF_1,INF_2,INF_4]
    NOT_PRESS = [REMOVE_PRES_3i]
elif conjugation == "3i":
    INF = INF_3i
    REMOVE_PRES = REMOVE_PRES_3i
    NOT_INFS = [INF_1,INF_2,INF_4]
elif conjugation == "4":
    INF = INF_4
    REMOVE_PRES = REMOVE_PRES_4
else:
    print("INVALID CONJUGATION NUMBER")
    exit()

form_map = {}
verblist = []
with open(lemmasfname,"r") as fin:

    verbs = set([])
    for line in fin:
        pres = line.split("\t")[0].strip()
        inf = line.split("\t")[1].strip()
        ppart = line.split("\t")[2].strip()
        if INF.findall(inf) and REMOVE_PRES.findall(pres):
            got_not = False
            for not_inf in NOT_INFS:
                if not_inf.findall(inf):
                    got_not = True
            for not_pres in NOT_PRESS:
                if not_pres.findall(pres):
                    got_not = True
            if not got_not:
                verbs.add((pres,inf,ppart))
#            print(pres,inf,ppart)

#    print(len(list(verbs)))
verblist = list(verbs)



numskip = 0
num_longa = 0
num_shorta = 0
num_longe = 0
num_shorte = 0
num_longi = 0
num_shorti = 0
num_consonant = 0
num_s = 0
num_other = 0
num_none = 0
num_consonant_len = 0
num_s_len = 0

num_longa_shorta = 0
num_consonant_consonant_len_other = 0
num_longe_shorte = 0
num_longi_shorti = 0
num_consonant_other = 0
num_consonant_s = 0
num_s_other = 0
num_consonant_consonant_len = 0
num_s_s_len = 0
num_longa_shorti = 0
num_longa_other = 0
num_consonant = 0

multiples = []
others = []
for pres, inf, pparts in verblist:


    pres_base = REMOVE_PRES.sub("",pres)

    got_longa = False
    got_shorta = False
    got_longe = False
    got_shorte = False
    got_longi = False
    got_shorti = False
    got_consonant = False
    got_s = False
    got_other = False
    got_none = False
    got_consonant_len = False
    got_s_len = False

    for ppart in pparts.split("/"):
        ppart_longa = REMOVE_PPART_longa.sub("",ppart)
        ppart_shorta = REMOVE_PPART_shorta.sub("",ppart)
        ppart_longe = REMOVE_PPART_longe.sub("",ppart)
        ppart_shorte = REMOVE_PPART_shorte.sub("",ppart)
        ppart_longi = REMOVE_PPART_longi.sub("",ppart)
        ppart_shorti = REMOVE_PPART_shorti.sub("",ppart)
        ppart_consonant = REMOVE_PPART_consonant.sub("",ppart)
        ppart_s = REMOVE_PPART_s.sub("",ppart)

        if pres_base == ppart_longa:
            got_longa = True
        elif pres_base == ppart_shorta:
            got_shorta = True
        elif pres_base == ppart_longe:
            got_longe = True
        elif pres_base == ppart_shorte:
            got_shorte = True
        elif pres_base == ppart_longi:
            got_longi = True
        elif pres_base == ppart_shorti:
            got_shorti = True
        elif pres_base == ppart_consonant:
            got_consonant = True
        elif pres_base == ppart_s:
            got_s = True
        elif ppart == "-":
            got_none = True
        else:
            pres_cons = pres_base + " "
            pres_cons = pres_cons.replace("g ", "c ").replace("h ", "c ").replace("m ", "mp ").replace("b ", "p ").replace("qu ", "cū ").replace("u ", "ū ")
            pres_cons = pres_cons.replace("ar ", "as ").replace("er ", "es ").replace("ir ", "is ").replace("or ", "os ").replace("ur ", "us ")
            pres_cons = pres_cons.replace("ār ", "ās ").replace("ēr ", "ēs ").replace("īr ", "īs ").replace("ōr ", "ōs ").replace("ūr ", "ūs ").replace("isc "," ")
            pres_cons = pres_cons.replace("rc ", "r ").replace("lc ", "l ")

            pres_s = pres_base + " "
            pres_s = pres_s.replace("tt ", " ").replace("ct ", " ").replace("d ", " ").replace("t ", " ").replace("ll ", "l ").replace("rr ", "r ").replace("s ", " ")

            pres_nolen = pres_base.replace("ā", "a").replace("ē", "e").replace("ī", "i").replace("ō", "o").replace("ū", "u")
            pres_cons_nolen = pres_cons.replace("ā", "a").replace("ē", "e").replace("ī", "i").replace("ō", "o").replace("ū", "u")
            ppart_cons_nolen = ppart_consonant.replace("ā", "a").replace("ē", "e").replace("ī", "i").replace("ō", "o").replace("ū", "u")
            pres_s_nolen = pres_s.replace("ā", "a").replace("ē", "e").replace("ī", "i").replace("ō", "o").replace("ū", "u")
            ppart_s_nolen = ppart_s.replace("ā", "a").replace("ē", "e").replace("ī", "i").replace("ō", "o").replace("ū", "u")

            pres_ie = pres_nolen.replace("i","e")
            pres_ie_nolen = pres_nolen.replace("i","e")
            pres_s_ie = pres_s.replace("i","e")
            pres_s_ie_nolen = pres_s_nolen.replace("i","e")

            if pres_cons.strip() == ppart_consonant:
                got_consonant = True
            elif pres_s.strip() == ppart_s:
                got_s = True
            elif pres_ie == ppart_consonant:
                got_consonant = True
            elif pres_s_ie.strip() == ppart_s:
                got_s = True
            elif pres_cons_nolen.strip() == ppart_cons_nolen:
                got_consonant_len = True
            elif pres_s_nolen.strip() == ppart_s_nolen:
                got_s_len = True
            else:
                got_other = True
            


    if got_longa and got_shorta:
        num_longa_shorta += 1
        multiples.append((pres, inf, pparts))
    elif got_consonant and got_consonant_len and got_other:
        num_consonant_consonant_len_other += 1
        multiples.append((pres, inf, pparts))
    elif got_longe and got_shorte:
        num_longe_shorte += 1
        multiples.append((pres, inf, pparts))
    elif got_longi and got_shorti:
        num_longi_shorti += 1
        multiples.append((pres, inf, pparts))
    elif got_consonant and got_other:
        num_consonant_other += 1
        multiples.append((pres, inf, pparts))
    elif got_consonant and got_s:
        num_consonant_s += 1
        multiples.append((pres, inf, pparts))
    elif got_s and got_other:
        num_s_other += 1
        multiples.append((pres, inf, pparts))
    elif got_consonant and got_consonant_len:
        num_consonant_consonant_len += 1
        multiples.append((pres, inf, pparts))
    elif got_s and got_s_len:
        num_s_s_len += 1
        multiples.append((pres, inf, pparts))
    elif got_longa and got_shorti:
        num_longa_shorti += 1
        multiples.append((pres, inf, pparts))
    elif got_longa and got_other:
        num_longa_other += 1
        multiples.append((pres, inf, pparts))
    elif got_longa and got_consonant:
        num_consonant += 1
        multiples.append((pres, inf, pparts))
    elif got_other:
        num_other += 1
        others.append((pres,inf,pparts))
    elif got_longa:
        num_longa += 1
    elif got_shorta:
        num_shorta += 1
    elif got_longi:
        num_longi += 1
    elif got_shorte:
        num_shorte += 1
    elif got_longi:
        num_longi += 1
    elif got_shorti:
        num_shorti += 1
    elif got_consonant:
        num_consonant += 1
    elif got_s:
        num_s += 1
    elif got_consonant_len:
        num_consonant_len += 1
    elif got_s_len:
        num_s_len += 1



print("")
print("OTHERS:\n")
for other in others:
    print(other)
print("\nMULTIPLES:\n")
for multiple in multiples:
    print(multiple)
print("\n\n")
print("LONG A:\t\t" + str(num_longa))
print("SHORT A:\t" + str(num_shorta))
print("LONG E:\t\t" + str(num_longe))
print("SHORT E:\t" + str(num_shorte))
print("LONG I:\t\t" + str(num_longi))
print("SHORT I:\t" + str(num_shorti))
print("CONSONANT:\t" + str(num_consonant))
print("   +LEN:\t" + str(num_consonant_len))
print("S:\t\t" + str(num_s))
print("   +LEN:\t" + str(num_s_len))
print("OTHER:\t\t" + str(num_other))
print("-------------------")
singletotal = num_longa+num_shorta+num_longe+num_shorte+num_longi+num_shorti+num_consonant+num_consonant_len+num_s+num_s_len+num_other
print("TOTAL:\t\t" + str(singletotal))
print("-------------------\n")
print("LONGA & SHORTA:\t" + str(num_longa_shorta))
print("LONGE & SHORTE:\t" + str(num_longe_shorte))
print("LONGI & SHORTI:\t" + str(num_longi_shorti))
print("LONGA & SHORTI:\t" + str(num_longa_shorti))
print("LONGA & OTHER:\t" + str(num_longa_other))
print("C&C+LEN&O:\t" + str(num_consonant_consonant_len_other))
print("C & C+LEN:\t" + str(num_consonant_consonant_len))
print("CONS & OTHER:\t" + str(num_consonant_other))
print("CONS & S:\t" + str(num_consonant_s))
print("S & OTHER:\t" + str(num_s_other))
print("S & S+LEN:\t" + str(num_s_s_len))
print("-------------------")
print("GRAND TOTAL:\t" + str(singletotal + num_longa_shorta + num_longe_shorte + num_longi_shorti + num_longa_shorti + num_longa_other + num_consonant_consonant_len_other + num_consonant_consonant_len + num_consonant_other + num_consonant_s + num_s_other + num_s_s_len))

