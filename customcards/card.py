from dataclasses import dataclass
from enum import Enum


class Colors(Enum):
    COLORLESS =  0
    RED   = 1 << 0
    GREEN = 1 << 1
    BLUE  = 1 << 2
    WHITE = 1 << 3
    BLACK = 1 << 4

def valid_pt(string:str):
    string = string.replace(" ","")
    if string.isdigit():
        return True, int(string)
    x = 0
    for n in string.split("+"):
        if n=="*":
            x+=0
        elif n.isdigit():
            x+=int(n)
        else:
            return False, 0
    return True, x



@dataclass
class Card:
    """The parts of a card are name, mana cost, illustration, 
    color indicator, type line, expansion symbol, text box, 
    power and toughness, 
    loyalty, 
    hand modifier, life modifier, 
    illustration credit, legal text, and collector number.
    Some cards may have more than one of any or all of these parts."""
    name:str
    mana_cost:str
    type_line:str
    oracle:str
    flavor:str
    art_link:str
    art_credit:str
    
@dataclass
class Creature(Card):
    power:str
    toughness:str




