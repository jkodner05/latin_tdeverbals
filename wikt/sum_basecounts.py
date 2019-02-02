import re, sys

spacedfname = sys.argv[1]
outfname = sys.argv[2]

def main():
    inlines = []
    with open(spacedfname, "r") as f:
        inlines = [line for line in f]
        inlines.reverse()
    basefreq = 0
    outlines = []
    for line in inlines:
        if not line.strip():
            outlines.append(str(basefreq) + "\n")
            outlines.append(line)
            basefreq = 0
        else:
            freq = int(line.split("\t")[0].strip())
            basefreq += freq
            outlines.append("\t"+line)
    outlines.append(str(basefreq) + "\n")

    with open(outfname, "w") as f:
        outlines.reverse()
        for line in outlines:
            f.write(line)

if __name__ == "__main__":
    main()

