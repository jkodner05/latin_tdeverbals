import re, sys


def vuji(word):
    return word.replace("v","u").replace("j","i")

def nolen(word):
    return word.replace("ā", "a").replace("ē", "e").replace("ī", "i").replace("ō", "o").replace("ū", "u")

def read_freqlist(freqfname, freqcutoff=0, top_n=0):
    remove_nums = re.compile(r"\d+")
    freq_words = {}
    i = 0
    with open(freqfname, "r") as f:
        for line in f:
            if top_n and i >= top_n:
                break
            components = vuji(line).split("\t")
            freq = int(components[0].strip())
            word = remove_nums.sub("",vuji(components[1])).replace("-","").replace("_","").strip()
            if freq >= freqcutoff and len(word) >= 2 and ((word[-1] == "o") or (word[-1] == "r" and word[-2] == "o")): #~verbs 
                old_word = word
#                word = strip_form(word)
                freq_words[word] = freq
                i += 1
#    print("GOT THE TOP " + str(i) + " VERBS")
    return freq_words


def is_freq(candidate, freq_words):
    candidate = nolen(candidate)
    if candidate in freq_words:
        return freq_words[candidate]
    return 0
