from PIL import Image, ImageDraw, ImageFont
import os, sys
from dataclasses import dataclass
from enum import Enum, StrEnum
from card import *

BELEREN = "typeface-beleren-bold-master/Beleren2016-Bold.ttf"
BELEREN_SC = "typeface-beleren-bold-master/Beleren2016SmallCaps-Bold.ttf"
BELEREN_IT = "typeface-beleren-bold-master/Beleren2016SmallCaps-BoldItalic.ttf"
class Font(StrEnum):
    BELEREN_SC = "fonts/Beleren Small Caps.ttf"
    BELEREN = "fonts/Beleren-Bold.ttf"
    BELEREN_J = "fonts/JaceBeleren-Bold.ttf"
    MPLANTIN = "fonts/MPlantin.ttf"
    MPLANTIN_B = "fonts/MPlantin-Bold.ttf"
    MPLANTIN_I = "fonts/MPlantin-Italic.ttf"
    MANA = "fonts/mana.ttf"


@dataclass
class Template:
    filename:str
    name_pos:tuple[float]
    type_pos:tuple[float]
    mana_pos:tuple[float]
    oracle_pos:tuple[float]
    flavor_pos:tuple[float]
    pt_pos:tuple[float]
    big_font:ImageFont
    small_font:ImageFont
    fontsize:int

templates = {
    "blackcreature": Template("blackcreature.jpg", (90, 125), (100, 815), (879,125),(105, 870),(105, 1185),(814,1260), ImageFont.truetype(Font.BELEREN_J, 48), ImageFont.truetype(Font.BELEREN,36), 48)
}


def write_to(d:ImageDraw, text:str, pos:tuple[float], font:ImageFont):
    d.text(pos, text, fill="black", anchor="ls", font=font)

def add_mana(mana:str, image:Image, template:Template):
    mask = Image.open("mana-icons/mask.png")
    mask = mask.resize((template.fontsize, template.fontsize))
    i = 0
    for ms in reversed(mana.split("}")):
        if len(ms)>1:
            ms = ms[1:].replace("/","").lower()
            img = Image.open("mana-icons/ms-"+ms+".png")
            img = img.resize((template.fontsize, template.fontsize))
            image.paste(img, (template.mana_pos[0]-i-img.size[0], template.mana_pos[1]-int(0.8*img.size[1])), mask)
            i+=img.size[0]+template.fontsize//10


def write(card:Creature, template:Template):
    im = Image.open("templates/blackcreature.jpg")
    d = ImageDraw.Draw(im)
    d.text(template.name_pos, card.name, fill="black", anchor="ls", font=template.big_font)
    # d.text(template.mana_pos, card.mana_cost, fill="black", anchor="rs", font=template.big_font)
    d.text(template.type_pos, card.type_line, fill="black", anchor="ls", font=template.big_font)
    d.text(template.pt_pos, card.power+"/"+card.toughness, fill="black", anchor="ms", font=template.big_font)
    # d.multiline_text(template.oracle_pos, card.oracle, fill="black", font=template.small_font)
    d.multiline_text(template.oracle_pos, card.oracle, fill="black", font=ImageFont.truetype(Font.MPLANTIN,36), anchor="la", spacing=6)
    d.multiline_text(template.flavor_pos, card.flavor, fill="black", font=ImageFont.truetype(Font.MPLANTIN_I,36), anchor="ld")
    add_mana(card.mana_cost, im, template)
    
    im.show()




test = Creature("Sir Meowthus, Timetwister","{2}{U}{R}","Legendary Creature - Cat Wizard", 
                "Flash, Storm\n\nWhenever Sir Meowthus, Timetwister dies, \nreturn target card in your graveyard to the \nbottom of your library.", 
                "The ripples of his sacrifices can be felt - signs of \nselfless acts lost to all memory.", "", "", "1", "4")

write(test, templates["blackcreature"])

def show_card(card):
    pass