from prompt_toolkit.document import Document
from jutils import *
import json
import csv
import re
from collections import namedtuple

import prompt_toolkit as pt
from prompt_toolkit.validation import Validator, ValidationError, ThreadedValidator
from prompt_toolkit.completion import FuzzyWordCompleter, ThreadedCompleter
from fuzzyfinder import fuzzyfinder


class NumberValidator(Validator):
    def __init__(self, max=None) -> None:
        self.max = max
        
    def validate(self, document):
        text = document.text
        if text:
            if not text.isdigit():
                i = 0
                for i, c in enumerate(text):
                    if not c.isdigit():
                        break
                raise ValidationError(message='This input contains non-numeric characters',
                                      cursor_position=i)
            if self.max and int(text)>self.max:
                raise ValidationError(0, f'This is too high, enter a number <={self.max}')

class CardValidator(Validator):
    def __init__(self, names, msg) -> None:
        self.msg = msg
        self.names = names
    def validate(self, document: Document) -> None:
        text = document.text
        if text and text not in self.names:
            raise ValidationError(0,self.msg)

def getCube():
    with open('cube.csv', 'r', encoding='utf8') as cards:
        pycube = list(csv.DictReader(cards))
        cubenames = list(card['name'] for card in pycube)
    return pycube, cubenames

with open('oracle-cards.json', 'r', encoding='utf8') as cards:
    pycards = json.load(cards)
    names = tuple(card['name'] for card in pycards)

_, cubenames = getCube()

mtg_completer = ThreadedCompleter(FuzzyWordCompleter(names))

card_validator = ThreadedValidator(CardValidator(names, "Not a valid card"))

Styler = namedtuple('Styler',['rex', 'tag'])
stylers = [
    Styler(r'Cube', 'blueviolet'),
    Styler(r'Add', 'seagreen'),
    Styler(r'Search', 'steelblue'),
    Styler(r'Remove', 'maroon'),
    Styler(r'Quit', 'darkgrey'),
]

def style_text(text:str):
    tags = dict()
    for styler in stylers:
        matches = re.finditer(r'\['+styler.rex+r"\]", text)
        if matches == None:
            continue

        if isinstance(styler.tag,str):
            start_tag = f'<{styler.tag}>'
            end_tag = f'</{styler.tag}>'
        else:
            start_tag = f'<{styler.tag[0]} {" ".join(styler.tag[1:])}>'
            end_tag = f'</{styler.tag[0]}>'

        for m in matches:
            s,e = m.span()
            text = text[:s]+start_tag+text[s+1:e-1]+end_tag+text[e:]
    return text

def get(cube, name):
    for i, row in enumerate(cube):
        if row["name"]==name:
            return i, row
    return None, None

def add_to_cube():
    card_to_add = None
    card_to_add = pt.prompt('What card should be added?\n>',
                            completer=mtg_completer, complete_while_typing=True, complete_in_thread=True,
                            validator=card_validator, validate_while_typing=False)        
    pycube, cubenames = getCube()

    row_i, row = get(pycube, card_to_add)
    if row_i == None:
        count = 0
    else:
        count = int(row['count'])
    
    # for i, row in enumerate(pycube):
    #     if row['name']==card_to_add:
    #         row_i = i
    #         count = int(row['count'])
    #         break

    num_to_add = int(pt.prompt(f'How many should be added? (you currently have {count})\n>', 
                               validator=NumberValidator()))
    total_num_after_add = num_to_add + count

    confirmation = pt.prompt(f'Adding {card_to_add} x{num_to_add} ({count}->{total_num_after_add})\n Confirm? (X to cancel)\n>'
                             ).lower()
    if "x" in confirmation or confirmation.find("cancel")>=0 or confirmation.find("no")>=0:
        return
    
    if row_i == None:
        row_i = len(pycube)
        pycube.append({"name":card_to_add, "count":str(total_num_after_add)})
        cubenames.append(card_to_add)

    pycube[row_i]['count'] = str(total_num_after_add)
    with open('cube.csv', 'w') as cube_w:
        writer = csv.DictWriter(cube_w, fieldnames=["name","count"], dialect="unix")
        writer.writeheader()
        writer.writerows(pycube)


def search_cube():
    pycube, cubenames = getCube()
    search_term = pt.prompt("Type your Search below\n>", completer=FuzzyWordCompleter(cubenames))

    res = list(fuzzyfinder(search_term, cubenames))
    for row in pycube:
        for i, n in enumerate(res):
            if row['name'] == n:
                res[i] += " x"+row['count']

    pt.print_formatted_text('\n'.join(res))
    pt.prompt("")
    

def remove_from_cube():
    pycube, cubenames = getCube()
    card_to_remove = pt.prompt("What should be removed?\n>",
                                validator=ThreadedValidator(CardValidator(cubenames, "Not in Cube")),
                                completer=FuzzyWordCompleter(cubenames))
    i, row = get(pycube, card_to_remove)
    num_removable = int(row["count"])
    num_to_remove = int(pt.prompt(f'How many should be removed? (out of {num_removable})\n>',
                                    validator=NumberValidator(max=num_removable)))
    total_num_after_remove = num_removable - num_to_remove
    confirmation = pt.prompt(f'Removing {card_to_remove} x{num_to_remove} ({num_removable}->{total_num_after_remove})\n Confirm? (X to cancel)\n>'
                             ).lower()
    if "x" in confirmation or confirmation.find("cancel")>=0 or confirmation.find("no")>=0:
        return
    if total_num_after_remove == 0:
        pycube = pycube[:i]+pycube[i+1:]
    else:
        pycube[i]['count'] = str(total_num_after_remove)

    with open('cube.csv', 'w') as cube_w:
        writer = csv.DictWriter(cube_w, fieldnames=["name","count"], dialect='unix')
        writer.writeheader()
        writer.writerows(pycube)
    

Option = namedtuple('Option',['text', 'func', 'keyword'])
options = [
    Option(style_text('[Add] to Cube'), add_to_cube, 'Add'),
    Option(style_text('[Search] Cube'), search_cube, 'Search'),
    Option(style_text('[Remove] from Cube'), remove_from_cube, 'Remove'),
    Option(style_text('[Quit] program'), exit, 'Quit'),
]

pt.shortcuts.clear()
while 1:
    pt.print_formatted_text(pt.HTML(style_text('\n<b>Welcome to the [Cube].</b>\n')
                                    +'Choose from the following options: \n'
                                    +'\n'.join(o.text for o in options)))
    invalid_option = True
    while invalid_option:
        opt = pt.prompt(">",completer=FuzzyWordCompleter([o.keyword for o in options])).strip()
        for o in options:
            if opt == o.keyword:
                invalid_option = False
                o.func()
                break
