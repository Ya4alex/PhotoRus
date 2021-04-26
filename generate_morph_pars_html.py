from Rus.Logic import Logic
from Rus.dictionaries import transl_to_lines
from pprint import pprint
from dominate.tags import *
from flask import render_template

LOGIC = Logic()


class GenerateMorphPars:
    def main_generate(self, text):
        sentences = LOGIC.json_pars(text)
        ret = div(cls="class")
        for sent in sentences:
            ret.add(self.sent_generate(sent))
        return ret.render()

    def sent_generate(self, sent):
        ret = div(cls="main fon")
        group = {'tag': False, 'id': False}
        container = None
        for word in sent['content']:
            if group['tag'] == word['relations']['group']['tag'] and group['id'] == word['relations']['m_head_id']:
                line = transl_to_lines[word['feathers']['natasha_tag']]
                if line == 'pretext' or line == 'union':
                    h_word = span(cls=f"{line} word")
                elif word['feathers']['natasha_tag'] == 'punct':
                    h_word = span()
                else:
                    h_word = span(cls="word")
                h_word.add(word['word'])
                self.set_title(h_word, word)
                container.add(h_word)
                continue

            elif group['tag'] and word['relations']['m_head_id'] != group['id']:
                dv = div(cls=f"{group['tag']} fon")
                dv.add(container)
                ret.add(dv)

                group = {'tag': False, 'id': False}
                container = None

            if not group['tag'] and not group['id'] and word['relations']['group']['tag'] in ('acl', 'gerund', 'amod'):
                group = {'tag': word['relations']['group']['tag'], 'id': word['relations']['m_head_id']}
                container = span(
                    cls={'amod': 'wavy_line',
                         'acl': 'wavy_line',
                         'gerund': 'dash_dotted_line'}[word['relations']['group']['tag']])

                line = transl_to_lines[word['feathers']['natasha_tag']]
                if line == 'pretext' or line == 'union':
                    h_word = span(cls=f"{line}")
                else:
                    h_word = span()
                h_word.add(word['word'])
                self.set_title(h_word, word)
                container.add(h_word)
                continue

            if transl_to_lines[word['feathers']['natasha_tag']]:
                h_word = span(
                    cls=f"{transl_to_lines[word['feathers']['natasha_tag']]} word",
                )
            elif word['feathers']['natasha_tag'] == 'punct':
                h_word = span()

            else:
                h_word = span(cls="word")
                h_word = div(cls='main fon').add(h_word)
            h_word.add(word['word'])
            self.set_title(h_word, word)
            ret.add(h_word)
        return ret

    def set_title(self, h_word, word):
        h_word.set_attribute('title',
                             "{}\n{}\n{}\nid:{} h_id:{} m_h_id:{}".format(
                                 word['feathers']['photorus_tag'], word['feathers']['natasha_tag'],
                                 word['relations']['group']['human_tag'], word['relations']['id'],
                                 word['relations']['head_id'], word['relations']['m_head_id']))
        return h_word

    def plug(self):
        return div()
