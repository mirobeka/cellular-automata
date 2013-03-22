from cellular_automata.cells.cell import Cell
from cellular_automata.lattices.base import Lattice

class VoronoiLattice(Lattice):
  def __init__(self):
    # TODO
    pass
'''
NEIGHBOURHOOD
Ďalšou vecou s ktorou sa treba popasovať sú susedstvá. Treba vedieť ako ich nastaviť tak aby správne fungovali. Takže v tomto prípade môžeme spraviť to, žeby sme bunke poskytli uhol, ktorý medzi sebou svierajú. Bunka môže by ako center a uhol ostatnej bunky už vieme zistiť. Takže takto by sme si mohli udržať susedstvo. Dictionary s kľúčom ako je uhol. miesto množiny susednov z jedného smeru. Uhol bude vždy unikátny pre každého suseda, takže ho bude môcť neurónka presne identifikovať.

NEURAL NETWORK VARIABLE INPUT
Tp u narážame na ďalší problém. ako skonštruovať neurónovú sieť s variabilnou dĺžkou vstupu? V tomto prípade mi na um prichádza riešenie tým, žeby sme vyhodili susedov a proste sčítali všetky chemikálie a stavy dokopy. Aj takéto automaty sa nejako volajú. Totalistické. To sú presne tie ktoré mám na mysli.

MERGE
Ok, poďme na ďalší problém. Ako vyriešim tú zmenu mriežky? V takom prípade musím bunky nejakým korektným a rýchlim spôsobom spojiť. Mohol by som sa tak márne zamyslieť nad tým, ale pochybujem, že tu niečo také bude k dosiahnutiu. K tomu spojeniu. Niečo ako, žeby som istým spôsobom upravil len to čo je treba. Všetko ostatné by zostalo nedotknuté. By by ešte aj urýchlilo tento spôsob. Zainvolvovať len tie bunky, ktorých hrany treba prepočítať a ostatné nechať na pokoji. Ale prvotné bežiace riešenie by mohlo byť, že prejdem cez všetky bunky ešte raz a vygenerujem celú mriežku ešte raz.

Center novej bunky bude v polovici úsečky, ktorú tvoria. Tu je výhoda, že sa môžu spájať po jednej. To je to čo chýba tej pracouhlej. To, že sa tam nedajú bunky spájať samostatne. Možno aj to by stálo za pozretie.


DIVISION
Tak isto ako merge. Zoberiem jednu bunku a rozdelím ju tak, aby to už bolo fajn? To ide? Dá sa rozdeliť jedna bunka, tak, že sa to proste stále bude tváriť ako voronoi? NO to by som si pozrel. V inom prípade si zoberiem zrejme to najužšie miesto, tam to predelím a vyrvorím tak niekde 2 nové vrcholy (alebo bunky) A opäť prepočítam všetky vrcholi alebo len tie ktoré sú zapojené do takejto zmeny

DÁTOVÁ ŠTRUKTÚRA
Tak v tomto prípade mi neostáva nič iné, len si nájsť nejskú knižnicu na prácu s DCEL štruktúrov. Pomocouj tejto štruktúry si vieme reprezentovať taký graf, akým je voronoi.
Myslím, že tu toho moc nenarobím teraz asi. dátová štruktúra je daná a basta.


THEORY
teória za mapovaním pravidla z normálneho cellulárneho automatu na irregulárny a ako sa menia pravidlá a ako sa definujú outer totalistic a iné tieto názvy. Tam to bolo všetko pekne definované. Aj tie pravidielka. Aj to ako sa to počítalo a takéto veci. No parádička. Navyše mám jeho kompletnú prácu. Takže to je ešte fajnejšie.

Možno by som sa mohol s nejakými otázkami obrátiť na pána Baetsa. Keby som niečomu nerozumel z jeho práce.
'''
