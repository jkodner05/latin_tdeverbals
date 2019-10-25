import re, sys
from math import log, floor

baselemmafname = sys.argv[1]
#outfname = sys.argv[2]

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
    theta = 0
    if N > 1:
        theta = N / log(N)
    if disp:
        if e >= theta:
            print("N:", N, "\ttheta:", round(theta,4), "\te:", e, "\t\t\t\t\ttolerable?", e < theta, "\tgap: ", e-floor(theta))#, "(", round(max(1,e-floor(theta))/N*100,4), "%)")
        else:
            print("N:", N, "\ttheta:", round(theta,4), "\te:", e, "\t\t\t\t\ttolerable?", e < theta)
    return e < theta

def construct_TPtraditional():
    traditional = TPHypothesisSet("Traditional")
    # 1st
    traditional.add_hypothesis(pp2=r"āre", pp4=r"ātu")
    # 2nd
    traditional.add_hypothesis(pp2=r"ēre", pp4=r"itu")
    traditional.add_hypothesis(pp2=r"ēre", pp4=r"[^aeiouāēīōū]([st])u")
    # 3rd non-io
    traditional.add_hypothesis(pp1=r"([^i])ō", pp2=r"ere", pp4=r"itu")
    traditional.add_hypothesis(pp1=r"([^i])ō", pp2=r"ere", pp4=r"[^aeiouāēīōū]([st])u")
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
    pres_rs = TPHypothesisSet("Present, Root Sensitive")
    # 2nd Vueo
    pres_rs.add_hypothesis(pp1 = "([ao]u)eō", pp2=r"ēre", pp4=r"(((au)|ō)t)u")
    # 2nd post velar
    pres_rs.add_hypothesis(pp1 = "(c|g|h|(qu))eō", pp2=r"ēre", pp4=r"[^aeiouāēīōū]([st])u")
    pres_rs.add_hypothesis(pp1 = "(c|g|h|(qu))eō", pp2=r"ēre", pp4=r"itu")
    # 2nd otherwise
    pres_rs.add_hypothesis(pp1 = "[^(c|g|h|(qu))]eō", pp2=r"ēre", pp4=r"[^aeiouāēīōū]([st])u")
    pres_rs.add_hypothesis(pp1 = "[^(c|g|h|(qu))]eō", pp2=r"ēre", pp4=r"itu")
    # 3rd u
    pres_rs.add_hypothesis(pp1=r"uō", pp2=r"uere", pp4=r"ūtu")
    # 3rd RR
    # by hand...
    pres_rs.add_hypothesis(pp1=r"(l|r)(l|r)ō", pp2=r"ere", pp4=r"([lr]s)u")
    # 3rd K-V-sc
    pres_rs.add_hypothesis(pp1=r"[c|g|h][aeiouāēīōū]scō", pp2=r"[aeiouāēīōū]scere", pp4=r"([^aeiouāēīōū]t)u")
    # 3rd V-sc
    pres_rs.add_hypothesis(pp1=r"[^(c|g|h)][aeiouāēīōū]scō", pp2=r"scere", pp4=r"([aeiouāēīōū]t)u")
    pres_rs.add_hypothesis(pp1=r"[^(c|g|h)][aeiouāēīōū]scō", pp2=r"[aeiouāēīōū]scere", pp4=r"itu")
    # 3rd-io
#    pres_rs.add_hypothesis(pp1=r"iō", pp2=r"ere", pp4=r"itu")
    pres_rs.add_hypothesis(pp1=r"iō", pp2=r"ere", pp4=r"[^aeiouāēīōū]([st])u")
    # 3rd otherwise
#    pres_rs.add_hypothesis(pp1=r"[^(ll|rr)][^iu]ō", pp2=r"ere", pp4=r"itu")
    pres_rs.add_hypothesis(pp1=r"[^(ll|rr)][^iu]ō", pp2=r"ere", pp4=r"[^aeiouāēīōū]([st])u")
    return pres_rs

