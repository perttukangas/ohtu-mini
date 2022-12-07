from ..utils.reference_type import ReferenceType

class Validator:
    def __init__(self, data):
        self.data = data
        self.error = None
        self.columns = []
        self.values = []
    
    def run_all_validators(self):
        self.validate_reference_name()
        if self.error:
            return self.error
        
        self.validate_reference_id()
        if self.error:
            return self.error
        
        self.validate_input_required()
        if self.error:
            return self.error
        
        self.validate_input_optional()
        if self.error:
            return self.error
        
        return None
    
    def validate_reference_name(self):
        try:
            ReferenceType[self.data.get("reference_name")]
        except KeyError:
            self.error = "404"

    def validate_reference_id(self):
        if len(self.data.get("reference_id", "")) < 1:
            self.error = "Vaadittu kenttä täyttämättä: reference_id"
    
    def validate_input_required(self):
        self._validate_input(True, ReferenceType[self.data.get("reference_name")])
    
    def validate_input_optional(self):
        self._validate_input(False, ReferenceType[self.data.get("reference_name")])

    def _validate_input(self, required, ref_type):
        types = ref_type.get_required() if required else ref_type.get_optional()
        for cur_type in types:

            bib_entry = self.get_bib_entry(cur_type)
            if self.error:
                # Jos kummatkin "tai" kentistä on täytetty 
                break

            bib_type, bib_data = bib_entry

            if len(bib_data) < 1:
                if required:
                    # Vaatitu kenttä on siis täyttämättä -> error
                    self.error = f"Vaadittu kenttä täyttämättä: {cur_type}"
                    break

                # Jos valinnainen kenttä niin älä lähetä tyhjää merkkijonoa tietokantaan
                continue
            
            self.validate_one_field(bib_type, bib_data)
            if self.error:
                # Data annetulle bib tyypille ei ollut valid
                break

            # Lisää "validit" tyypit ja arvot listoihin samassa järjestyksessä
            self.columns.append(bib_type)
            self.values.append(bib_data)

    def get_bib_entry(self, cur_type):
        if isinstance(cur_type, tuple):
            first = self.data.get(cur_type[0], "") 
            second = self.data.get(cur_type[1], "") 
            if len(first) > 0 and len(second) > 0:
                # Koska joillakin bib tyypeillä on mahdollista x tai y, niin tässä tarkastetaan
                # ettei kumpikin niistä ole kentistä ole täytettynä
                self.error = f"Vain toinen kentistä {cur_type[0]} ja {cur_type[1]} voi sisältää tietoa"
                return None

            bib_type = cur_type[0] if len(first) > 0 else cur_type[1]
            bib_entry = first if len(first) > 0 else second
        else:
            # Eli kenttä on "yksittäinen", jolloin ei tarvetta tarkastaa ovatko
            # kummatkin "tai" kentistä täytettynä
            bib_type = cur_type
            bib_entry = self.data.get(cur_type, "") 
        return (bib_type, bib_entry)

    def validate_one_field(self, bib_type, bib_data):
        self.is_less_than(bib_type, bib_data, 120)
        self.is_numeric(bib_type, bib_data)

    def is_less_than(self, bib_type, bib_data, length):
        if len(bib_data) > length:
            self.error = f"{bib_type} ei voi olla pidempi kuin {length} kirjainta"
    
    def is_numeric(self, bib_type, bib_data):
        if bib_type == "year" and not bib_data.isnumeric():
            self.error = f"Kentän '{bib_type}' arvon tulee olla kokonaisluku"
