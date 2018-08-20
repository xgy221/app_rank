import csv
import warnings

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim import corpora, models, similarities

sum_sim = 0

with open("../paper_needed/jieba_deal1739536.csv", 'r', newline="", encoding='utf-8-sig') as f:
    all_list = list(csv.reader((line.replace('\0', '') for line in f)))

dictionary = corpora.Dictionary(all_list)
corpus = [dictionary.doc2bow(text) for text in all_list]
tf_idf = models.TfidfModel(corpus)
corpus_tf_idf = tf_idf[corpus]

for data in all_list:
    vec_bow = dictionary.doc2bow(data)
    vec_tfidf = tf_idf[vec_bow]
    index = similarities.MatrixSimilarity(corpus_tf_idf)
    sims = index[vec_tfidf]
    similarity = list(sims)
    sum_sim = sum_sim + sum(similarity)

sim = (sum_sim-30)/2
print(sim)
ave_sim = sim*2/(30*29)
print(ave_sim)
