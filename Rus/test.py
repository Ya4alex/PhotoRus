# -*- coding: utf-8 -*-
from natasha import Segmenter
import nltk
import time

start_time = time.time()

segmenter = Segmenter()
'''morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)
names_extractor = NamesExtractor(morph_vocab)'''

text = 'Мистер и миссис Дурсль проживали в доме номер четыре по Тисовой улице и всегда с гордостью заявляли, что они, ' \
       'слава богу, абсолютно нормальные люди. Уж от кого-кого, а от них никак нельзя было ожидать, чтобы они попали ' \
       'в какую-нибудь странную или загадочную ситуацию. Мистер и миссис Дурсль весьма неодобрительно относились к ' \
       'любым странностям, загадкам и прочей ерунде.'
text = text.replace('...', '.')
'''doc = Doc(text)
doc.segment(segmenter)'''
sent = segmenter.sentenize(text)

print("--- %s seconds ---" % (time.time() - start_time))

for i in sent:
    print('\n'.join(nltk.sent_tokenize(i.text, language="russian")))
