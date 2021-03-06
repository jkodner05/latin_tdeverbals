import re, sys
from difflib import SequenceMatcher
from wikt_utils import *

lemmasfname = sys.argv[1]
outfname = sys.argv[2]

PREP_PPTC = re.compile(r"(s|m|s\ssum|m\ssum)$")

INF_1 = re.compile(r"(āre|ārī)$")
PRES_1 = re.compile(r"(ō|or)$")

INF_2 = re.compile(r"(ēre|ērī)$")
PRES_2 = re.compile(r"(eō|eor)$")

INF_3 = re.compile(r"(ere|ī|)$")
PRES_3 = re.compile(r"(ō|or)$")

INF_3i = re.compile(r"(ere|ī)$")
PRES_3i = re.compile(r"(iō|ior)$")

INF_4 = re.compile(r"(īre|īrī)$")
PRES_4 = re.compile(r"(iō|ior)$")

PERF_A = re.compile(r"āui$")
PERF_I = re.compile(r"īui$")
PERF_E = re.compile(r"ēui$")
PERF_ui = re.compile(r"uī$")
PERF_other = re.compile(r"[^u]ī$")


REMOVE_PPART_longa = re.compile(r"(ātus|ātum|ātus\ssum|ātum\ssum)$")
REMOVE_PPART_shorta = re.compile(r"(atus|atum|atus\ssum|atum\ssum)$")
REMOVE_PPART_longe = re.compile(r"(ētus|ētum|ētus\ssum|ētum\ssum)$")
REMOVE_PPART_shorte = re.compile(r"(etus|etum|etus\ssum|etum\ssum)$")
REMOVE_PPART_longi = re.compile(r"(ītus|ītum|ītus\ssum|ītum\ssum)$")
REMOVE_PPART_shorti = re.compile(r"(itus|itum|itus\ssum|itum\ssum)$")
REMOVE_PPART_consonant = re.compile(r"(tus|tum|tus\ssum|tum\ssum)$")
REMOVE_PPART_s = re.compile(r"(s+us|s+um|s+us\ssum|s+um\ssum|xus|xum|xus\ssum|xum\ssum)$")

issues = 0

def calc_H1a_45(lemmas):
    return




def find_common_forms(lemmas):

    def max_substring(forms):
        if len(forms) == 0:
            return "-"
        if len(forms) == 1:
            return forms[0]
        revforms = [vowel_red(form)[::-1] for form in forms]
        current = revforms[0]
        for form in revforms[1:]:
            s = SequenceMatcher(None, current, form)
            match = s.find_longest_match(0,len(current),0,len(form))
#            print(current[match.a:match.a+match.size][::-1], "\t", form[::-1], "\t", current[::-1])
            current = current[match.a:match.a+match.size]
        return current[::-1]

    firsts = [lem[0] for lem in lemmas]
    seconds = [lem[1] for lem in lemmas]
    thirds = [lem[2] for lem in lemmas if lem[2] != "-"]
    fourths = [lem[3] for lem in lemmas]

    first = max_substring(firsts)
    second = max_substring(seconds)
    third = max_substring(thirds)
    fourth = max_substring(fourths)

#    print(first, "\t", second, "\t", third, "\t", fourth)

    if not first or not second or not third or not fourth or first[0] != second[0] or (first[0] != third[0] and third != "-") or first[0] != fourth[0]:
        print(first, "\t", second, "\t", third, "\t", fourth)
        print(lemmas)
        print()
        global issues
        issues += 1



def main():
    lemmas = []
    with open(lemmasfname, "r") as fin:
        lemma = []
        for line in fin:
            if "\t" not in line:
                if lemma:
                    baselemma = find_common_forms(lemma)
                    lemmas.append(baselemma)
                    lemma = []
            else:
                components = line.strip().split("\t")
                #ignore verbs with no pptc
                if components[-1].strip() != "-":
                    components[-1] = PREP_PPTC.sub("", components[-1])
                    lemma.append(components[1:])

    print("ISSUES", issues)
    print(lemmas)

if __name__ == "__main__":
    main()
