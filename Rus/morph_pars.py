from pprint import pprint

from pymorphy2 import MorphAnalyzer
from .ru_morph_dict import (morph_to_rus_case, morph_to_rus_part, morph_to_rus)


class MorphParser(MorphAnalyzer):
    def __init__(self):
        super().__init__()
        self.global_now = None
        self.now = None
        self.word = None

    def main_pars(self, word, first=False):
        self.word = word
        self.global_now = self.parse(word)
        if first:
            self.global_now = self.global_now[:1]
        ret = []
        for self.now in self.global_now:
            dict_now = self.sings()
            dict_now['word'] = word
            dict_now['normal_form'] = self.now.normal_form
            dict_now['part'] = morph_to_rus_part[self.now.tag.POS]
            ret.append(dict_now)
        return ret

    def sings(self):
        sings = {  # lambda :
            'NOUN': self.part_noun,
            "ADJF": lambda: self.part_adj(True),
            "ADJS": lambda: self.part_adj(False),
            "COMP": self.part_comp,
            "VERB": self.part_verb,
            "INFN": self.part_infn,
            "PRTF": lambda: self.part_prt(True),
            "PRTS": lambda: self.part_prt(False),
            "GRND": self.part_grnd,
            "NUMR": self.part_numr,
            "ADVB": self.part_advb,
            "NPRO": self.part_npro,
        }
        ret = sings.get(self.now.tag.POS)
        if ret:
            return ret()
        return {'regular_signs': {}, 'irregular_signs': {}}

    def part_noun(self):
        declin = self.declin()
        return {
            'regular_signs': {
                "proper": self.proper(),
                "animacy": morph_to_rus[self.now.tag.animacy],
                "gender": morph_to_rus[self.now.tag.gender],
                "declin": str(declin)
            },
            'irregular_signs': {
                "number": morph_to_rus[self.now.tag.number],
                "case": morph_to_rus_case[self.now.tag.case]
            },
            'ru_regular_signs': [
                self.proper(),
                morph_to_rus[self.now.tag.animacy],
                morph_to_rus[self.now.tag.gender] + " род",
                str(declin) + " склонение",
            ],
            'ru_irregular_signs': [
                morph_to_rus_case[self.now.tag.case] + " падеж",
                morph_to_rus[self.now.tag.number] + " число"
            ],
        }

    def part_adj(self, is_full=True):
        full = {True: 'полня форма', False: 'неполная форма'}[is_full]
        ret = {
            "regular_signs": {
                "class": self.adj_class()},
            "irregular_signs": {
                "full_form": is_full,
                "number": morph_to_rus[self.now.tag.number],
                "gender": morph_to_rus[self.now.tag.gender]},

            'ru_regular_signs': [self.adj_class()],
            'ru_irregular_signs': [
                full,
                morph_to_rus[self.now.tag.number] + " число",
                str(morph_to_rus[self.now.tag.gender]) + " род",
            ],
        }
        if is_full:
            ret['irregular_signs']['case'] = str(morph_to_rus_case[self.now.tag.case]) + ' падеж'
            ret['ru_irregular_signs'].append(morph_to_rus_case[self.now.tag.case] + " падеж")
        return ret

    def part_comp(self):
        cls = self.adj_class()
        return {
            "regular_signs": {
                "class": cls},
            "irregular_signs": {},
            'ru_regular_signs': [cls],
            'ru_irregular_signs': [],
        }

    def part_verb(self):
        conj = self.conj()
        return {
            "regular_signs": {
                "aspect": morph_to_rus[self.now.tag.aspect],
                "transitivity": morph_to_rus[self.now.tag.transitivity],
                "conj": str(conj) + ' спряжение',
                "returnable": self.returnable()},
            "irregular_signs": {
                "mood": morph_to_rus[self.now.tag.mood],
                "number": morph_to_rus[self.now.tag.number],
                "person": morph_to_rus[self.now.tag.person],
                "gender": morph_to_rus[self.now.tag.gender],
                "tense": morph_to_rus[self.now.tag.tense]
            },
            'ru_regular_signs': [
                morph_to_rus[self.now.tag.aspect] + ' вид',
                str(conj) + ' спряжение',
                morph_to_rus[self.now.tag.transitivity],
                self.returnable()
            ],
            'ru_irregular_signs': [
                morph_to_rus[self.now.tag.mood] + ' наклонение',
                morph_to_rus[self.now.tag.number] + " число",
                str(morph_to_rus[self.now.tag.tense]) + " время",
                str(morph_to_rus[self.now.tag.person]) + ' лицо',
                str(morph_to_rus[self.now.tag.gender]) + " род",
            ],
        }

    def part_infn(self):
        conj = self.conj()
        return {
            "regular_signs": {
                "aspect": morph_to_rus[self.now.tag.aspect],
                "transitivity": morph_to_rus[self.now.tag.transitivity],
                "conj": str(conj) + ' спряжение',
                "returnable": self.returnable()},
            "irregular_signs": {},
            'ru_regular_signs': [
                morph_to_rus[self.now.tag.aspect] + ' вид',
                str(conj) + ' спряжение',
                morph_to_rus[self.now.tag.transitivity],
                self.returnable()
            ],
            'ru_irregular_signs': [],
        }

    def part_prt(self, is_full):
        full = {True: 'полня форма', False: 'неполная форма'}[is_full]
        ret = {
            "regular_signs": {
                "aspect": morph_to_rus[self.now.tag.aspect],
                "tense": morph_to_rus[self.now.tag.tense],
                "voice": morph_to_rus[self.now.tag.voice],
            },
            "irregular_signs": {
                "full_form": is_full,
                "number": morph_to_rus[self.now.tag.number],
                "gender": morph_to_rus[self.now.tag.gender]
            },
            'ru_regular_signs': [
                morph_to_rus[self.now.tag.voice],
                morph_to_rus[self.now.tag.tense] + " время",
                morph_to_rus[self.now.tag.aspect],
            ],
            'ru_irregular_signs': [
                full,
                morph_to_rus[self.now.tag.number] + " число",
                morph_to_rus[self.now.tag.gender] + " род",
            ],
        }
        if is_full:
            ret['irregular_signs']['case'] = str(morph_to_rus_case[self.now.tag.case]) + ' падеж'
            ret['ru_irregular_signs'].append(morph_to_rus_case[self.now.tag.case] + " падеж")
        return ret

    def part_grnd(self):
        return {
            "regular_signs": {
                "aspect": morph_to_rus[self.now.tag.aspect],
                "transitivity": morph_to_rus[self.now.tag.transitivity],
                "returnable": self.returnable(),
            },
            "irregular_signs": {},
            'ru_regular_signs': [
                morph_to_rus[self.now.tag.aspect],
                morph_to_rus[self.now.tag.transitivity],
                self.returnable()
            ],
            'ru_irregular_signs': [],
        }

    def part_numr(self):
        return {
            "regular_signs": {},
            "irregular_signs": {
                "number": morph_to_rus[self.now.tag.number],
                "case": morph_to_rus_case[self.now.tag.case] + ' падеж',
                "gender": morph_to_rus[self.now.tag.gender]
            },
            'ru_regular_signs': [],
            'ru_irregular_signs': [
                morph_to_rus_case[self.now.tag.case] + " падеж",
                morph_to_rus[self.now.tag.number] + " число",
                morph_to_rus[self.now.tag.gender] + " род"

            ]
        }

    def part_advb(self):
        return {
            "regular_signs": {
                "extend": None,  # доделать
            },
            "irregular_signs": {},
            'ru_regular_signs': [],
            'ru_irregular_signs': []
        }

    def part_npro(self):
        return {
            "regular_signs": {
                "class": self._class(),
                "person": morph_to_rus[self.now.tag.person],
            },
            "irregular_signs": {
                "number": morph_to_rus[self.now.tag.number],
                "case": morph_to_rus_case[self.now.tag.case] + ' падеж',
                "gender": morph_to_rus[self.now.tag.gender]
            },
            'ru_regular_signs': [
                self._class(),
                str(morph_to_rus[self.now.tag.person]) + ' лицо',
            ],
            'ru_irregular_signs': [
                morph_to_rus_case[self.now.tag.case] + " падеж",
                morph_to_rus[self.now.tag.number] + " число",
                morph_to_rus[self.now.tag.gender] + " род"
            ],
        }

    def adj_class(self):
        if 'Qual' in self.now.tag:
            return "Качественное"
        if 'Poss' in self.now.tag:
            return "Притяжательное"
        return "Относительное"

    def adv_class(self):  # доделать
        if 'Qual' in self.now.tag:
            return "Качественное"
        if 'Poss' in self.now.tag:
            return "Притяжательное"
        return "Относительное"

    def proper(self):
        if self.word[0] == self.word[0].upper():
            return "собственное"
        return "нарицательное"

    def returnable(self):
        if self.word[-2:] == 'ся' or self.word[-2:] == 'сь':
            return 'возвратный'
        return 'невозвратный'

    def conj(self):
        first = ('брить', 'стелить')
        second = ('гнать', 'держать', 'терпеть', 'обидеть', 'видеть', 'слышать',
                  'ненавидеть', 'зависеть', 'вертеть', 'дышать', 'смотреть')
        word = self.now.normal_form.lower()
        if word in first:
            return 1
        elif word in second:
            return 2
        if 'ить' in word:
            return 2
        return 1

    def _class(self):
        word = self.now.normal_form
        raz = {
            "личное": ["я", "ты", "он", "она", "оно", "мы", "вы", "они"],
            "возвратное": ["себя"],
            "вопросительное": ["кто", "что", "какой", "который", "чей", "сколько"],
            "неопределённое": ["некто", "нечто", "некоторый", "некий", "несколько"],
            "отрицательное": ["никто", "ничто", "некого", "нечего", "никакой", "ничей"],
            "притяжательное": ["мой", "твой", "ваш", "наш", "свой", "его", "её", "их"],
            "указательное": ["этот", "тот", "такой", "таков", "столько", "сей", "оный"],
            "определительное": ["сам", "самый", "весь", "всякий", "каждый", "любой", "другой", "иной", "всяк",
                                "всяческий"]
        }
        for key, val in raz.items():
            if word in val:
                return key
        if word[:4] == "кое":
            return "неопределённое"
        if word.split('-')[-1] == "то" or word.split('-')[-1] == "нибудь" or word.split('-')[-1] == "либо":
            return "неопределённое"
        return None

    def declin(self):
        if self.now.tag.gender == "masc" or self.now.tag.gender == "femn":
            if self.now.normal_form[-1] == "а" or self.now.normal_form[-1] == "я":
                return 1
            if self.now.normal_form[-1] == "ь" and self.now.tag.gender == "femn":
                return 3
        return 2


if __name__ == '__main__':
    m = MorphParser()
    while True:
        xx = m.main_pars(input())
        for x in xx:
            pprint(x)
            print(f"часть речи:\t{x['part']}")
            print(f"начальная форма:\t{x['normal_form']}")
            print('постоянные признаки:', end='\n\t')
            print('\n\t'.join(map(str, x['regular_signs'].values())))
            print('непостоянные признаки:', end='\n\t')
            print('\n\t'.join(map(str, x['irregular_signs'].values())))
            print()
