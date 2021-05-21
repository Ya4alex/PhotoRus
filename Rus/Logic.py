from .syntactic_parsing import syntactic_parser
from .morph_pars import MorphParser
from .Grammar import Grammar
import nltk


class Logic:
    def __init__(self):
        self.grammar = Grammar()
        self.morph = MorphParser()

    def syntactic_pars(self, text, check_grammar=False):
        if check_grammar:
            text = self.grammar.sent_spellcheck(text)

        sentences = nltk.sent_tokenize(text.replace('...', '.'), language="russian")

        ret = []
        for sent in sentences:
            ret.append(syntactic_parser(sent))
        return ret

    def morph_pars(self, word, first=False, check_grammar=False):
        word = word.split()[0]
        if check_grammar:
            word = self.grammar.spellcheck(word)
        return self.morph.main_pars(word, first)
