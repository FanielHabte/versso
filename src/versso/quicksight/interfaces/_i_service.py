from abc import abstractmethod, ABC


class Service(ABC):
    """
    Interface that defines the structure of Analysis, Dashboard and Dataset Services
    """

    def __init__(self, payload, context, client):
        self.payload = payload
        self.context = context
        self.client = client

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def define(self):
        pass

    @abstractmethod
    def describe(self):
        pass

    @abstractmethod
    def update(self, definition: dict):
        pass

    @abstractmethod
    def clone(self):
        pass

    @abstractmethod
    def promote_to(self, target):
        pass

    @abstractmethod
    def _create_template(self):
        pass
