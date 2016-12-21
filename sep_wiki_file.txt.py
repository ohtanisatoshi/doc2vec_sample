# -*- coding: utf-8 -*-
import os
import MeCab

filename = '/home/satoshi/dev/wikipedia/all.txt'
outdir = "/home/satoshi/dev/wikipedia/titles"

mt = MeCab.Tagger("-Owakati -d /usr/lib/mecab/dic/mecab-ipadic-neologd")
openfile = filename
with open(openfile, "r") as f:
    title = ""
    content = ""
    wf = None
    for line in f:
        try:
            if line.startswith("*"):
                continue
            if line.startswith("=="):
                continue
            if line.startswith("[[File:"):
                continue
            if line.startswith("[[ファイル:"):
                continue
            if line.startswith("[[:"):
                continue
            if line.startswith("[[Image:"):
                continue
            line = line.replace("\n", "")
            if len(line) == 0:
                continue

            if line.startswith("[[") and line.endswith("]]"):
                if len(content) > 0:
                    openfile = os.path.join(outdir, title + ".txt")
                    with open(openfile, "w") as wf:
                        wf.write(mt.parse(content))

                title = line.replace("[[", "").replace("]]", "").replace("/", "_")
                content = ""
                continue

            content += line.replace("[[", "").replace("]]", "")
        except IOError:
            print("cannot open file {}".format(openfile))

    if len(content) > 0:
        openfile = os.path.join(outdir, title + ".txt")
        with open(openfile, "w") as wf:
            wf.write(mt.parse(content))
