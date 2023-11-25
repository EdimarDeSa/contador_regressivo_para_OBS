from abc import ABC, abstractmethod


class AbstractController(ABC):
    @abstractmethod
    def start_count(self) -> None:
        pass

    @abstractmethod
    def stop_count(self) -> None:
        pass

    @abstractmethod
    def validate_hour_input_cmd(self, tempo: str) -> bool:
        pass

    @abstractmethod
    def validate_minute_second_input_cmd(self, tempo: str) -> bool:
        pass

    @abstractmethod
    def evento_de_fechamento(self) -> None:
        pass
