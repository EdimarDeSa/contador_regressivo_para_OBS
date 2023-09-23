import datetime

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def valida_entrada_de_hora(numero):
    if numero == "" or numero.isdigit() and int(numero) <= 24:
        return True
    else:
        return False


def valida_entrada_de_minuto_ou_segundo(numero):
    if numero == "" or numero.isdigit() and int(numero) <= 60:
        return True
    else:
        return False


class Temporizador(object):
    def __init__(self, master: ttk.Window):
        self.root = master

        master.geometry('600x300')
        master.title('Contador regressivo')

        self.validate_hour_input_cmd = master.register(valida_entrada_de_hora)
        self.validate_minute_second_input_cmd = master.register(valida_entrada_de_minuto_ou_segundo)

        self.contando = ttk.BooleanVar(value=False)
        self.afterid = ttk.StringVar()

        self.atualiza_horario_atual()

        self.form_horario_inicio(master)
        self.form_horario_fim(master)
        self.inicia_display(master)
        self.inicia_botoes(master)

    def form_horario_inicio(self, master):
        ttk.Label(master, text='Horário de início').place(relx=0.05, rely=0.02)

        ttk.Label(master, text='Hora').place(relx=0.05, rely=0.1)
        self._hora_inicio = ttk.Spinbox(master, from_=0, to=24, validate='key',
                                        validatecommand=(self.validate_hour_input_cmd, "%P"))
        self._hora_inicio.place(relx=0.05, rely=0.2, width=75)
        self._hora_inicio.insert(0, '19')

        ttk.Label(master, text=':', font='times 25').place(relx=0.185, rely=0.155)

        ttk.Label(master, text='Minuto').place(relx=0.22, rely=0.1)
        self._minuto_inicio = ttk.Spinbox(master, from_=0, to=60, validate='key',
                                          validatecommand=(self.validate_minute_second_input_cmd, "%P"))
        self._minuto_inicio.place(relx=0.22, rely=0.2, width=75)
        self._minuto_inicio.insert(0, '00')

    def form_horario_fim(self, master):
        ttk.Label(master, text='Horário de encerramento').place(relx=0.55, rely=0.02)

        ttk.Label(master, text='Hora').place(relx=0.55, rely=0.1)
        self._hora_fim = ttk.Spinbox(master, from_=0, to=24, validate='key',
                                     validatecommand=(self.validate_hour_input_cmd, "%P"))
        self._hora_fim.place(relx=0.55, rely=0.2, width=75)
        self._hora_fim.insert(0, '19')

        ttk.Label(master, text=':', font='times 25').place(relx=0.685, rely=0.155)

        ttk.Label(master, text='Minuto').place(relx=0.72, rely=0.1)
        self._minuto_fim = ttk.Spinbox(master, from_=0, to=60, validate='key',
                                       validatecommand=(self.validate_minute_second_input_cmd, "%P"))
        self._minuto_fim.place(relx=0.72, rely=0.2, width=75)
        self._minuto_fim.insert(0, '40')

    @property
    def horario_inicio_str(self):
        return f'{self._hora_inicio.get()}:{self._minuto_inicio.get()}'

    @property
    def horario_inicio_timer(self):
        return datetime.datetime.strptime(self.horario_inicio_str, '%H:%M')

    @property
    def horario_fim_str(self):
        return f'{self._hora_fim.get()}:{self._minuto_fim.get()}'

    @property
    def horario_fim_timer(self):
        return datetime.datetime.strptime(self.horario_fim_str, '%H:%M')

    def inicia_display(self, master: ttk.Window):
        self.display = ttk.Label(master, anchor=CENTER, font='-size 32')
        self.display.place(relx=0.05, rely=0.45, relwidth=.9)
        self.set_display('00:00:00')

    def set_display(self, text):
        self.display.config(text=text)

    def inicia_botoes(self, master):
        self.bt_start = ttk.Button(master, text='Start', style='success', command=self.conta_tempo)
        self.bt_stop = ttk.Button(master, text='Stop', style='danger',
                                  command=lambda txt='Cancelado!': self.encerrar_contagem(txt))

        self.place_bt_start()

    @staticmethod
    def escreve_arquivo_de_contagem(text=''):
        with open('contagem_regressiva.txt', 'w') as arquivo:
            arquivo.write(text)

    def tempo_restante(self, tempo_limite: datetime.datetime) -> str:
        minutos_restantes = int((tempo_limite - self.horario_atual).total_seconds())
        horas_totais = minutos_restantes // 3600
        minutos_totais = (minutos_restantes // 60) % 60
        segundos = minutos_restantes % 60

        if not horas_totais:
            return f'{minutos_totais:02}:{segundos:02}'

        return f'{horas_totais:02}:{minutos_totais:02}:{segundos:02}'

    def conta_tempo(self):
        self.place_bt_cancelar()

        self.atualiza_horario_atual()
        if self.horario_atual < self.horario_inicio_timer:

            self.set_display(f'Faltam {self.tempo_restante(self.horario_inicio_timer)}')
            self.escreve_arquivo_de_contagem('00:00:00')

        elif self.horario_atual < self.horario_fim_timer:
            minutos_restantes_str = self.tempo_restante(self.horario_fim_timer)
            self.set_display(minutos_restantes_str)
            self.escreve_arquivo_de_contagem(minutos_restantes_str)

        else:
            self.set_display(text='Timer finalizado!')
            self.escreve_arquivo_de_contagem('00:00')
            self.place_bt_start()
            self.encerrar_contagem('Tempo encerrado')

        self.afterid.set(self.root.after(500, self.conta_tempo))

    def atualiza_horario_atual(self):
        # Obtem o horário atual
        horario_atual_str = datetime.datetime.now().strftime('%H:%M:%S')
        self.horario_atual_list = horario_atual_str.split(':')
        self.horario_atual = datetime.datetime.strptime(horario_atual_str, '%H:%M:%S')

    def encerrar_contagem(self, texto: str):
        self.root.after_cancel(self.afterid.get())
        self.display.config(text=texto)
        self.escreve_arquivo_de_contagem('00:00')
        self.place_bt_start()

    def place_bt_start(self):
        self.bt_start.place(relx=0.35, rely=0.8, relwidth=0.3)
        self.bt_stop.place_forget()

        self._hora_inicio.configure(state='active')
        self._minuto_inicio.configure(state='active')

        self._hora_fim.configure(state='active')
        self._minuto_fim.configure(state='active')

    def place_bt_cancelar(self):
        self.bt_stop.place(relx=0.35, rely=0.8, relwidth=0.3)
        self.bt_start.place_forget()

        self._hora_inicio.configure(state='readonly')
        self._minuto_inicio.configure(state='readonly')

        self._hora_fim.configure(state='readonly')
        self._minuto_fim.configure(state='readonly')


if __name__ == '__main__':
    root = ttk.Window()
    Temporizador(root)
    root.mainloop()
