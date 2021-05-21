from pprint import pprint
from .dictionaries import pos_tags_morph_to_nat, transl_tag, groups

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


def sent_segment(text):
    pass


def syntactic_parser(text):
    result = []
    doc = Doc(text)
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
                if count == 1:  # часть речи
                    suggest = []
                    flag_out = False
                    for p in morph.parse(local_word):
                        if p.tag.POS not in suggest:
                            suggest.append(p.tag.POS)
                            if None in suggest:
                                result[-1]['feathers']['obj'] = str(p.tag)  # часть речи
                                count += 1
                                flag_out = True
                                continue
                    if flag_out:
                        continue
                    try:  # чекнуть
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
                            if k == "X":  # добавить токен Х
                                pass
                            else:
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
            print(text)
            break
        # print(doc.tokens[num])
        rel = doc.tokens[num].rel
        result[num]['relations']['head_id'] = int(doc.tokens[num].head_id.split('_')[1]) - 1
        result[num]['relations']['id'] = int(doc.tokens[num].id.split('_')[1]) - 1
        result[num]['feathers']['feats'] = doc.tokens[num].feats
        result[num]['feathers']['natasha_tag'] = rel

        # -------------------
        if transl_tag.get(rel) is None:
            logger.warning(f"no natasha teg {rel}\t{doc.tokens[num]}\t{text}")

            result[num]['feathers']['photorus_tag'] = rel
            continue
        # --------------------

        if local_obj in ('GRND', 'PRTF', 'PRTS') and rel != 'root':  # сократить
            if local_obj == 'GRND':
                photorus_tag = 'деепричастие'
            else:
                photorus_tag = 'причастие'
        elif (local_obj == 'NOUN' and transl_tag[str(rel)] == 'сказуемое' and  # тут
              result[num]['feathers']['set']['Case'] != 'Loc'):  # чек

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
        'sent': text
    }
