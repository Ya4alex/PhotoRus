import string
import enchant
import re


def sent_spellchecker(par_sent):
    return par_sent.translate(str.maketrans('', '', string.punctuation))


class Grammar:
    def __init__(self):
        self.dictionary = enchant.Dict("ru_RU")

    def spellcheck(self, word):
        if not self.dictionary.check(word):
            result = self.dictionary.suggest(word)
            if result:
                return result[0]
        return word

    def sent_spellcheck(self, pars):
        return ' '.join([self.spellcheck(i) for i in pars.split()])


def sent_split(paragraph):
    """ break a paragraph into sentences
        and return a list """

    sentenceEnders = re.compile('[.!?]')
    sentenceList = sentenceEnders.split(paragraph)
    return sentenceList


if __name__ == '__main__':
    log = Grammar()
    while True:
        print(log.spellcheck(input()))