def construct_TPperfect_rootsensitive():
    perf_rs = TPHypothesisSet("Perfect, Root Sensitive")
    # VVvi
    perf_rs.add_hypothesis(pp3=r"āuī", pp4=r"ātu")
    perf_rs.add_hypothesis(pp3=r"īuī", pp4=r"ītu")
    perf_rs.add_hypothesis(pp3=r"ēuī", pp4=r"ētu")
    perf_rs.add_hypothesis(pp3=r"[āīē]uī", pp4=r"[āīē]tu")
    # evi itus
    perf_rs.add_hypothesis(pp3=r"ēuī", pp4=r"itu")
    # ui
    perf_rs.add_hypothesis(pp3=r"([^āīē])uī", pp4=r"itu")
    perf_rs.add_hypothesis(pp3=r"([^āīē])uī", pp4=r"[^aeiouāēīōū]([st])u")
    # ui post velar
    perf_rs.add_hypothesis(pp3 = "(c|g|h|q)uī", pp4=r"itu")
    perf_rs.add_hypothesis(pp3 = "(c|g|h|q)uī", pp4=r"[^aeiouāēīōū]([st])u")
    # ui post non-velar
    perf_rs.add_hypothesis(pp3 = "([^(c|g|h|q|ā|ī|ē)])uī", pp4=r"itu")
    perf_rs.add_hypothesis(pp3 = "([^(c|g|h|q|ā|ī|ē)])uī", pp4=r"[^aeiouāēīōū]([st])u")
    # si
    perf_rs.add_hypothesis(pp3=r"sī", pp4=r"[^aeiouāēīōū]([st])u")
    perf_rs.add_hypothesis(pp3=r"sī", pp4=r"([aeiouāēīōū]s)u")
    # Csi 
    perf_rs.add_hypothesis(pp3=r"([^aeiouāēīōū])sī", pp4=r"[^aeiouāēīōū]([st])u")
    # Vsi
    perf_rs.add_hypothesis(pp3=r"([aeiouāēīōū]s)ī", pp4=r"([aeiouāēīōū]s)u")
    # other stem change
    perf_rs.add_hypothesis(pp3=r"([^us])ī", pp4=r"[^aeiouāēīōū]([st])u")
    return perf_rs


def construct_TPpresperf_rootsensitive():
    presperf_rs = TPHypothesisSet("Present + Perfect, Root Sensitive")
    # 1st/4th ui
    presperf_rs.add_hypothesis(pp2="āre", pp3=r"([^āīē])uī", pp4=r"itu")
    presperf_rs.add_hypothesis(pp2="īre", pp3=r"([^āīē])uī", pp4=r"[^aeiouāēīōū]([st])u")
    presperf_rs.add_hypothesis(pp2="[āī]re", pp3=r"([^āīē])uī", pp4=r"itu")
    presperf_rs.add_hypothesis(pp2="[āī]re", pp3=r"([^āīē])uī", pp4=r"[^aeiouāēīōū]([st])u")
    # 2nd ui
    presperf_rs.add_hypothesis(pp2="ēre", pp3=r"([^āīē])uī", pp4=r"itu")
    presperf_rs.add_hypothesis(pp2="ēre", pp3=r"([^āīē])uī", pp4=r"[^aeiouāēīōū]([st])u")
    # 3rd ui
    presperf_rs.add_hypothesis(pp2="ere", pp3=r"([^āīē])uī", pp4=r"itu")
    presperf_rs.add_hypothesis(pp2="ere", pp3=r"([^āīē])uī", pp4=r"[^aeiouāēīōū]([st])u")
    # other stem change
    presperf_rs.add_hypothesis(pp2="ere", pp3=r"([^us])ī", pp4=r"[^aeiouāēīōū]([st])u")
    presperf_rs.add_hypothesis(pp2="īre", pp3=r"([^us])ī", pp4=r"[^aeiouāēīōū]([st])u")
    #UTU
    presperf_rs.add_hypothesis(pp2="uere", pp3=r"([^āīē])uī", pp4=r"ūtu")
    return presperf_rs



