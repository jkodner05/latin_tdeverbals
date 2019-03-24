import re, sys
from math import log

baselemmafname = sys.argv[1]
outfname = sys.argv[2]

class TPHypothesis:
    def __init__(self, pp1_rx, pp2_rx, pp3_rx, pp4_rx):
        self.pp1_rx = self.wrap(pp1_rx)
        self.pp2_rx = self.wrap(pp2_rx)
        self.pp3_rx = self.wrap(pp3_rx)
        self.pp4_rx = self.wrap(pp4_rx)

    def __str__(self):
        def unwrap(pp):
            if pp:
                pattern = pp.pattern[14:-1]
                while len(pattern) < 5:
                    pattern += " "
                return pattern
            else:
                return "     "
        return "pp1: " + unwrap(self.pp1_rx) + "\tpp2: " + unwrap(self.pp2_rx) + "\tpp3: " + unwrap(self.pp3_rx) + "\tpp4: " + unwrap(self.pp4_rx)

    def wrap(self, pp):
        if pp:
            wrapped = r"(^[\wāēīōū]+?)"+pp+"$"
            wrapped = wrapped.replace(")[^aeiouāēīōū]", "[^aeiouāēīōū])")
            return re.compile(wrapped)
        else:
            return None

    def get_matches(self, pparts):

        def get_match(pp_rx, pp):
            if not pp_rx:
                return ""
            if pp == "-":
                return "-"
#            print(pp)
            match = pp_rx.match(pp)
            if match:
                stem = match.group(1)
                if pp_rx.groups >= 2:
#                    print(stem)
                    stem += match.group(2)
#                    if "s" in match.group(2):
#                        stem += match.group(2)
#                    print(stem)
                return stem
            return ""

        matches = (get_match(self.pp1_rx, pparts[0]),get_match(self.pp2_rx, pparts[1]),get_match(self.pp3_rx, pparts[2]),get_match(self.pp4_rx, pparts[3]))
        if self.pp1_rx and not matches[0]:
            return None
        elif self.pp2_rx and not matches[1]:
            return None
        elif self.pp3_rx and not matches[2]:
            return None
#        elif self.pp4_rx and not matches[3]:
#            return None

        return matches


class TPHypothesisSet:
    def __init__(self, name):
        self.name = name
        self.hypotheses = []

    def __str__(self):
        return self.name

    def add_hypothesis(self, pp1=None, pp2=None, pp3=None, pp4=None):
        self.hypotheses.append(TPHypothesis(pp1, pp2, pp3, pp4))


def do_TP(N, e, disp=False):
    if disp:
        theta = N / log(N)
        print("N:", N, "\ttheta:", round(theta,4), "\te:", e, "\t\t\t\t\ttolerable?", e < theta)
    return e < N / log(N)

def construct_TPtraditional():
    traditional = TPHypothesisSet("Traditional")
    # 1st
    traditional.add_hypothesis(pp2=r"āre", pp4=r"ātu")
    # 2nd
    traditional.add_hypothesis(pp2=r"ēre", pp4=r"itu")
    traditional.add_hypothesis(pp2=r"ēre", pp4=r"[^aeiouāēīōū]([st])u")
    # 3rd non-io
    traditional.add_hypothesis(pp1=r"[^i]ō", pp2=r"ere", pp4=r"itu")
    traditional.add_hypothesis(pp1=r"[^i]ō", pp2=r"ere", pp4=r"[^aeiouāēīōū]([st])u")
    # 3rd-io
    traditional.add_hypothesis(pp1=r"iō", pp2=r"ere", pp4=r"itu")
    traditional.add_hypothesis(pp1=r"iō", pp2=r"ere", pp4=r"[^aeiouāēīōū]([st])u")
    # 3rd all
    traditional.add_hypothesis(pp2=r"ere", pp4=r"itu")
    traditional.add_hypothesis(pp2=r"ere", pp4=r"[^aeiouāēīōū]([st])u")
    # 4th
    traditional.add_hypothesis(pp2=r"īre", pp4=r"ītu")
    traditional.add_hypothesis(pp2=r"īre", pp4=r"itu")
    traditional.add_hypothesis(pp2=r"īre", pp4=r"[^aeiouāēīōū]([st])u")
    return traditional

def construct_TPpresent_rootsensitive():
    pres_rs = TPHypothesisSet("Pres, Root Sensitive")
    # 1st
    pres_rs.add_hypothesis(pp2=r"āre", pp4=r"ātu")
    # 2nd
    pres_rs.add_hypothesis(pp2=r"ēre", pp4=r"itu")
    pres_rs.add_hypothesis(pp2=r"ēre", pp4=r"[^aeiouāēīōū]([st])u")
    # 3rd non-io
    pres_rs.add_hypothesis(pp1=r"[^i]ō", pp2=r"ere", pp4=r"itu")
    pres_rs.add_hypothesis(pp1=r"[^i]ō", pp2=r"ere", pp4=r"[^aeiouāēīōū]([st])u")
    # 3rd-io
    pres_rs.add_hypothesis(pp1=r"iō", pp2=r"ere", pp4=r"itu")
    pres_rs.add_hypothesis(pp1=r"iō", pp2=r"ere", pp4=r"[^aeiouāēīōū]([st])u")
    # 3rd all
    pres_rs.add_hypothesis(pp2=r"ere", pp4=r"itu")
    pres_rs.add_hypothesis(pp2=r"ere", pp4=r"[^aeiouāēīōū]([st])u")
    # 4th
    pres_rs.add_hypothesis(pp2=r"īre", pp4=r"ītu")
    pres_rs.add_hypothesis(pp2=r"īre", pp4=r"itu")
    pres_rs.add_hypothesis(pp2=r"īre", pp4=r"[^aeiouāēīōū]([st])u")
    return pres_rs



