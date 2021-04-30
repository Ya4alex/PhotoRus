from pprint import pprint
from dictionaries import pos_tags_morph_to_nat, transl_tag, groups

import logging
import pymorphy2
from natasha import (
    Segmenter,
    NewsEmbedding,
    NewsSyntaxParser,
    NewsMorphTagger,
    Doc
)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

morph = pymorphy2.MorphAnalyzer()
segmenter = Segmenter()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)


def func_grammarchecker(string):
    result = []
    doc = Doc(string)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    for num in doc.sents[0].morph:
        for j in range(len(num)):
            count = 0
            local_word = ''
            for k in num[j]:
                if count == 0:
                    local_word = k
                    result.append({
                        'word': local_word,
                        'feathers': {
                            'natasha_tag': None,
                            'obj': None,
                            'photorus_tag': None,
                            'set': {'Case': None},
                            'feats': {},
                        },
                        'relations': {
                            'id': None,
                            'head_id': None,
                            'm_head_id': None,
                            'group': {'tag': None, 'human_tag': None}
                        }
                    })
                if count == 1:
                    suggest = []
                    for p in morph.parse(local_word):
                        if p.tag.POS not in suggest:
                            suggest.append(p.tag.POS)
                            if None in suggest:
                                result[-1]['feathers']['obj'] = str(p.tag) # часть речи
                                count += 1
                                continue
                    try:
                        if k in suggest and len(suggest) == 1:
                            result[-1]['feathers']['obj'] = k
                        else:
                            if len(suggest) == 1:
                                result[-1]['feathers']['obj'] = suggest[0]
                            else:
                                result[-1]['feathers']['obj'] = pos_tags_morph_to_nat[k]
                    except ValueError:
                        if len(suggest) == 1:
                            result[-1]['feathers']['obj'] = suggest[0]
                        else:
                            if k == "X":
                                print('\nX---------------------------')
                                pprint(result)
                                print(string)
                                print(num)
                                [i ** 0.5 for i in range(1000)]
                            result[-1]['feathers']['obj'] = pos_tags_morph_to_nat[k]
                if count == 2:
                    if 'Case' in k and result[-1]['feathers']['obj'] == 'VERB':
                        result[-1]['feathers']['set']['Mood'] = 'povel'
                    else:
                        for key, val in k.items():
                            if key == 'Mood':
                                result[-1]['feathers']['set'][str(key)] = str(val)
                                result[-1]['feathers']['set']['Case'] = None
                            elif key == 'Case' and val is not None:
                                result[-1]['feathers']['set']['Mood'] = None
                                result[-1]['feathers']['set'][str(key)] = str(val)
                count += 1

    doc.parse_syntax(NewsSyntaxParser(emb))

    for num in range(len(doc.tokens)):
        try:
            local_obj = result[num]['feathers']['obj']
        except IndexError:
            print('\n\n--------------------------------')
            print(num, len(doc.tokens))
            pprint(doc.tokens)
            print()
            pprint(result)
            print()
            pprint(doc.sents[0].morph)
            print(string)
            break
        # print(doc.tokens[num])
        result[num]['relations']['head_id'] = int(doc.tokens[num].head_id.split('_')[1]) - 1
        result[num]['relations']['id'] = int(doc.tokens[num].id.split('_')[1]) - 1
        result[num]['feathers']['feats'] = doc.tokens[num].feats

        rel = doc.tokens[num].rel

        # -------------------
        if transl_tag.get(rel) is None:
            logger.warning(f"no natasha teg {rel}\t{doc.tokens[num]}\t{string}")

            result[num]['feathers']['photorus_tag'] = rel
            continue
        # --------------------

        if local_obj == 'GRND' or local_obj == 'PRTF' or local_obj == 'PRTS' and rel != 'root':
            if local_obj == 'GRND':
                photorus_tag = 'деепричастие'
            else:
                photorus_tag = 'причастие'
        elif (local_obj == 'NOUN' and transl_tag[str(rel)] == 'сказуемое' and  # тут
              result[num]['feathers']['set']['Case'] != 'Loc'):

            photorus_tag = 'подлежащие'
        elif local_obj == 'NPRO' and transl_tag[str(rel)] == 'сказуемое':
            photorus_tag = 'подлежащие'
        elif local_obj == 'ADJF' and transl_tag[str(rel)] == 'сказуемое':
            result[num]['feathers']['obj'] = 'VERB'
            photorus_tag = 'сказуемое'
        else:
            photorus_tag = transl_tag[str(rel)]
            if photorus_tag is None:
                photorus_tag = result[result[num]['relations']['head_id']]['feathers']['photorus_tag']

        result[num]['feathers']['natasha_tag'] = rel  # <---- ruski debug
        result[num]['feathers']['photorus_tag'] = photorus_tag

    for i, word in enumerate(result):
        wordx = word
        count = 0
        while not groups.get(wordx['feathers']['natasha_tag']):
            if wordx['feathers']['photorus_tag'] == 'деепричастие' or wordx['relations']['head_id'] < 0 or count > 20:
                break
            if wordx['feathers']['photorus_tag'] == 'причастие' or wordx['relations']['head_id'] < 0 or count > 20:
                break
            wordx = result[wordx['relations']['head_id']]
            count += 1

        if wordx['feathers']['photorus_tag'] == 'причастие':
            result[i]['relations']['group']['human_tag'] = "причатная группа"
            result[i]['relations']['group']['tag'] = 'partic'
        elif wordx['feathers']['photorus_tag'] == 'деепричастие':
            result[i]['relations']['group']['human_tag'] = "деепричатная группа"
            result[i]['relations']['group']['tag'] = 'gerund'
        elif groups.get(wordx['feathers']['natasha_tag']):
            result[i]['relations']['group']['human_tag'] = groups.get(wordx['feathers']['natasha_tag'])
            result[i]['relations']['group']['tag'] = wordx['feathers']['natasha_tag']
        else:
            result[i]['relations']['group']['human_tag'] = "основная группа"
            result[i]['relations']['group']['tag'] = 'root'
        result[i]['relations']['m_head_id'] = wordx['relations']['id']
    return {
        'content': result,
        'sent': string
    }

if __name__ == '__main__':
    morph_tagger