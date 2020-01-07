import re, sys
import statistics

baselemmafname = sys.argv[1]
outfname = sys.argv[2]
rankcutoff = int(sys.argv[3])

def read_baselemmas():
    baselemmacounts = {}
    with open(baselemmafname, "r") as fin:
        for line in fin:
            if not line.strip() or line[0] != "\t":
                continue

            comps = line.strip().split("\t")
            freq = int(comps[0].strip())
            lemma = comps[1].strip()
            if lemma not in baselemmacounts:
                baselemmacounts[lemma] = set([])
            baselemmacounts[lemma].add(freq)
    avglemmacounts = {}
    for lemma, freqs in baselemmacounts.items():
        avglemmacounts[lemma] = statistics.mean(freqs)
    sortedlemmas = sorted(avglemmacounts.items(), key=lambda kv : kv[1], reverse=True)[0:rankcutoff]
    return sortedlemmas

def write_avglemmacounts(sortedlemmas):
    with open(outfname, "w") as fout:
        for lemma, freq in sortedlemmas:
            fout.write(str(freq) + "\t" + lemma + "\n")

def main():
    sortedlemmas = read_baselemmas()
    write_avglemmacounts(sortedlemmas)

if __name__ == "__main__":
    main()

