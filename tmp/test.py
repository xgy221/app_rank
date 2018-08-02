import jieba
import gensim
from gensim import corpora, models

stop_words = []

with open("../data/stop_words.txt", "r") as f:
    for word in f:
        stop_words.append(word.strip())

s = '今天我和男票一块去了西溪湿地游玩，我们坐着船进入景区，观赏了很多美丽的荷花'
s1 = '今天我学习了LDA，一种主题模型算法。'
ss = jieba.cut(s)
ss1 = jieba.cut(s1)
out = []
out_words = []
for word in ss:
    if word not in stop_words:
        if word != '\t':
            out_words.append(word)
out.append(out_words)
out_words = []
for word in ss1:
    if word not in stop_words:
        if word != '\t':
            out_words.append(word)
out.append(out_words)
print(out)
dictionary = corpora.Dictionary(out)


corpus = [dictionary.doc2bow(text) for text in out]
print(corpus[0])
print(corpus[1])

ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=2, id2word = dictionary, passes=20)
print(ldamodel.print_topics(num_topics=2, num_words=4))