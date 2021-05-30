import enchant.checker


class Grammar:
    def __init__(self):
        return
        self.dictionary = enchant.Dict("ru_RU")
        self.checker = enchant.checker.SpellChecker("ru_RU")

    def spellcheck(self, word):
        return word
        if not self.dictionary.check(word):
            result = self.dictionary.suggest(word)
            if result:
                return result[0]
        return word

    def sent_spellcheck(self, text):
        return text
        self.checker.set_text(text)
        for err in self.checker:
            suggest = err.suggest()
            if suggest:
                err.replace(suggest[0])

        return self.checker.get_text()


if __name__ == '__main__':
    g = Grammar()
    print(g.spellcheck('Солга'))
