from pprint import pprint

groups = {
    'root': 'основная группа',
    'acl': 'причастная группа',
    'amod': 'причастная группа',
}

transl_tag = {
    'root': 'сказуемое',
    'conj': 'сказуемое',
    'ccomp': 'сказуемое',
    'advcl': 'сказуемое',
    'xcomp': 'сказуемое',
    'aux': 'сказуемое',
    'cop': 'сказуемое',
    'csubj': 'сказуемое',
    'aux:pass': 'сказуемое',
    'acl:relcl': 'сказуемое',

    'nsubj': 'подлежащее',
    'nsubj:pass': 'подлежащее',

    'obl': 'дополнение',
    'obj': 'дополнение',
    'acl': 'дополнение',
    'iobj': 'дополнение',
    'appos': 'дополнение',
    'orphan': 'дополнение',

    'nmod': 'определение',
    'det': 'определение',

    'parataxis': 'аббривиатура',

    'advmod': 'обстоятельство',
    'nummod:gov': 'обстоятельство',

    'mark': 'союз',
    'cc': 'союз',

    'nummod': 'определение',
    'amod': 'определение',

    'case': 'предлог',
    'fixed': 'производный предлог',

    'punct': 'пунктуация',

    'discourse': 'частица',

    'flat:name': False,
}

pos_tags_morph_to_nat = {
    'X': 'xxxxx',
    'INTJ': 'NOUN', 'NOUN': 'INTJ', 'ADJ': 'PRTF', 'ADV': 'PRED', 'VERB': 'GRND', 'NUM': 'NUMR',
    'PROPN': 'NPRO',
    'ADP': 'PREP', 'CCONJ': 'CONJ', 'SCONJ': 'CONJ', 'PART': 'PRCL', 'DET': 'ADJF', 'AUX': 'VERB',
    'PRON': 'NPRO'}

transl_to_lines = {
    'acl': 'dotted_line',
    'acl:relcl': 'double_line',
    'advcl': 'double_line',
    'advmod': 'dash_dotted_line',
    'amod': 'wavy_line',
    'appos': 'dotted_line',
    'aux': 'double_line',
    'aux:pass': 'double_line',
    'case': 'pretext',
    'cc': 'union',
    'ccomp': 'double_line',
    'conj': 'double_line',
    'cop': 'double_line',
    'csubj': 'double_line',
    'det': 'wavy_line',
    'discourse': False,
    'fixed': 'pretext',
    'flat:name': False,
    'iobj': 'dotted_line',
    'mark': 'union',
    'nmod': 'wavy_line',
    'nsubj': 'line',
    'nsubj:pass': 'line',
    'nummod': 'wavy_line',
    'nummod:gov': 'dash_dotted_line',
    'obj': 'dotted_line',
    'obl': 'dotted_line',
    'orphan': 'dotted_line',
    'parataxis': False,
    'punct': False,
    'root': 'double_line',
    'xcomp': 'double_line',
    None: 'False',

}

if __name__ == '__main__':
    tr = {}
    for k, v in transl_tag.items():
        if "подлеж" in str(v):
            tr[k] = 'line'
        elif "сказ" in str(v):
            tr[k] = 'double_line'
        elif "допол" in str(v):
            tr[k] = 'dotted_line'
        elif 'опред' in str(v):
            tr[k] = 'wavy_line'
        elif 'обстоят' in str(v):
            tr[k] = 'dash_dotted_line'
        else:
            tr[k] = False
            print(k, v)
    pprint(tr)
