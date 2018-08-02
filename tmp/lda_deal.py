import csv
import warnings

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
from gensim import corpora

with open("../pre_processed_data/free/free75.csv", 'r', newline="", encoding='utf-8-sig') as f:
    all_list = list(csv.reader((line.replace('\0', '') for line in f)))

dictionary = corpora.Dictionary(all_list)
corpus = [dictionary.doc2bow(text) for text in all_list]
lda_model = gensim.models.ldamodel.LdaModel(corpus, num_topics=6, id2word=dictionary, passes=20)
print(lda_model.print_topics(num_topics=6, num_words=4))
