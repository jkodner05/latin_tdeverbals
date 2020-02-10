import re
from os import listdir, walk
from os.path import isfile, join, exists, basename, expanduser

STATSBASE = "stats"

decl1 = "(a|am|ae|ae|a|ae|as|arum|is|is|abus)"
decl2 = "(us|um|i|o|o|i|os|orum|is|is)"
decl3 = "(is|em|is|i|e|es|es|um|ibus|ibus|ium)"
decl4 = "(us|um|us|ui|u|us|us|uum|ibus|ibus|ubus)"
decl12 = "("+decl1+"|"+decl2+")"

none_rx = re.compile(r"^$")
pptc_rx = re.compile(r"(.*?(t|s))"+decl12+"$")
adv_rx = re.compile(r"(.*?(t|s))im$")
agent_rx = re.compile(r"(.*?(t|s))or"+decl3+"?$")
event1_rx = re.compile(r"(.*?(t|s))io(n"+decl3+")?$")
event2_rx = re.compile(r"(.*?(t|s))"+decl4+"$")
fptc_rx = re.compile(r"(.*?(t|s))ur("+decl1+"|"+decl2+")$")
result_rx = re.compile(r"(.*?(t|s))ur"+decl1 + "$")

notpptc_rx = re.compile(r"(.*?)(^[ts]"+decl12+"|^legat"+decl12+"|^poet"+decl12+"|^quart"+decl12+"|^quint"+decl12+"|^sext"+decl12+"|^marit"+decl12+"|^beat"+decl12+"|^auctorit"+decl12+"|^piet"+decl12+"|^mult"+decl12+"|^senat"+decl12+"|^sat"+decl12+"|^est"+decl12+"|^uelut"+decl12+"|^nis"+decl12+"|^quas"+decl12+"|^caus"+decl12+"|^uit"+decl12+"|^ut"+decl12+"|^senect"+decl12+"|^etiams"+decl12+"|^crass"+decl12+"|^uult"+decl12+"|^exercit"+decl12+"|^trist"+decl12+"|^iuuent"+decl12+"|^ips"+decl12+"|^tot"+decl12+"|^tant"+decl12+"|^ciuit"+decl12+"|^equit"+decl12+"|^ciuitat"+decl12+"|^oss"+decl12+"|^class"+decl12+"|^lit"+decl12+"|^aetat"+decl12+"|^uirtut"+decl12+"|^virtus|^aegypt"+decl12+"|^potest"+decl12+"|^trigint"+decl12+"|isti|asti|isse|ntis|nti|nto|ntum|bitis|batis|ueratis|ueritis|os"+decl12+"|ens"+decl3+"|[ts]ess"+decl12+"|eatis|betis|iass"+decl12+"|fertis|issetis)$")
notagent_rx = re.compile(r"((.*?n(t|s))or"+decl3+"?|ipsorum|praetor.*|.*?[st]orum)$")
notevent1_rx = re.compile(r"(.*?)(^spatio|^tertio|^negotio|^vitio|^pretio|^otio|^sentio|^silentio|^contio|^contion"+decl3+")$")
notevent2_rx = re.compile(r"(" + pptc_rx.pattern + "|.*?(^exercit"+decl4+"|^senat"+decl4+"|^spirit"+decl4+"|^equit"+decl4+"|^port"+decl4+"|^virtut"+decl4+"|^oss"+decl4+"|^art"+decl4+"|^host"+decl4+"|^milit"+decl4+"|^[st]"+decl4+"|^uult"+decl4+"|ntibus|nsibus|tatibus)$)")
notfptc_rx = re.compile(r"(.*?)(^futur"+decl12+"|^natur"+decl12+"|^matur"+decl12+"|^pictur"+decl12+"|^cultur"+decl12+"|^structur"+decl12+"|^mensur"+decl12+")$")

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

def filterall(countsbyform):
    pptcbystem = filterforms(pptc_rx, countsbyform, notpptc_rx)
    advbystem = filterforms(adv_rx, countsbyform)
    agentbystem = filterforms(agent_rx, countsbyform, notagent_rx)
    event1bystem = filterforms(event1_rx, countsbyform, notevent1_rx)
    event2bystem = filterforms(event2_rx, countsbyform,notevent2_rx)
    fptcbystem = filterforms(fptc_rx, countsbyform,notfptc_rx)
#    resultbystem = filterforms(result_rx, countsbyform)

    print("Raw Counts")
    print("pptc:\t", len(pptcbystem))
    print("adv:\t", len(advbystem))
    print("agent:\t", len(agentbystem))
    print("event1:\t", len(event1bystem))
    print("event2:\t", len(event2bystem))
    print("fptc:\t", len(fptcbystem))
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
    print("fptc:\t", len(fptcbystem_unambig))
#    print(len(resultbystem_unambig))

    pptcbystem_stemcounts = valuesort(get_tokensbystem(pptcbystem))
    advbystem_stemcounts = valuesort(get_tokensbystem(advbystem))
    agentbystem_stemcounts = valuesort(get_tokensbystem(agentbystem))
    event1bystem_stemcounts = valuesort(get_tokensbystem(event1bystem))
    event2bystem_stemcounts = valuesort(get_tokensbystem(event2bystem))
    fptcbystem_stemcounts = valuesort(get_tokensbystem(fptcbystem))
#    resultbystem_stemcounts = valuesort(get_tokensbystem(resultbystem))

    rankthresh = 100
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
    print("fptc:\t", len(fptcabove), fptcabove)
#    print(resultbystem_stemcounts)[0:30]


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
