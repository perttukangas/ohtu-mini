class Validator:
    def __init__(self):
        self.errors = []
        self._max_string_length = 100

    def add_error(self, error: str):
        self.errors.append(str(error))

    def has_errors(self):
        return len(self.errors) != 0

    def __str__(self):
        return self.errors[0].capitalize()

    def has_length_less_than(self, form_type, content):
        if len(content) > self._max_string_length:
            self.add_error(
                f"{form_type} ei voi olla pidempi kuin {self._max_string_length} kirjainta"
                )
    
    def year_input_correctly(self, form_type, content):
        if form_type == "year":
            if not content.isnumeric():
                self.add_error(f"Kentän '{form_type}' arvon tulee olla kokonaisluku")


def check_for_errors(validator: Validator, form_type: str, content: str):
    validator.has_length_less_than(form_type, content)
    validator.year_input_correctly(form_type, content)
    if validator.has_errors():
        return validator
    return None
