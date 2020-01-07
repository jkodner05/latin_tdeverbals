import re
from os import walk
from os.path import isfile, join
from cltk.stem.latin.j_v import JVReplacer

STATSBASE = "stats"
REMOVE_DIGITS = re.compile(r"\d")
JV = JVReplacer()

def clean_word(word):
    return JV.replace(REMOVE_DIGITS.sub("",word.strip()))


def process_unk(forms):
    rn_rx = re.compile(r"[iuxlcdm_\.]*")
    prefixlen_default = 20
    prefixlen = prefixlen_default
    prefixes = {}
    skips = set(["m","b","s","r","e","u","i","o","a"])
    for form in forms:
        if not form:
            continue
#        print(form, len(form), prefixlen, (len(form) >= prefixlen and form[prefixlen-1] in skips))
        while len(form) < prefixlen or (len(form) >= prefixlen and form[prefixlen-1] in skips):
            prefixlen -= 1
            if prefixlen < 0:
                prefixlen = len(form)
                break
        prefix = form[0:prefixlen]
        if not rn_rx.sub("",form):
            prefix = "~NUMBER"
        if prefix not in prefixes:
            prefixes[prefix] = set([])
        prefixes[prefix].add(form)
        prefixlen = prefixlen_default

    sortedprefixes = sorted(prefixes.items(), key=lambda kv : kv[0])
#    print(sortedprefixes)
    for prefix, forms in sortedprefixes:
        if len(forms) == 1:
            print(list(forms)[0])
        else:
            print(prefix, "\t", len(forms), "\t", ", ".join(list(forms)))
                  

def collate_lemmaforms(infnameext, outfname):
    lemmaforms = {}
    for subdir, dirs, fnames in walk(STATSBASE):
        for fname in fnames:
            if infnameext in fname:
                with open(join(STATSBASE,fname), "r") as f:
                    for line in f:
                        components = line.split("\t")
                        lemma = clean_word(components[0])
                        forms = set(clean_word(components[1]).split(","))
                        if lemma not in lemmaforms:
                            lemmaforms[lemma] = set([])
                        lemmaforms[lemma] = lemmaforms[lemma].union(forms)

    process_unk(lemmaforms["UNK"])

    sortedlemmaforms = sorted(lemmaforms.items(), key=lambda kv : kv[0])
    with open(join(STATSBASE,outfname), "w") as f:
        for lemma, forms in sortedlemmaforms:
            f.write(lemma + "\t")
            f.write(",".join(sorted(list(forms))) + "\n")
    

def collate_counts(infnameext, outfname):
    wordcounts = {}
    for subdir, dirs, fnames in walk(STATSBASE):
        for fname in fnames:
            if infnameext in fname:
                with open(join(subdir,fname), "r") as f:
                    for line in f:
                        components = line.split("\t")
                        count = int(components[0])
                        word = clean_word(components[1])
                        if word not in wordcounts:
                            wordcounts[word] = 0
                        wordcounts[word] += count

    sortedwordcounts = sorted(wordcounts.items(), key=lambda kv : kv[1], reverse=True)
    with open(join(STATSBASE,outfname), "w") as f:
        for word, count in sortedwordcounts:
            f.write(str(count))
            f.write("\t" + word + "\n")
    print(outfname + ":\t" + str(len(wordcounts.keys())) + "\t" + str(sum(wordcounts.values())))


def extract_bysuff(infname, outfname, include=[], exclude=[]):
    tokencount = 0
    typecount = 0
    with open(join(STATSBASE,infname), "r") as fin:
        with open(join(STATSBASE,outfname), "w") as fout:
            for line in fin:
                components = line.split("\t")
                count = int(components[0])
                word = components[1].strip() + " "
                for inc in include:
                    if inc in word:
                        excluded = False
                        for exc in exclude:
                            if exc in word:
                                excluded = True
                                break
                        if not excluded:
                            fout.write(str(count))
                            fout.write("\t" + word + "\n")
                            tokencount += count
                            typecount += 1
    print(outfname + ":\t" + str(typecount) + "\t" + str(tokencount))


def main():
    collate_counts("_fc.txt", "formcounts.txt")
    collate_counts("_lc.txt", "lemmacounts.txt")
    collate_lemmaforms("_lf.txt", "lemmaforms.txt")

    extract_bysuff("lemmacounts.txt", "verb_lemmacounts.txt", include=("o ", "or "), exclude=("tio ", "sio ", "tor ", "sor "))
    extract_bysuff("lemmacounts.txt", "tdeverb_lemmacounts.txt", include=("tor ", "sor ", "tio ", "sio ", "tura ", "sura ", "tim ", "sim ", "turus " "surus "))

if __name__ == "__main__":
    main()
