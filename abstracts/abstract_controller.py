from abc import ABC, abstractmethod


class AbstractController(ABC):
    @abstractmethod
    def start_count(self) -> None:
        pass

    @abstractmethod
    def stop_count(self) -> None:
        pass

    @abstractmethod
    def evento_de_fechamento(self) -> None:
        pass
