import re
from os import listdir, walk
from os.path import isfile, join, exists, basename, expanduser

STATSBASE = "stats"

decl1 = "(a|am|ae|ae|a|ae|as|arum|is|is|abus)"
decl2 = "(us|um|i|o|o|i|os|orum|is|is)"
decl3 = "(is|em|is|i|e|es|es|um|ibus|ibus|ium)"
decl4 = "(us|um|us|ui|u|us|us|uum|ibus|ibus|ubus)"
decl12 = "("+decl1+"|"+decl2+")"
decl12s = "("+decl1+"|"+decl2+"|(u)"+")"

none_rx = re.compile(r"^$")
pptc_rx = re.compile(r"(.*?(t|s))"+decl12s+"$")
adv_rx = re.compile(r"(.*?(t|s))im$")
agent_rx = re.compile(r"(.*?(t|s))or"+decl3+"?$")
event1_rx = re.compile(r"(.*?(t|s))io(n"+decl3+")?$")
event2_rx = re.compile(r"(.*?(t|s))"+decl4+"$")
fptc_rx = re.compile(r"(.*?(t|s))ur("+decl1+"|"+decl2+")$")
result_rx = re.compile(r"(.*?(t|s))ur"+decl1 + "$")

notpptc_rx = re.compile(r"(.*?)(^[ts]"+decl12s+"|.*?itat"+decl3+"|^legat"+decl12s+"|^int"+decl12s+"|^subit"+decl12s+"|^poet"+decl12s+"|^quart"+decl12s+"|^quint"+decl12s+"|^uoluptat"+decl12s+"|^sext"+decl12s+"|^marit"+decl12s+"|^beat"+decl12s+"|^auctorit"+decl12s+"|^piet"+decl12s+"|^mult"+decl12s+"|^senat"+decl12s+"|^sat"+decl12s+"|^est"+decl12s+"|^quant"+decl12s+"|^humanitas|^liberalitas|^coet"+decl12s+"|^digit"+decl12s+"|^grauit"+decl12s+"|^salut"+decl12s+"|^uelut"+decl12s+"|^nis"+decl12s+"|^quas"+decl12s+"|^caus"+decl12s+"|^uit"+decl12s+"|^medicament"+decl12s+"|^monument"+decl12s+"|^iument"+decl12s+"|^uoluntat"+decl12s+"|^paupert"+decl12s+"|^ut"+decl12s+"|^senect"+decl12s+"|^etiams"+decl12s+"|^crass"+decl12s+"|^uult"+decl12s+"|^exercit"+decl12s+"|^trist"+decl12s+"|^iuuent"+decl12s+"|^ips"+decl12s+"|^tot"+decl12s+"|^tant"+decl12s+"|^ciuit"+decl12s+"|^equit"+decl12s+"|^ciuitat"+decl12s+"|^oss"+decl12s+"|^brut"+decl12s+"|^class"+decl12s+"|^lit"+decl12s+"|^aetat"+decl12s+"|^maiest"+decl12s+"|^uirtut"+decl12s+"|^virtus|^aegypt"+decl12s+"|^potest"+decl12s+"|^moniment"+decl12s+"|^muniment"+decl12s+"|^fundament"+decl12s+"|^utilit"+decl12s+"|^aliment"+decl12s+"|^instrument"+decl12s+"|^ornament"+decl12s+"|^argument"+decl12s+"|^element"+decl12s+"|^potestat"+decl12s+"|^trigint"+decl12s+"|^quadragint"+decl12s+"|^sexagint"+decl12s+"|^quinquagint"+decl12s+"|^vigint"+decl12s+"|scripsi|isti|asti|isse|ntis|nti|nto|ntum|bitis|batis|ueratis|ueritis|os"+decl12s+"|ens"+decl3+"|[ts]ess"+decl12s+"|eatis|betis|iass"+decl12s+"|fertis|issetis)$")
notadv_rx = re.compile(r"(^sim|sitim|ausim|possim)$")
notagent_rx = re.compile(r"((.*?n(t|s))or"+decl3+"?|ipsorum|^testor|^pector|^litor|^hortor|^tor"+decl3+"|^praetor"+decl3+"?|^utor"+decl3+"?|^hector"+decl3+"?|^castor"+decl3+"?|^nitor"+decl3+"?|.*?[st]orum)$")
notevent1_rx = re.compile(r"(.*?)(^spatio|^tertio|^negotio|^cassio|^ostio|^vitio|^dionysio|^martio|^pretio|^otio|^sentio|^silentio|^contio|^contion"+decl3+")$")
notevent2_rx = re.compile(r"(" + pptc_rx.pattern + "|.*?(^exercit"+decl4+"|^capit"+decl4+"|^equitat"+decl4+"|^senat"+decl4+"|^spirit"+decl4+"|^equit"+decl4+"|^port"+decl4+"|^virtut"+decl4+"|^oss"+decl4+"|^cohort"+decl4+"|^circuit"+decl4+"|^art"+decl4+"|^host"+decl4+"|^milit"+decl4+"|^[st]"+decl4+"|^uult"+decl4+"|ntibus|nsibus|tatibus)$)")
notfptc_rx = re.compile(r"(.*?)(^futur"+decl12+"|^natur"+decl12+"|^matur"+decl12+"|^pictur"+decl12+"|^cultur"+decl12+"|^structur"+decl12+"|^mensur"+decl12+"|^tur"+decl12+"|^mixtur"+decl12+"|^coniectur"+decl12+")$")
notfptcr_rx = re.compile(r"(.*?)(^tur"+decl12+")$")

