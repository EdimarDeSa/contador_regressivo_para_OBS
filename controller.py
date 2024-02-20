from dataclasses import dataclass
from datetime import date, datetime, time
from tempfile import TemporaryFile
from pathlib import Path
from threading import Event, Thread
from time import sleep
from typing import Optional

from abstracts.abstract_controller import AbstractController
from abstracts.abstract_view import AbstractView
from constants import *


@dataclass
class TimerParameters:
    now: Optional[datetime] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    date: Optional[date] = None

    def __post_init__(self) -> None:
        self.now = datetime.now()
        self.date = self.now.date()


class Controller(AbstractController):
    def __init__(self, view: AbstractView):
        self.view = view

        self.timer_params = TimerParameters()
        self.base_file: Optional[TemporaryFile] = None

        self.counting = Event()

    def start(self) -> None:
        self.view.start(self)

        Thread(target=self.start_loop_counter, daemon=True).start()

    def loop(self) -> None:
        self.view.main_loop()

    def start_count(self) -> None:
        start_timer = time(self.view.get_start_hour, self.view.get_start_minute)
        self.timer_params.start_time = self._convert_time(start_timer)

        end_timer = time(self.view.get_end_hour, self.view.get_end_minute)
        self.timer_params.end_time = self._convert_time(end_timer)

        self.timer_params.now = datetime.now()
        if self.timer_params.now > self.timer_params.end_time:
            self.view.alert(
                'O horário já passou...',
                'Não é possível iniciar um timer com o tempo de término menor que o horário atual!',
            )
            return

        self.timer_params.counting = True

        self.view.set_time_fields(READONLY)

        self._escreve_arquivo_de_contagem()
        self.view.show_file_path(str(self._temp_file))

        self.view.setup_start_cancel_button(Buttons.STOP)

        self.counting.set()

    def _convert_time(self, time_: time) -> datetime:
        return datetime.combine(self.timer_params.date, time_)

    def start_loop_counter(self) -> None:
        while True:
            self.counting.wait()

            self.timer_params.now = datetime.now()

            counting = 'Tempo encerrado!'
            if self.timer_params.now < self.timer_params.start_time:
                remaining_time = self._calculate_remaining_time(
                    self.timer_params.start_time
                )
                counting = f'Faltam {remaining_time}'

            elif self.timer_params.now < self.timer_params.end_time:
                counting = self._calculate_remaining_time(self.timer_params.end_time)
                self._escreve_arquivo_de_contagem(counting)

            else:
                self._escreve_arquivo_de_contagem(TEMPO_ZERADO)
                self.view.setup_start_cancel_button(Buttons.START)
                self.stop_count()

            self.view.set_display(counting)
            sleep(0.5)

    def _calculate_remaining_time(self, tempo_limite: datetime) -> str:
        tempo_restante = tempo_limite - self.timer_params.now
        formmater = formatters.get(self.view.format.get())
        return formmater.format_time(tempo_restante.seconds)

    def stop_count(self) -> None:
        self.counting.clear()
        self.view.set_time_fields(NORMAL)
        self.view.setup_start_cancel_button(Buttons.START)

    @staticmethod
    def _valida_entrada(numero: str, tempo_maximo: int) -> bool:
        return numero == '' or numero.isdigit() and int(numero) <= tempo_maximo

    def _escreve_arquivo_de_contagem(self, text=TEMPO_ZERADO) -> None:
        with open(self._temp_file, 'w') as f:
            f.write(text)

    @property
    def _temp_file(self) -> Path:
        if self.base_file is None:
            filename = self.view.get_timer_name()
            self.base_file = Path(__file__).resolve().parent / f'{filename}.txt'
        return self.base_file

    def evento_de_fechamento(self) -> None:
        if self.counting.is_set():
            r = self.view.askyesno(
                'Contagem em andamento',
                'Tem certeza que deseja cancelar a contagem atual?',
            )
            if not r:
                return

        exit(0)
