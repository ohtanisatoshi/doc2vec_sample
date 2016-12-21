# -*- coding: utf-8 -*-
import gensim
import os
import collections
import MeCab

data_dir = '/var/data/wiki_files'
min_word_count = 10
model_save_file = 'doc2vec.model'

def read_corpus(max_data_count=10000):
    train_corpus = []
    corpus_cnt = 0
    for filename in [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]:
        if corpus_cnt >= max_data_count:
            break

        with open(os.path.join(data_dir, filename)) as f:
            title = filename.replace(".txt", "")
            content = ""
            for l in f:
                content += l
            tagged_doc = gensim.models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(content), [title])
            if len(tagged_doc.words) < min_word_count:
                continue
            train_corpus.append(tagged_doc)
            corpus_cnt += 1

    return train_corpus

def train_model(train_corpus):
    model = gensim.models.doc2vec.Doc2Vec(size=100, min_count=2, iter=10, workers=10)
    model.build_vocab(train_corpus)
    model.train(train_corpus)
    model.save(model_save_file)

    return model

def load_model():
    model = gensim.models.doc2vec.Doc2Vec.load(model_save_file)
    return model

def test_model(model, train_corpus):
    ranks = []
    for i, corpus in enumerate(train_corpus):
        title = corpus.tags[0]
        inferred_vector = model.infer_vector(corpus.words)
        sims = model.docvecs.most_similar([inferred_vector], topn=3)
        if title == sims[0][0]:
            ranks.append(0)
        else:
            print("{} {}".format(i, title))
            for j, t in enumerate(sims):
                print("  {}: {}, {:.2f}".format(j+1, t[0], t[1]))
            ranks.append(1)

    ranks_counter = collections.Counter(ranks)
    accuracy = float(ranks_counter[0]) / float(len(train_corpus))
    print("accuracy: {:.2f} {:d} / {:d}".format(accuracy, ranks_counter[0], len(train_corpus)))

if os.path.exists(model_save_file):
    mt = MeCab.Tagger("-Owakati -d /usr/lib/mecab/dic/mecab-ipadic-neologd")
    model = load_model()
    filename = "シドニー" + ".txt"
    test_doc = []
    with open(os.path.join(data_dir, filename)) as f:
        content = ""
        for l in f:
            content += l
        sliced_content = content[int(len(content)*0.3):int(len(content)*0.5)]
        sliced_content = "2015年にはメジャーリーグサッカーで注目を集める選手にまで成長。レッドブルズではレギュラーに定着し、北米リーグでのクラブ最高成績に貢献。レッドブルズではCONCACAFチャンピオンズリーグも経験した。所属していたニューヨーク・レッドブルズとの契約を1年残していたが、2016年から地元のクラブを離れる決断を下した。"
        print sliced_content
        test_doc = gensim.utils.simple_preprocess(mt.parse(sliced_content))
    inferred_vector = model.infer_vector(test_doc)
    sims = model.docvecs.most_similar([inferred_vector], topn=10)
    for j, t in enumerate(sims):
        print("  {}: {}, {:.2f}".format(j+1, t[0], t[1]))
else:
    print("reading corpus...")
    train_corpus = read_corpus(9999999999)

    print("training corpus...")
    model = train_model(train_corpus)

    print("testing corpus...")
    test_model(model, train_corpus)