print(pptc_rx.pattern)
print(adv_rx.pattern)
print(agent_rx.pattern)
print(event1_rx.pattern)
print(event2_rx.pattern)
print(fptc_rx.pattern)
#print(result_rx.pattern)


def filterforms(regex, forms, excluderegex=none_rx):
    itemsbystem = {}
    for form, count in forms.items():
        match = regex.match(form)
        exclude = excluderegex.match(form)
#        if exclude and excluderegex == not_rx:
#            print(exclude.group(0), exclude.group(1))
        if match and not exclude:
            stem = match.group(1)
            if stem not in itemsbystem:
                itemsbystem[stem] = {}
                itemsbystem[stem][form] = count
    return itemsbystem


def find_ambigs(formsbystems):
    seenforms = set()
    duplicateforms = set()
    for formsbystem in formsbystems:
        for stem, formcounts in formsbystem.items():
            for form in formcounts:
                if form not in seenforms:
                    seenforms.add(form)
                else:
                    duplicateforms.add(form)
    return duplicateforms


def subtract_ambigs(rawsbystem, ambigs):
    unambigsbystem = {}
    for stem, formcounts in rawsbystem.items():
        unambigsbystem[stem] = {}
        for form, count in formcounts.items():
            if form not in ambigs:
                unambigsbystem[stem][form] = count
    return {stem:formcounts for stem, formcounts in unambigsbystem.items() if formcounts}


def get_tokensbystem(formsbystem):
    return {stem:sum(formcounts.values()) for stem, formcounts in formsbystem.items()}
    

def valuesort(keysbyvalue, reverse=True):
    return sorted(keysbyvalue.items(), key=lambda kv : kv[1], reverse=reverse)


def get_abovethresh(keyssorted, thresh):
    return [(key, count) for key, count in keyssorted if count >= thresh]


def get_uniq(keyssorted, subtractkeyssorted):
    subtractkeys = set([key for key, count in subtractkeyssorted])
    return [(key, count) for key, count in keyssorted if key not in subtractkeys]

def filterall(countsbyform):
    pptcbystem = filterforms(pptc_rx, countsbyform, notpptc_rx)
    advbystem = filterforms(adv_rx, countsbyform, notadv_rx)
    agentbystem = filterforms(agent_rx, countsbyform, notagent_rx)
    event1bystem = filterforms(event1_rx, countsbyform, notevent1_rx)
    event2bystem = filterforms(event2_rx, countsbyform,notevent2_rx)
    fptcbystem = filterforms(fptc_rx, countsbyform,notfptcr_rx)
#    resultbystem = filterforms(result_rx, countsbyform)

    print("Raw Counts")
    print("pptc:\t", len(pptcbystem))
    print("adv:\t", len(advbystem))
    print("agent:\t", len(agentbystem))
    print("event1:\t", len(event1bystem))
    print("event2:\t", len(event2bystem))
    print("fptc+r:\t", len(fptcbystem))
#    print(len(resultbystem))

    ambiguities = find_ambigs((pptcbystem, advbystem, agentbystem, event1bystem, event2bystem, fptcbystem))#, resultbystem))
    pptcbystem_unambig = subtract_ambigs(pptcbystem, ambiguities)
    advbystem_unambig = subtract_ambigs(advbystem, ambiguities)
    agentbystem_unambig = subtract_ambigs(agentbystem, ambiguities)
    event1bystem_unambig = subtract_ambigs(event1bystem, ambiguities)
    event2bystem_unambig = subtract_ambigs(event2bystem, ambiguities)
    fptcbystem_unambig = subtract_ambigs(fptcbystem, ambiguities)
