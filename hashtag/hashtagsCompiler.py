import csv
import json
import gensim


with open('sets.json', 'r', encoding='utf-8') as outfile:
    training_set = json.load(outfile)

mod = gensim.models.Word2Vec(min_count=3, window=5, sg=1, hs=1, vector_size=300)
mod.build_vocab(training_set, progress_per=1000)
mod.train(training_set, total_examples=mod.corpus_count, epochs=25)

unique = set()
for i in training_set:
    for j in i:
        unique.add(j)

result = {}
for i in unique:
    if i in mod.wv:
        result[i] = float(mod.wv.similarity('votealldemocrat', i) - mod.wv.similarity('voterepublican', i))

result = sorted(result.items(), key=lambda x: x[1])

with open('hashtags.csv', 'w', encoding="utf_8", newline='') as f:
    writer = csv.writer(f)

    for key, val in result:
        writer.writerow([key, val])