def unmutate(matches):
    unmutated = list(matches)

    def unfinaldevoice(left, pptc):
        if left[-1] == "b" and pptc[-2] == "p":
            pptc = pptc[:-2] + "bt"
        elif left[-1] == "g" and pptc[-2] == "c":
            pptc = pptc[:-2] + "gt"
        elif left[-1] == "h" and pptc[-2] == "c":
            pptc = pptc[:-2] + "ht"
        return left, pptc

    def unclustersimplify(left, pptc):
        if left[-1] == "m" and pptc[-3:-1] == "mp":
            pptc = pptc[:-2] + "t"
        elif left[-2:] == "mn" and pptc[-3:-1] == "mp":
            pptc = pptc[:-2] + "nt"
        elif left[-2:] == "rc" and pptc[-2:] == "rt":
            pptc = pptc[:-1] + "ct"
        elif left[-3:] == "rqu" and pptc[-2:] == "rt":
            pptc = pptc[:-1] + "qut"
        elif left[-2:] == "lc" and pptc[-2:] == "lt":
            pptc = pptc[:-1] + "ct"
        elif left[-2:] == "lg" and pptc[-2:] == "lt":
            pptc = pptc[:-1] + "gt"

        if len(left) >= 3 and len(pptc) >= 4:
            if left[-2] == "i" and pptc[-3] == "e":
                pptc = pptc[:-3] + "i" + pptc[-2:] 
            elif left[-2] == "o" and pptc[-3] == "u":
                pptc = pptc[:-3] + "o" + pptc[-2:] 

        return left, pptc

    def unlengthen(left, pptc):
        for longv, shortv in (("ā","a"),("ē","e"),("ī","i"),("ō","o"),("ū","u")):
            replindex = pptc.rfind(longv)
            if len(left) > replindex and replindex >= 0 and left[replindex] == shortv:
                pptc = pptc[:replindex] + shortv + pptc[replindex+1:]
        return left, pptc
    
    if unmutated[-1]:
        if unmutated[1] and unmutated[2]:
            if unmutated[-1][-1] in ("s","t") and unmutated[1] != unmutated[-1]:
                #undo s
                if unmutated[1][-1] in ("t", "d") and unmutated[-1][-2:] == "ss":
                    unmutated[-1] = unmutated[-1][:-2] + unmutated[1][-1] + "t"
                if unmutated[1][-1] in ("t", "d") and unmutated[-1][-1] == "s":
                    unmutated[-1] = unmutated[-1][:-1] + unmutated[1][-1] + "t"
                #undo final devoicing
                unmutated[1], unmutated[-1] = unfinaldevoice(unmutated[1], unmutated[-1])
                #undo cluster simplification
                unmutated[1], unmutated[-1] = unclustersimplify(unmutated[1], unmutated[-1])
                #undo lengthening
                if unmutated[-1][-2] == "ō":
                    unmutated[-1] = unmutated[-1][:-2] + "out"
                unmutated[1], unmutated[-1] = unlengthen(unmutated[1], unmutated[-1])
        elif unmutated[1]:
            if unmutated[-1][-1] in ("s","t") and unmutated[1] != unmutated[-1]:
                #undo s
                if unmutated[1][-1] in ("t", "d") and unmutated[-1][-2:] == "ss":
                    unmutated[-1] = unmutated[-1][:-2] + unmutated[1][-1] + "t"
                if unmutated[1][-1] in ("t", "d") and unmutated[-1][-1] == "s":
                    unmutated[-1] = unmutated[-1][:-1] + unmutated[1][-1] + "t"
                #undo final devoicing
                unmutated[1], unmutated[-1] = unfinaldevoice(unmutated[1], unmutated[-1])
                #undo cluster simplification
                unmutated[1], unmutated[-1] = unclustersimplify(unmutated[1], unmutated[-1])
                #undo lengthening
                if len(unmutated[-1]) > 2 and  unmutated[-1][-2] == "ō":
                    unmutated[-1] = unmutated[-1][:-2] + "out"
                unmutated[1], unmutated[-1] = unlengthen(unmutated[1], unmutated[-1])
        elif unmutated[2]:
            if unmutated[-1][-1] in ("s","t") and unmutated[2] != unmutated[-1]:
                #undo s
                if unmutated[2][-1] in ("t", "d") and unmutated[-1][-2:] == "ss":
                    unmutated[-1] = unmutated[-1][:-2] + unmutated[2][-1] + "t"
                if unmutated[2][-1] in ("t", "d") and unmutated[-1][-1] == "s":
                    unmutated[-1] = unmutated[-1][:-1] + unmutated[2][-1] + "t"
                #decompose x
                if unmutated[2][-1] == "x":
                    unmutated[2] = unmutated[2][:-1] + "c"
                #undo final devoicing
                unmutated[2], unmutated[-1] = unfinaldevoice(unmutated[2], unmutated[-1])
                #undo cluster simplification
                unmutated[2], unmutated[-1] = unclustersimplify(unmutated[2], unmutated[-1])
                #undo lengthening
                unmutated[2], unmutated[-1] = unlengthen(unmutated[2], unmutated[-1])


        #q
        unmutated[-1] = unmutated[-1].replace("q","c")
        unmutated[1] = unmutated[1].replace("q","c")
        unmutated[2] = unmutated[2].replace("q","c")

        if unmutated[-1][-1] in ("s","t") and unmutated[1] != unmutated[-1] and unmutated[2] != unmutated[-1]:
            unmutated[-1] = unmutated[-1][:-1]

    return unmutated


