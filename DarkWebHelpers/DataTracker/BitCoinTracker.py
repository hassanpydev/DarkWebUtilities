from blockcypher import get_address_overview, is_valid_address
from DarkWebHelpers.app import AppConfigurations
config = AppConfigurations()

class Validate:
    def __init__(self, address):
        self.address = address

    def V(self):
        if is_valid_address(self.address):
            return True
        else:
            return False


class Track:
    def __init__(self, address):
        self.address = address
        self.result = None
    def __address_overview(self):
        try:
            results = get_address_overview(self.address)
            return results
        except BaseException as e:
            config.debug(e)

    def track(self):
        validator = Validate(self.address)
        if validator.V():
            results = self.__address_overview()
            self.result = results
            config.debug(results)
            return True