def construct_TPHypothesisSets():
    hypothesis_sets = []
    hypothesis_sets.append(construct_TPtraditional())
    hypothesis_sets.append(construct_TPpresent_rootsensitive())
    return hypothesis_sets


def unmutate(matches):
    unmutated = list(matches)


    if unmutated[1] and unmutated[-1]:
#        if unmutated[-1][-2:] == "ss":
#            print(unmutated[1], unmutated[-1], (unmutated[1][-1] != "t" and unmutated[1][-1] != "s"), (unmutated[-1][-1] == "t" or unmutated[-1][-1] == "s"))
#        if (unmutated[1][-1] != "t" and unmutated[1][-1] != "s") and (unmutated[-1][-1] == "t" or unmutated[-1][-1] == "s"):
        if unmutated[-1][-1] in ("s","t") and unmutated[1] != unmutated[-1]:
#            if unmutated[-1][-2:] == "ss":
#                print("got", unmutated[-1][-2:] == "ss", unmutated[1], unmutated[-1])
            #undo s
            if unmutated[1][-1] in ("t", "d") and unmutated[-1][-2:] == "ss":
                unmutated[-1] = unmutated[-1][:-2] + unmutated[1][-1] + "t"
            if unmutated[1][-1] in ("t", "d") and unmutated[-1][-1] == "s":
                unmutated[-1] = unmutated[-1][:-1] + unmutated[1][-1] + "t"

            #undo final devoicing
            if unmutated[1][-1] == "b" and unmutated[-1][-2] == "p":
                unmutated[-1] = unmutated[-1][:-2] + "bt"
            elif unmutated[1][-1] == "g" and unmutated[-1][-2] == "c":
                unmutated[-1] = unmutated[-1][:-2] + "gt"
            elif unmutated[1][-1] == "h" and unmutated[-1][-2] == "c":
                unmutated[-1] = unmutated[-1][:-2] + "ht"
            #undo cluster simplification
            if unmutated[1][-1] == "m" and unmutated[-1][-3:-1] == "mp":
                unmutated[-1] = unmutated[-1][:-2] + "t"
            elif unmutated[1][-2:] == "rc" and unmutated[-1][-2:] == "rt":
                unmutated[-1] = unmutated[-1][:-1] + "ct"
            elif unmutated[1][-2:] == "lc" and unmutated[-1][-2:] == "lt":
                unmutated[-1] = unmutated[-1][:-1] + "ct"
            elif unmutated[1][-2:] == "lg" and unmutated[-1][-2:] == "lt":
                unmutated[-1] = unmutated[-1][:-1] + "gt"

            #undo lengthening
            for longv, shortv in (("ā","a"),("ē","e"),("ī","i"),("ō","o"),("ū","u")):
                replindex = unmutated[-1].rfind(longv)
                if replindex >= 0 and unmutated[1][replindex] == shortv:

                    unmutated[-1] = unmutated[-1][:replindex] + shortv + unmutated[-1][replindex+1:]

            unmutated[-1] = unmutated[-1][:-1]

    return unmutated

def test_hypothesis(baselemmas, hypothesis):
    print()
    print(hypothesis)
    N = 0
    e = 0
    for pparts in baselemmas:
        matches = hypothesis.get_matches(pparts)
        if matches:
            unmutated = unmutate(matches)
#            print(pparts, matches)
            if unmutated[-1].strip() and unmutated[-1] != "-" and unmutated[1] != unmutated[-1]:
#                print("\tIRREG MUTATION" +"\t".join(unmutated) + "\t" + " ".join(pparts))
                e += 1
            elif not unmutated[-1].strip():
#                print("\tNO PPTC MATCH" +"\t".join(unmutated) + "\t" + " ".join(pparts))
                e += 1
            N += 1
    return N, e, do_TP(N,e, disp=True)

def test_hypothesis_set(baselemmas, hypothesis_set):
    print("\n------------------\n")
    print(hypothesis_set)
    for hypothesis in hypothesis_set.hypotheses:
        N, e, is_tolerable = test_hypothesis(baselemmas,hypothesis)


def get_baselemmas(baselemmafname):
    baselemmas = []
    with open(baselemmafname, "r") as fin:
        for line in fin:
            if line.strip() and line[0] != "\t":
                components = line.split("\t")
                pp1 = components[1].strip()
                pp2 = components[2].strip()
                pp3 = components[3].strip()
                pp4 = components[4].strip()
                baselemmas.append((pp1,pp2,pp3,pp4))
    return baselemmas

def main():
    baselemmas = get_baselemmas(baselemmafname)
    hypothesis_sets = construct_TPHypothesisSets()
    for hset in hypothesis_sets:
        test_hypothesis_set(baselemmas, hset)

if __name__ == "__main__":
    main()

