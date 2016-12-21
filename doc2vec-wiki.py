import gensim
import os
import smart_open

data_dir = '/home/satoshi/dev/wikipedia/titles'

def read_corpus(fname, tokens_only=False):
    with smart_open.smart_open(fname, encoding="utf-8") as f:
        all_lines = ""
        for i, line in enumerate(f):
            all_lines
            if tokens_only:
                yield gensim.utils.simple_preprocess(line)
            else:
                # For training data, add tags
                yield gensim.models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(line), [i])

train_corpus = []
for filename in [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]:
    title = ""
    with open(os.path.join(data_dir, filename)) as f:
        title = filename.replace(".txt", "")
        content = ""
        for l in f:
            content += l
        tagged_doc = gensim.models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(content), [title])
        train_corpus.append(tagged_doc)

model = gensim.models.doc2vec.Doc2Vec(size=100, min_count=2, iter=10, workers=6)
model.build_vocab(train_corpus)
model.train(train_corpus)
model.save("doc2vec.model")

inferred_vector = model.infer_vector(['only', 'you', 'can', 'prevent', 'forrest', 'fires'])
print inferred_vector


ranks = []
for doc_id in range(len(train_corpus)):
    inferred_vector = model.infer_vector(train_corpus[doc_id].words)
    sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))
    rank = [docid for docid, sim in sims].index(doc_id)
    ranks.append(rank)


