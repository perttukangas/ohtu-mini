from enum import Enum

# https://en.wikibooks.org/wiki/LaTeX/Bibliography_Management
# http://newton.ex.ac.uk/tex/pack/bibtex/btxdoc/node6.html
# http://newton.ex.ac.uk/tex/pack/bibtex/btxdoc/node7.html

# https://www.bibtex.com/format/

class ReferenceType(Enum):

    ARTICLE = (1,
    "Artikkeli",
    ("author", "journal", "title", "year"), 
    ("month", "note", "number", "pages", "volume"))
    BOOK = (2, 
    "Kirja",
    (("author", "editor"), "title", "publisher", "year"), 
    (("volume", "number"), "series", "address", "edition", "month", "note")) 

    def get_db_id(self):
        return self.value[0]

    def get_name(self):
        return self.value[1]

    def get_required(self):
        return self.value[2]
    
    def get_optional(self):
        return self.value[3]

    def get_required_for_add(self):
        return self._get_data(self.value[2])

    def get_optional_for_add(self):
        return self._get_data(self.value[3])
    
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


references_for_index = []
def get_references_for_index():
    if references_for_index:
        return references_for_index
    
    for data in ReferenceType:
        references_for_index.append((data.name, data.get_name()))
    
    return references_for_index

cache = {}
def get_form_message(type):
    if cache:
        return cache.get(type, f"Lomakeviesti puuttuu: {type}")
    

    cache["address"] = "Osoite, esimerkiksi 'Helsinki, Suomi'"
    # ...

    return cache.get(type, f"Lomakeviesti puuttuu: {type}")

