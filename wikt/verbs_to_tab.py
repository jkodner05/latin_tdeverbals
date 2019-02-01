import re, sys
from os import listdir
from os.path import isfile, join

FIND_Pres = re.compile(r"<p><strong class=\"Latn headword\" lang=\"la\">(\w+)<")
FIND_Inf = re.compile(r"present infinitive</i> <b class=\"Latn\" lang=\"la\">.*?title=\".+?\">([^\s]+?)</a></b>")
FIND_Perf = re.compile(r"perfect active</i> <b class=\"Latn\" lang=\"la\">.*?title=\".+?\">(.+?)</a></b>")
FIND_Sup = re.compile(r"supine</i> <b class=\"Latn\" lang=\"la\">.*?title=\".+?\">([^\s]+?)</a></b>")


path = sys.argv[1]

verb_pages = [f for f in listdir(path) if isfile(join(path, f))]

for fname in verb_pages:
    in_latin = False
    etym_next = False

    compound = ""

    pres = ""
    ppart = "-"
    inf = "-"

    with open(join(path,fname), "r") as f:

        for line in f:
            #Find start of Latin section
            if """<span class="mw-headline" id="Latin">Latin</span>""" in line:
                in_latin = True
                continue
            if not in_latin:
                continue

            #get etymological info. Assuming + implies compounds
            if """<h3><span class="mw-headline" id="Etymology""" in line:
                etym_next = True
                continue
            if etym_next:
                if "+" in line:
                    compound += "+"

            #get principle parts
            PParts = FIND_Pres.match(line)
            if PParts:
                if "infinitive" not in line and "conjugation" not in line:
                    continue
                pres = PParts.group(1)

#                print(PParts.group(0), PParts.group(1))
                Inf = FIND_Inf.search(line)
                if Inf:
                    inf = Inf.group(1)
#                    print(Inf.group(0), Inf.group(1))
#                Perf = FIND_Perf.search(line)
#                if Perf:
#                    print(Perf.group(0), Perf.group(1))
                Sup = FIND_Sup.search(line)
                if Sup:
                    ppart = Sup.group(1)
                elif "deponent" in line:
                    Perf = FIND_Perf.search(line)
                    if Perf:
                        ppart = Perf.group(1)

                print(pres + "\t" + inf + "\t" + ppart + "\t\t" + compound.strip())
#                    if "deponent" not in line:
#                        print(line)
#                    print(Sup.group(0), Sup.group(1))


#                print("")