def construct_TPHypothesisSets():
    hypothesis_sets = []
    hypothesis_sets.append(construct_TPtraditional())
    hypothesis_sets.append(construct_TPpresent_rootsensitive())
    hypothesis_sets.append(construct_TPperfect_rootsensitive())
    hypothesis_sets.append(construct_TPpresperf_rootsensitive())
    return hypothesis_sets


def test_hypothesis(baselemmas, hypothesis):
    disp = True
    print()
    print(hypothesis)
    N = 0
    e = 0
    exceptions = []
    for pparts in baselemmas:
        matches = hypothesis.get_matches(pparts)
        if matches:
            unmutated = unmutate(matches)
#            print(pparts, matches)
            if unmutated[1].strip() and unmutated[-1] != "-" and unmutated[1] != unmutated[-1] and unmutated[-1].strip():
                if disp:
                    print("\tIRREG MUTATION  " +"\t".join(unmutated) + "\t" + " ".join(pparts))
                e += 1
            elif not unmutated[1].strip() and unmutated[-1].strip() and unmutated[2].strip() and unmutated[2].strip() != "-" and unmutated[-1] != "-" and unmutated[2] != unmutated[-1]:
                if disp:
                    print("\tIRREG MUTATION  " +"\t".join(unmutated) + "\t" + " ".join(pparts))
                e += 1
            elif not unmutated[-1].strip() and (unmutated[2] != "-" or not hypothesis.pp3_rx):
                if disp:
                    print("\tNO PPTC MATCH  " +"\t".join(unmutated) + "\t" + " ".join(pparts))
                e += 1
            elif unmutated[-1] != "-" and (unmutated[2] != "-" or not hypothesis.pp3_rx):
                if disp:
                    print("\tGOOD!\t  " +"\t".join(unmutated) + "\t" + " ".join(pparts))
            if unmutated[-1] != "-" and (unmutated[2] != "-" or not hypothesis.pp3_rx):
                N += 1
    print("result: ", hypothesis)
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
                components = line.replace("x","cs").split("\t")
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

