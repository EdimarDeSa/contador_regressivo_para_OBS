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
