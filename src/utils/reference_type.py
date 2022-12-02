from enum import Enum

# https://en.wikibooks.org/wiki/LaTeX/Bibliography_Management
# http://newton.ex.ac.uk/tex/pack/bibtex/btxdoc/node6.html
# http://newton.ex.ac.uk/tex/pack/bibtex/btxdoc/node7.html

# https://www.bibtex.com/format/

class ReferenceType(Enum):

    ARTICLE = ("Artikkeli",
    ("author", "journal", "title", "year"), 
    ("month", "note", "number", "pages", "volume"))
    BOOK = ("Kirja",
    (("author", "editor"), "title", "publisher", "year"), 
    (("volume", "number"), "series", "address", "edition", "month", "note"))

    def get_name(self):
        return self.value[0]

    def get_required(self):
        return self.value[1]
    
    def get_optional(self):
        return self.value[2]

    def get_required_for_add(self):
        return self._get_data(self.value[1])

    def get_optional_for_add(self):
        return self._get_data(self.value[2])
    
    def _get_data(self, fromArray):
        array = []
        for row in fromArray:
            if type(row) is tuple:
                first = (row[0], get_form_message(row[0]))
                second = (row[1], get_form_message(row[1]))
                array.append((first, second))
            else:
                array.append((row, get_form_message(row)))
        return array

cache_references_for_index = []
def get_references_for_index():
    if cache_references_for_index:
        return cache_references_for_index
    
    for data in ReferenceType:
        cache_references_for_index.append((data.name, data.get_name()))
    
    return cache_references_for_index

cache = {}
def get_form_message(type):
    if cache:
        return cache.get(type, f"Lomakeviesti puuttuu: {type}")

    cache["address"] = "Osoite, esim. 'Helsinki, Suomi'"
    cache["author"] = "Kirjoittaja, esim. 'Ludwig van Beethoven'"
    cache["booktitle"] = "Kirjan nimi, esim. 'Sinuhe egyptiläinen'"
    cache["chapter"] = "Kirjan luku, esim. 4"
    cache["edition"] = "Painos, esim. 'Kolmas' tai '3.'"
    cache["editor"] = "Toimittaja, esim. 'Waltari, Mika"
    cache["howpublished"] = "Julkaisutapa, esim. Jaettu näytteenä kirjamessuilla"
    cache["institution"] = "Instituutio"
    cache["journal"] = "Lehti, esim. 'Tieteen kuvalehti"
    cache["month"] = "Kuukausi, esim. '2' tai 'marraskuu'"
    cache["note"] = "Huomautus, esim. 'Luettu 15.10.2019 osoitteessa xx'"
    cache["number"] = "Lehden numero, esim. '5'"
    cache["organization"] = "Organisaatio, esim. 'British Society for Immunology'"
    cache["pages"] = "Sivunumero tai -- väli, esim. '75' tai '40--50'"
    cache["publisher"] = "Kustantaja, esim. 'Otava'"
    cache["school"] = "Oppilaitos, esim. 'HY' tai 'Helsingin yliopisto'"
    cache["series"] = "Kirjallisuussarja, esim. 'LNCS'"
    # HUOM: 'title'-kentässä isot kirjaimet tulee laittaa {} sisälle, esim {S}uomi
    # Muuten BibTex muuttaa ne pikkukirjaimiksi
    cache["title"] = "Otsikko"
    cache["type"] = "Tarkempia tietoja työstä. esim. 'kandidaatin tutkielma'"
    cache["volume"] = "Lehden niteen numero, esim. '3'"
    cache["year"] = "Julkaisuvuosi, esim. '2008'"

    return cache.get(type, f"Lomakeviesti puuttuu: {type}")
