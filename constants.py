from abc import ABC, abstractmethod
from enum import Enum, StrEnum

from ttkbootstrap.constants import *


class Start(StrEnum):
    HOUR = 'hour_inicio'
    MINUT = 'minut_inicio'
    SECOND = 'second_inicio'


class End(StrEnum):
    HOUR = 'hour_encerramento'
    MINUT = 'minut_encerramento'
    SECOND = 'second_encerramento'


class DefaultStart(StrEnum):
    HOUR = '19'
    MINUT = '00'
    SECOND = '00'


class DefaultEnd(StrEnum):
    HOUR = '19'
    MINUT = '40'
    SECOND = '00'


class Buttons(Enum):
    START = {
        'text': 'Start',
        'bootstyle': SUCCESS,
    }

    STOP = {
        'text': 'Cancelar',
        'bootstyle': DANGER,
    }


class TimeFormatter(ABC):
    @staticmethod
    @abstractmethod
    def format_time(total_seconds: int) -> str:
        pass


class SecondsFormatter(TimeFormatter):
    @staticmethod
    def format_time(total_seconds: int) -> str:
        return f'{total_seconds}'


class MinutesSecondsFormatter(TimeFormatter):
    @staticmethod
    def format_time(total_seconds: int) -> str:
        total_minutes, seconds = divmod(total_seconds, 60)
        return f'{total_minutes}:{seconds:02}'


class HoursMinutesSecondsFormatter(TimeFormatter):
    @staticmethod
    def format_time(total_seconds: int) -> str:
        total_hours, remaining_seconds = divmod(total_seconds, 3600)
        total_minutes, seconds = divmod(remaining_seconds, 60)
        return f'{total_hours}:{total_minutes:02}:{seconds:02}'


# Utilização:
formatters = {
    'SS': SecondsFormatter,
    'MM:SS': MinutesSecondsFormatter,
    'HH:MM:SS': HoursMinutesSecondsFormatter
}

INIT = 'inicio'
ENDING = 'encerramento'

HOUR = 'Hora'
MINUT = 'Minuto'

TEMA = 'flatly'

TEMPO_ZERADO = '00:00'

WINDOW_TITLE = 'Contador regressivo'
DEFAULT_NAME = 'contador1'
KEY = 'key'

IMG_ICON = '../../Imagens/cronometro-de-areia.png'
