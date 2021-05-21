from Rus.Logic import Logic
from Rus.dictionaries import transl_to_lines
from pprint import pprint
from dominate.tags import div, span, table, th, tr, td, tbody, nav, ul, li, a

LOGIC = Logic()


class GenerateSyntacticPars:
    def main_generate(self, text, grammar_check=False):
        sentences = LOGIC.syntactic_pars(text, grammar_check)
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
                dv = div(cls=f"{group['tag']} fon2")
                dv.add(container)
                ret.add(dv)

                group = {'tag': False, 'id': False}
                container = None

            if not group['tag'] and not group['id'] and word['relations']['group']['tag'] in ('partic', 'gerund'):
                group = {'tag': word['relations']['group']['tag'], 'id': word['relations']['m_head_id']}
                container = span(
                    cls={'partic': 'wavy_line',
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

            if transl_to_lines.get(word['feathers']['natasha_tag']):
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
        h_word.set_attribute(
            'title',
            "{}\n{}\n{}\nid:{} h_id:{} m_h_id:{}".format(
                word['feathers']['photorus_tag'], word['feathers']['natasha_tag'],
                word['relations']['group']['human_tag'], word['relations']['id'],
                word['relations']['head_id'], word['relations']['m_head_id']))
        return h_word

    def plug(self):
        return div()


class GenerateMorphPars:
    def __init__(self):
        pass

    def main_generate(self, word, check_grammar=False):
        pars = LOGIC.morph_pars(word, check_grammar)
        ret = div()
        but = ul()
        for i, part in enumerate(pars):
            ret.add(self.part_generate(part, i))
            but.add(li(a(f"{part['part']}", href=f"#yak{i}"), cls="morph_btn"))
        return ret.render(), nav(but, id="menu").render()

    def part_generate(self, part, i):
        body = tbody()
        body.add(*self.parts(part))
        return div(table(body, cls="table table-sm morph_table"), cls='var', id=f"yak{i}")

    def parts(self, part):
        part_speech = tr()
        part_speech.add(th('часть речи'))
        part_speech.add(td(div(part['part'], cls='main part')))

        normal_form = tr()
        normal_form.add(td('начальная форма'))
        normal_form.add(td(div(part['normal_form'], cls='main normal_form')))

        value = div(cls='main regular')
        for v in map(str, part['ru_regular_signs']):
            value.add(div(v, cls='main sig'))
        if not part['ru_regular_signs']:
            value.add('нет постоянных признаков')
        regular_signs = tr()
        regular_signs.add(td('постоянные признаки'))
        regular_signs.add(td(value))

        value = div(cls='main irregular')
        for v in map(str, part['ru_irregular_signs']):
            value.add(div(v, cls='main sig'))
        if not part['ru_irregular_signs']:
            value.add('нет непостоянных признаков')
        irregular_signs = tr()
        irregular_signs.add(td('непостоянные признаки'))
        irregular_signs.add(td(value))

        return part_speech, normal_form, regular_signs, irregular_signs

    def plug(self):
        return div()
