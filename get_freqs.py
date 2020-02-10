import re, unicodedata, time
import multiprocessing as mp
from os import listdir, walk, makedirs
from os.path import isfile, join, exists, basename, expanduser

import cltk
from cltk.corpus.utils.importer import CorpusImporter
from cltk.tokenize.word import WordTokenizer
from cltk.stem.lemma import LemmaReplacer
from cltk.stem.latin.j_v import JVReplacer
import cltk.lemmatize.latin.backoff as lemmatizers
from cltk.utils.file_operations import open_pickle

STATSBASE = "stats"
BACKOFFPATH = "~/cltk_data/latin/model/latin_models_cltk/lemmata/backoff"
DATABASE = "../data/Perseus_OL-CL/rawtext"

def create_lemmatizer():
    path = expanduser(BACKOFFPATH)

    def getmodel(fname):
        return open_pickle(join(path, fname))

    fname1 = 'latin_misc_patterns.pickle'
    fname3 = 'latin_model.pickle'
    fname4 = 'latin_lemmata_cltk.pickle'
    fname5 = 'latin_names.pickle'
    fname6 = 'latin_pos_lemmatized_sents.pickle'
    model1 = getmodel(fname1)
    model1 = [(elem[0].replace("(\\w*)","")+"$",elem[1]) for elem in model1]
#    model2 = getmodel(fname2)
    model3 = getmodel(fname3)
    model4 = getmodel(fname4)
    model5 = getmodel(fname5)
    model6 = getmodel(fname6)

    lemmatizer0 = lemmatizers.DefaultLemmatizer('UNK')
    lemmatizer1 = lemmatizers.RegexpLemmatizer(model1,  backoff=lemmatizer0)
    lemmatizer2 = lemmatizers.PPLemmatizer(lemmatizers.latin_verb_patterns, lemmatizers.latin_pps, backoff=lemmatizer1)
    lemmatizer3 = lemmatizers.TrainLemmatizer(model3, backoff=lemmatizer2)
    lemmatizer4 = lemmatizers.TrainLemmatizer(model4, backoff=lemmatizer3)
    lemmatizer5 = lemmatizers.TrainLemmatizer(model5, backoff=lemmatizer4)
    lemmatizer6 = lemmatizers.BigramPOSLemmatizer(model6, backoff=lemmatizer5)
#    lemmatizer7 = lemmatizers.NgramPOSLemmatizer(3, model6, backoff=lemmatizer6)
    return lemmatizer6


def remove_accents(accentedtext):
    normalizedtext = unicodedata.normalize('NFD', accentedtext)
    return normalizedtext.encode('ASCII', 'ignore').decode("utf-8")


def lemmatize(fname, tokenizer, lemmatizer):
    jv = JVReplacer()

    lemmacounts = {}
    formcounts = {}
    lemmaforms = {}
    with open(fname, "r") as f:
        i = 0
        hangingword = ""

#        t = time.time()
        for line in f:

            line = hangingword.replace("-","") + line.strip()
            if line and line[-1] == "-":
                splitline = line.split(" ")
                hangingword = " ".join(splitline[-1])
                line = " ".join(splitline[0:-1])
            else:
                hangingword = ""
                
            noaccents = remove_accents(line).replace("'","").replace("/","").replace("-","").replace("!","").replace("?","").replace(".","")
            lemmatized = lemmatizer.lemmatize(tokenizer.tokenize(jv.replace(noaccents.lower())))
            for form, lemma in lemmatized:
                if lemma.lower() == "punc" or lemma.lower() == "period":
                    continue
                if form not in formcounts:
                    formcounts[form] = 0
                formcounts[form] += 1
                if lemma not in lemmacounts:
                    lemmacounts[lemma] = 0
                    lemmaforms[lemma] = set([])
                lemmacounts[lemma] += 1
                lemmaforms[lemma].add(form)
            i += 1
            if not i % 100:
                
                print(basename(fname), i)
#                print(basename(fname), i, time.time() - t)
#                t = time.time()

    return formcounts, lemmacounts, lemmaforms
#    print(lemmaforms)
#    print(lemmaforms["UNK"])
#    print(sorted(formcounts.items(), key=lambda kv : kv[1], reverse=True))
#    print(sorted(lemmacounts.items(), key=lambda kv : kv[1], reverse=True))



def write_data(fnamebase, formcounts, lemmacounts, lemmaforms):

    def write_freqs(fnamebase, suffix, counts):
        sortedcounts = sorted(counts.items(), key=lambda kv : kv[1], reverse=True)
        with open(join(STATSBASE,fnamebase.replace(".txt", suffix)), "w") as f:
            for word, count in sortedcounts:
                f.write(str(count))
                f.write("\t" + word + "\n")

    with open(join(STATSBASE,fnamebase.replace(".txt", "_lf.txt")), "w") as f:
        sortedlemmaforms = sorted(lemmaforms.items(), key=lambda kv : kv[0])
        for lemma, forms in sortedlemmaforms:
            f.write(lemma + "\t")
            f.write(",".join(sorted(list(forms))) + "\n")

    write_freqs(fnamebase, "_lc.txt", lemmacounts)
    write_freqs(fnamebase, "_fc.txt", formcounts)


tokenizer = WordTokenizer('latin')
lemmatizer = create_lemmatizer()

def process(fnamebase):
    print("STARTING:\t", fnamebase)
    processstarttime = time.time()
    formcounts, lemmacounts, lemmaforms = lemmatize(fnamebase, tokenizer, lemmatizer)
    write_data(basename(fnamebase), formcounts, lemmacounts, lemmaforms)
    print("FINISHED ", fnamebase, "\tTIME:\t", time.time() - processstarttime)

def main():
    if not exists(STATSBASE):
        makedirs(STATSBASE)

    corpus_importer = CorpusImporter('latin')
    corpus_importer.import_corpus(corpus_name='latin_models_cltk')

    startime = time.time()
    sizes = {}
    for subdir, dirs, fnames in walk(DATABASE):
        for fname in fnames:
            fullname = join(subdir, basename(fname))
            with open(fullname, "r") as f:
                size = sum([len(line.strip()) for line in f])
                sizes[fullname] = size
                
    sortedfnames = sorted(sizes.items(), key=lambda kv : kv[1], reverse=True)
    print(sortedfnames)
    print([fname for fname, charlen in sortedfnames])
    p = mp.Pool(processes=5)
    p.map(process, [fname for fname, charlen in sortedfnames])
    print("TOTAL TIME:\t", time.time() - starttime)

#        for fname in fnames:
#            print(join(subdir,fname))
#            formcounts, lemmacounts, lemmaforms = lemmatize(join(subdir,fname), tokenizer, lemmatizer)
#            write_data(fname, formcounts, lemmacounts, lemmaforms)



if __name__ == "__main__":
    main()
