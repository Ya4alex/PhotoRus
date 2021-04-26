import pymorphy2
from pprint import pprint

pos_tags_pymorphy = ['NOUN', 'ADJF', 'ADJS', 'COMP', 'VERB', 'INFN', 'PRTF', 'PRTS', 'GRND',
                     'NUMR', 'ADVB', 'NPRO', 'PRED', 'PREP', 'CONJ', 'CONJ', 'PRCL', 'INTJ',
                     'ADJF', 'VERB']
pos_tags_photorus = ['существительное', 'прилагательное(полное)', 'прилагательное(краткое)', 'компаратив', 'глагол',
                     'глагол(инфинитив)', 'причастие(полное)', 'причастие(краткое)', 'деепричастие',
                     'числительное', 'наречие', 'местоимение-существительное', 'предикатив', 'предлог', 'союз',
                     'частица', 'междометие']
morph_tags_pymorphy = ['indc', 'impr', '1',  # Наклонение
                       'perf', 'impf',  # Вид
                       'tran', 'intr',  # Переходность
                       'sing', 'plur',  # Число
                       'masc', 'femn', 'neut',  # Род
                       '1per', '2per', '3per',  # Лицо
                       'past', 'pres', 'futr',  # Время
                       'nomn', 'gent', 'datv', 'accs', 'ablt', 'loct',  # Падеж
                       'None']
morph_tags_photorus = ['изъявительное', 'повелительное', 'условное',  # наклонение
                       'совершенный', 'несовершенный',  # Вид
                       'переходный', 'непереходный',  # Переходность
                       'единсвтенное', 'множественное',  # Число
                       'мужской', 'женский', 'средний',  # Род
                       'первое', 'второе', 'третье',  # Лицо
                       'прошедшее', 'настоящее', 'будущее',  # Время
                       'именительный', 'родительный', 'дательный', 'винительный', 'творительный', 'предложный']  # Падеж
morph_tags_natasha = ['Ind', 'povel', 'Cnd',  # наклонение
                      'Perf', 'Imp',  # Вид
                      '-1', '-1',  # Переходность
                      'Sing', 'Plur',  # Число
                      'Masc', 'Fem', 'Neut',  # Род
                      '1', '2', '3',  # Лицо
                      'Past', 'Pres', 'Fut',  # Время
                      'Nom', 'Gen', 'Dat', 'Acc', 'Ins', 'Loc',  # Падеж
                      'None']


def noun_sn(string):
    if string[0] == string[0].upper():
        return "собственное"
    else:
        return "нарицательное"


def noun_on(string, i):
    morph = pymorphy2.MorphAnalyzer()
    p = morph.parse(string)[i]
    gent_case = p.inflect({'plur', 'gent'})
    accs_case = p.inflect({'plur', 'accs'})
    if gent_case is None or accs_case is None:
        return "неодушевлённое"
    if gent_case.word == accs_case.word:
        return "одушевлённое"
    else:
        return "неодушевлённое"


def verb_sp(string, i):
    morph = pymorphy2.MorphAnalyzer()
    p = morph.parse(string)[i]
    if p.tag.person == "1per":
        if p.tag.number == 'sing':
            if string[-1] == 'у' or string[-1] == 'ю':
                new_string = p.inflect({'plur'})[0]
                if new_string[-2:] == 'ем':
                    return "1-е"
                else:
                    return "2-e"
        else:
            if string[-2:] == 'ем':
                return "1-е"
            else:
                return "2-e"
    elif p.tag.person == "2per":
        if p.tag.number == 'sing':
            if string[-3:] == 'ешь':
                return "1-е"
            else:
                return "2-е"
        else:
            if string[-3:] == 'ете':
                return "1-е"
            else:
                return "2-е"
    else:
        if p.tag.number == 'sing':
            if string[-2:] == 'ет':
                return "1-е"
            else:
                return "2-е"
        else:
            if string[-2:] == 'ут' or string[-2] == 'ют':
                return "1-е"
            else:
                return "2-е"


def verb_vn(string):
    if string[-2:] == 'ся' or string[-2:] == 'сь':
        return "возвратный"
    else:
        return "невозвратный"


def noun_skl(string, i):
    morph = pymorphy2.MorphAnalyzer()
    p = morph.parse(string)[i]


def func_morphanalyze(string):
    morph = pymorphy2.MorphAnalyzer()
    for i in range(len(morph.parse(string))):
        p = morph.parse(string[:string.find('(')])[i]
        tag_case = morph_tags_pymorphy[morph_tags_natasha.index(string[string.find('Case:') + 5:string.find(']')])]
        tag_mood = morph_tags_pymorphy[morph_tags_natasha.index(string[string.find('[Mood:') + 6:string.find(',')])]
        if p.tag.POS == string[string.find('(') + 1:string.find(')')] and (
                p.tag.case == tag_case or p.tag.mood == tag_mood):
            morph_types = {"VERB": ({"Вид": p.tag.aspect, "Переходность": p.tag.transitivity,
                                     "Спряжение": verb_sp(string[:string.find('(')], i),
                                     "Возвратность": verb_vn(string[:string.find('(')])},
                                    {"Наклонение": p.tag.mood, "Число": p.tag.number, "Лицо": p.tag.person,
                                     "Род": p.tag.gender,
                                     "Время": p.tag.tense}),
                           "NOUN": (
                               {"Имя": noun_sn(string[:string.find('(')]),
                                "свойство": noun_on(string[:string.find('(')], i),
                                "Род": p.tag.gender, "Склоннеие": noun_skl(string[:string.find('(')], i)},
                               {"Число": p.tag.number, "Падеж": p.tag.case})}

            ret = {
                'part_of_speech': {
                    'part': pos_tags_photorus[pos_tags_pymorphy.index(p.tag.POS)],
                    'initial_form': p.normal_form,
                },
                'morph_features': {'persistent_signs': {},
                                   'irregular_signs': {}},
                'syntactic_role': string[string.find("<") + 1:string.find(">")]
            }

            op = morph_types[p.tag.POS][0]
            for key, val in op.items():
                if op[key] is None:
                    ret['morph_features']['persistent_signs'][key] = None
                else:
                    try:
                        ret['morph_features']['persistent_signs'][key] = morph_tags_photorus[
                            morph_tags_pymorphy.index(str(op[key]))]
                    except ValueError:
                        ret['morph_features']['persistent_signs'][key] = val

            nop = morph_types[p.tag.POS][1]
            for key, val in nop.items():
                if nop[key] is None:
                    ret['morph_features']['irregular_signs'][key] = None
                else:
                    try:
                        ret['morph_features']['irregular_signs'][key] = morph_tags_photorus[
                            morph_tags_pymorphy.index(str(nop[key]))]
                    except ValueError:
                        ret['morph_features']['irregular_signs'][key] = val

            res = {'parsed': True, 'data': ret}
            return res
        return {'parsed': False}
