import re, sys

baselemmafname = sys.argv[1]
outfname = sys.argv[2]
rankcutoff = int(sys.argv[3])

def read_baselemmas():
    baselemmafreqs = {}
    with open(baselemmafname, "r") as fin:
        freq = 0
        lemma = []
        lines = [line for line in fin]
        lines.reverse()
        for line in lines:
            if line.strip() and line[0] != "\t":
                freq = (int(line.strip().split("\t")[0]), line.strip())
                if line.split("\t")[-1] == "-" and line.split("\t")[-2] == "-":
                    lemma = []
                    continue
                baselemmafreqs["\n".join(lemma)] = freq
                lemma = []
            else:
                lemma.append(line.strip())

    sortedlemmas = sorted(baselemmafreqs.items(), key=lambda kv : kv[1][0], reverse=True)[0:rankcutoff]
    return sortedlemmas


def write_baselemmas(sortedlemmas):
    with open(outfname, "w") as fout:
        for lemmas, freq in sortedlemmas:
#            print()
#            print(freq)
#            print(lemmas.strip()+"\n")
            fout.write(freq[1] + "\n")
#            fout.write("\n"+freq[1]+"\n\t"+lemmas.strip().replace("\n","\n\t")+"\n")

def main():
    sortedlemmas = read_baselemmas()
    write_baselemmas(sortedlemmas)

if __name__ == "__main__":
    main()

