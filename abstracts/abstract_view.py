from abc import ABC, abstractmethod
from typing import Literal

from constants import *


class AbstractView(ABC):
    @abstractmethod
    def start(self, controller) -> None:
        pass

    @abstractmethod
    def main_loop(self) -> None:
        pass

    @abstractmethod
    def alert(self, title: str, message: str) -> None:
        pass

    @abstractmethod
    def set_display(self, text: str) -> None:
        pass

    @abstractmethod
    def askyesno(self, title: str, message: str) -> bool:
        pass

    @abstractmethod
    def set_time_fields(self, state: Literal['readonly', 'normal']) -> None:
        pass

    @abstractmethod
    def get_start_hour(self) -> str:
        pass

    @abstractmethod
    def get_start_minute(self) -> str:
        pass

    @abstractmethod
    def get_end_hour(self) -> str:
        pass

    @abstractmethod
    def get_end_minute(self) -> str:
        pass

    @abstractmethod
    def setup_start_cancel_button(self, button: Buttons) -> None:
        pass

    @abstractmethod
    def show_file_path(self, file_path: str) -> None:
        pass

    @abstractmethod
    def get_timer_name(self) -> str:
        pass
