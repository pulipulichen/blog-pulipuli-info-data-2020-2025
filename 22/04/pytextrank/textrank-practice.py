# Configuration
output_phrases_count = 10
output_sentences_count = 3

# -----------

!python3 -m pip install pytextrank
!python3 -m spacy download en_core_web_sm

import spacy
import pytextrank

# load a spaCy model, depending on language, scale, etc.
nlp = spacy.load("en_core_web_sm")

# add PyTextRank to the spaCy pipeline
nlp.add_pipe("textrank")

# -----------

# example text
with open('input.txt', 'r') as file:
    text = file.read().replace('\n', '')
doc = nlp(text)

# examine the top-ranked phrases in the document
path = 'output-phrases.txt'
f = open(path, 'w')

for phrase in doc._.phrases:
    print("=== RANK: ", phrase.rank, " ====")
    print("TEXT:\t", phrase.text)
    print("COUNT:\t", phrase.count)
    print("CHUNKS:\t", phrase.chunks)


# -----------------
# Construct a list of the sentence boundaries with a phrase vector (initialized to empty set) for each...

sent_bounds = [ [s.start, s.end, set([])] for s in doc.sents ]

# -----------------
# Iterate through the top-ranked phrases, added them to the phrase vector for each sentence...

# for use in tutorial and development; do not include this `sys.path` change in production:
import sys ; sys.path.insert(0, "../")
!python3 -m pip install icecream
from icecream import ic

phrase_id = 0
unit_vector = []

for p in doc._.phrases:
    ic(phrase_id, p.text, p.rank)

    unit_vector.append(p.rank)

    for chunk in p.chunks:
        ic(chunk.start, chunk.end)

        for sent_start, sent_end, sent_vector in sent_bounds:
            if chunk.start >= sent_start and chunk.end <= sent_end:
                ic(sent_start, chunk.start, chunk.end, sent_end)
                sent_vector.add(phrase_id)
                break

    phrase_id += 1

    f.write(p.text)
    if phrase_id == output_phrases_count:
        break

    f.write("\n")

f.close()

# -----------------
# Then normalized...

sum_ranks = sum(unit_vector)

unit_vector = [ rank/sum_ranks for rank in unit_vector ]
unit_vector

# -----------------
# Iterate through each sentence, calculating its euclidean distance from the unit vector...

from math import sqrt

sent_rank = {}
sent_id = 0

for sent_start, sent_end, sent_vector in sent_bounds:
    ic(sent_vector)
    sum_sq = 0.0
    ic
    for phrase_id in range(len(unit_vector)):
        ic(phrase_id, unit_vector[phrase_id])

        if phrase_id not in sent_vector:
            sum_sq += unit_vector[phrase_id]**2.0

    sent_rank[sent_id] = sqrt(sum_sq)
    sent_id += 1

# -----------------
# Sort the sentence indexes in descending order

from operator import itemgetter

sorted(sent_rank.items(), key=itemgetter(1))

# -----------------
# Extract the sentences with the lowest distance, up to the limit requested...

sent_text = {}
sent_id = 0

for sent in doc.sents:
    sent_text[sent_id] = sent.text
    sent_id += 1

num_sent = 0

path = 'output-sentences.txt'
f = open(path, 'w')

for sent_id, rank in sorted(sent_rank.items(), key=itemgetter(1)):
    ic(sent_id, sent_text[sent_id])
    f.write(sent_text[sent_id])
    num_sent += 1

    if num_sent == output_sentences_count:
        break
    f.write("\n")

f.close()
