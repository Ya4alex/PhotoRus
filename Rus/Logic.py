from .Grammarchecker import func_grammarchecker
import nltk


class Logic:
    def __init__(self):
        pass

    def json_pars(self, text, check_grammar=False):
        sentences = nltk.sent_tokenize(text.replace('...', '.'), language="russian")

        ret = []
        for sent in sentences:
            print(sent)
            ret.append(func_grammarchecker(sent))

        return ret


if __name__ == '__main__':
    log = Logic()
    log.json_pars(input())
