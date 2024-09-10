import json
from datetime import date, timedelta


currentDeck = []

def getNextRotation():
    today = date.today()
    rotationday = date(today.year, 6, 30)
    if rotationday < today:
        rotationday = date(today.year+1, 6, 30)
    return rotationday

def extractSets():
    with open("sets.json", "r") as setsjson:
        sets = json.load(setsjson)["data"]
    rotationday = getNextRotation()
    today = date.today()
    standardsets = []
    for mtgset in sets:
        setdate = mtgset["released_at"]
        settype = mtgset["set_type"]
        setname = mtgset["name"]
        setcode = mtgset["code"]
        setdate = date.fromisoformat(setdate)
        if (settype in ("core", "expansion")) and is_legal_date(setdate, rotationday, today):
            # print(f"{setname} ({setcode}): {settype}, {setdate}")
            standardsets.append({"name":setname, "date":setdate, "code":setcode, "type":settype})
    return standardsets

def is_legal_date(setdate, rotationday, today):
    return (setdate + timedelta(days=365.25*3) > rotationday) and (setdate<today)


def willrotate(mtgset):
    rotationday = getNextRotation()
    return not (mtgset["date"] + timedelta(days=365.25*2) > rotationday)

def rotatingSets():
    out = []
    for mtgset in standard_sets:
        if willrotate(mtgset):
            out.append(mtgset["code"])
    return out

standard_sets = extractSets()
rotating_sets = rotatingSets()

print(rotating_sets)

class Deck():
    @staticmethod
    def fromfile(filename):
        name = filename[:-4]
        mainboard = []
        sideboard = []
        detail = dict()

        with open('../oracle-cards.json', 'r', encoding='utf8') as cards:
            pycards = json.load(cards)
        pycards:dict[str,dict] = {card['name']:card for card in pycards}
        def __add_split_cards():
            splitcards:dict = dict()
            for cardname in pycards:
                sep = cardname.find(" // ")
                if sep>-1:
                    splitcards[cardname[:sep]] = pycards[cardname]
            for k,v in splitcards.items():
                if k not in pycards:
                    pycards[k] = v
        __add_split_cards()

        with open("decks/"+filename,"r") as deck:
            addlist = mainboard
            for line in deck.readlines():
                if line == "\n":
                    addlist = sideboard
                    continue
                count, cardname = line.split(" ", maxsplit=1)
                count = int(count)
                cardname = cardname.strip()
                cardname = pycards[cardname]["name"]
                addlist.append((count, cardname))
        for _, cardname in mainboard:
            detail[cardname] = pycards[cardname]
        for _, cardname in sideboard:
            detail[cardname] = pycards[cardname]
        # return {"name":name, "mainboard":mainboard, "sideboard":sideboard, "detail":detail}
        return Deck(name, mainboard, sideboard, detail)

    def __init__(self, name, mainboard, sideboard, detail) -> None:
        self.name:str = name
        self.mainboard:list[tuple[int, str]] = mainboard
        self.sideboard:list[tuple[int, str]] = sideboard
        self.detail:dict[str,dict[str]] = detail

    def __str__(self) -> str:
        out = ""
        for count, cardname in self.mainboard:
            out += str(count)+" "+cardname+"\n"
        out+="\n"
        for count, cardname in self.sideboard:
            out += str(count)+" "+cardname+"\n"
        # out+="\n"
        return out

    def getlen(self):
        mainlen = 0
        for count, _ in self.mainboard:
            mainlen += count
        sidelen = 0
        for count, _ in self.sideboard:
            sidelen += count
        return mainlen, sidelen, mainlen + sidelen
    
    def unique(self):
        return list(self.detail.keys())
    
    def is_legal(self):
        for card in self.detail.values():
            if card["legalities"]["standard"] != "legal":
                return False
        mainlen, sidelen, totallen = self.getlen()
        return (mainlen >= 60) and (sidelen <= 15) and (totallen <= 75)
