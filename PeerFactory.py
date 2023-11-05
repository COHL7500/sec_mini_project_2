from abc import abstractmethod, ABC

from config import Config
from patient import Patient


class PeerFactory(ABC):
    @abstractmethod
    def create_peer(self, config: Config, port: int, id: int):
        pass

class PatientFactory(PeerFactory):
    def create_peer(self, config, port, id):
        return Patient(config, port, id)
