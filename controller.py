from dataclasses import dataclass
from datetime import date, datetime, time
from tempfile import TemporaryFile
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
        start_hour = self.view.get_start_hour()
        start_minute = self.view.get_start_minute()
        start_timer = time(int(start_hour), int(start_minute))
        self.timer_params.start_time = self._convert_time(start_timer)

        end_hour = self.view.get_end_hour()
        end_minute = self.view.get_end_minute()
        end_timer = time(int(end_hour), int(end_minute))
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
        self.view.show_file_path(self._get_file_path.name)

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
        if tempo_restante.total_seconds() <= 0:
            return TEMPO_ZERADO

        horas_totais, total_segunds = divmod(tempo_restante.seconds, 3600)
        minutos_totais, segundos = divmod(total_segunds, 60)
        return (
            f'{horas_totais:02}:{minutos_totais:02}:{segundos:02}'
            if horas_totais
            else f'{minutos_totais:02}:{segundos:02}'
        )

    def stop_count(self) -> None:
        self.counting.clear()
        self.view.set_time_fields(NORMAL)

        self.view.setup_start_cancel_button(Buttons.START)

    def validate_hour_input_cmd(self, tempo: str) -> bool:
        return self._valida_entrada(tempo, 23)

    def validate_minute_second_input_cmd(self, tempo: str) -> bool:
        return self._valida_entrada(tempo, 59)

    @staticmethod
    def _valida_entrada(numero: str, tempo_maximo: int) -> bool:
        return numero == '' or numero.isdigit() and int(numero) <= tempo_maximo

    def _escreve_arquivo_de_contagem(self, text=TEMPO_ZERADO) -> None:
        filename = self.view.get_timer_name()
        # TODO: Não está escrevendo conforme o esperado.
        with open(filename, mode='w', encoding='utf-8-sig') as timer_file:
            timer_file.write(text)
        self._get_file_path.write(f'{text}')

    @property
    def _get_file_path(self) -> TemporaryFile:
        if self.base_file is None:
            filename = self.view.get_timer_name()
            self.base_file = TemporaryFile(
                dir='./', mode='w', prefix=filename, suffix='.txt', delete=True
            )
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