#    resultbystem_unambig = subtract_ambigs(resultbystem, ambiguities)

    print("\nUnambiguous Counts, subtracting", len(ambiguities))
    print("pptc:\t", len(pptcbystem_unambig))
    print("adv:\t", len(advbystem_unambig))
    print("agent:\t", len(agentbystem_unambig))
    print("event1:\t", len(event1bystem_unambig))
    print("event2:\t", len(event2bystem_unambig))
    print("fptc+r:\t", len(fptcbystem_unambig))
#    print(len(resultbystem_unambig))

    pptcbystem_stemcounts = valuesort(get_tokensbystem(pptcbystem))
    advbystem_stemcounts = valuesort(get_tokensbystem(advbystem))
    agentbystem_stemcounts = valuesort(get_tokensbystem(agentbystem))
    event1bystem_stemcounts = valuesort(get_tokensbystem(event1bystem))
    event2bystem_stemcounts = valuesort(get_tokensbystem(event2bystem))
    fptcbystem_stemcounts = valuesort(get_tokensbystem(fptcbystem))
#    resultbystem_stemcounts = valuesort(get_tokensbystem(resultbystem))

    rankthresh = 500
    freqthresh = pptcbystem_stemcounts[rankthresh][1]
    pptcabove = get_abovethresh(pptcbystem_stemcounts, freqthresh)
    advabove = get_abovethresh(advbystem_stemcounts, freqthresh)
    agentabove = get_abovethresh(agentbystem_stemcounts, freqthresh)
    event1above = get_abovethresh(event1bystem_stemcounts, freqthresh)
    event2above = get_abovethresh(event2bystem_stemcounts, freqthresh)
    fptcabove = get_abovethresh(fptcbystem_stemcounts, freqthresh)
    print("\nTypes with token counts >=", freqthresh)
    print("pptc:\t", len(pptcabove), pptcabove)
    print("adv:\t", len(advabove), advabove)
    print("agent:\t", len(agentabove), agentabove)
    print("event1:\t", len(event1above), event1above)
    print("event2:\t", len(event2above), event2above)
    print("fptc+r:\t", len(fptcabove), fptcabove)
#    print(resultbystem_stemcounts)[0:30]

    advabove_uniq = get_uniq(get_uniq(get_uniq(get_uniq(get_uniq(advabove, pptcabove), agentabove), event1above), event2above), fptcabove)
    agentabove_uniq = get_uniq(get_uniq(get_uniq(get_uniq(get_uniq(agentabove, advabove), pptcabove), event1above), event2above), fptcabove)
    event1above_uniq = get_uniq(get_uniq(get_uniq(get_uniq(get_uniq(event1above, advabove), agentabove), pptcabove), event2above), fptcabove)
    event2above_uniq = get_uniq(get_uniq(get_uniq(get_uniq(get_uniq(event2above, advabove), agentabove), event1above), pptcabove), fptcabove)
    fptcabove_uniq = get_uniq(get_uniq(get_uniq(get_uniq(get_uniq(fptcabove, advabove), agentabove), event1above), event2above), pptcabove)
    pptcabove_uniq = get_uniq(get_uniq(get_uniq(get_uniq(get_uniq(pptcabove, advabove), agentabove), event1above), event2above), fptcabove)
    print("\nUnique stems not attested in other tdevs")
    print("pptc:\t", len(pptcabove_uniq))
    print("adv:\t", len(advabove_uniq))
    print("agent:\t", len(agentabove_uniq))
    print("event1:\t", len(event1above_uniq))
    print("event2:\t", len(event2above_uniq))
    print("fptc+r:\t", len(fptcabove_uniq))


def main():
    countsbyform = {}
    for subdir, dirs, fnames in walk(STATSBASE):
        for fname in fnames:
            if "_fc" in fname:
                fullname = join(subdir, basename(fname))
                print(fullname)
                with open(fullname, "r") as fin:
                    for line in fin:
                        count = int(line.split("\t")[0])
                        form = line.split("\t")[1].strip()
                        if form not in countsbyform:
                            countsbyform[form] = 0
                        countsbyform[form] += count
    sortedcounts = sorted(countsbyform.items(), key=lambda kv : kv[1], reverse=True)

    filterall(countsbyform)


if __name__ == "__main__":
    main()
