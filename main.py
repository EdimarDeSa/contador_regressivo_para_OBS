import pathlib
import sys
from tkinter.messagebox import askyesno, showerror

from ttkbootstrap import *

from variaveis import *


def valida_entrada(numero, tempo_maximo) -> bool:
    return numero == "" or numero.isdigit() and int(numero) <= tempo_maximo


class Temporizador:
    def __init__(self, master: Window):
        self.root = master

        self.configura_janela()
        self.configura_variaveis()
        self.configura_interface_do_usuario()

        self.atualiza_horario_atual()

    def configura_janela(self):
        self.root.wm_protocol('WM_DELETE_WINDOW', self.evento_de_fechamento)

    def configura_variaveis(self):
        self.validate_hour_input_register = self.root.register(self.validate_hour_input_cmd)
        self.validate_minute_second_input_register = self.root.register(self.validate_minute_second_input_cmd)

        self.contando = BooleanVar(value=False)
        self.afterid = StringVar()

        self.nome_do_arquivo = NOME_ARQUIVO_PADRAO
        self.BASE = pathlib.Path(__file__).resolve().parent.parent

    def configura_interface_do_usuario(self):
        self.form_horario(INICIO, 0.05)
        self.form_horario(ENCERRAMENTO, 0.55)
        self.form_nome_arquivo(0.05)
        self.inicia_display()
        self.inicia_botoes()

    def form_horario(self, nome_da_label, relx):
        Label(self.root, text=f'Horário de {nome_da_label}').place(relx=relx, rely=0.02)

        Label(self.root, text=HORA).place(relx=relx, rely=0.1)
        hour_spinbox = Spinbox(self.root, name=f'hora_{nome_da_label}', from_=0, to=24, validate=KEY,
                               validatecommand=(self.validate_hour_input_register, "%P"))
        hour_spinbox.place(relx=relx, rely=0.2, width=75)
        hour_spinbox.insert(0, HORA_INICIAL_PADRAO if nome_da_label == INICIO else HORA_FINAL_PADRAO)

        Label(self.root, text=':', font='times 25').place(relx=relx + 0.135, rely=0.155)

        Label(self.root, text=MINUTO).place(relx=relx + 0.175, rely=0.1)
        minute_spinbox = Spinbox(self.root, name=f'minuto_{nome_da_label}', from_=0, to=60, validate=KEY,
                                 validatecommand=(self.validate_minute_second_input_register, "%P"))
        minute_spinbox.place(relx=relx + 0.175, rely=0.2, width=75)
        minute_spinbox.insert(0, MINUTO_INICAL_PADRAO if nome_da_label == INICIO else MINUTO_FINAL_PADRAO)

    def form_nome_arquivo(self, relx):
        Label(self.root, text='Nome do arquivo:', font='-size 12').place(relx=relx, rely=0.405)

        self.entry_nome_do_arquivo = Entry(self.root)
        self.entry_nome_do_arquivo.place(relx=relx + 0.28, rely=0.4, relwidth=0.62)
        self.entry_nome_do_arquivo.insert(0, self.nome_do_arquivo)

    def inicia_display(self):
        self.display = Label(self.root, anchor=CENTER, font='-size 32')
        self.display.place(relx=0.05, rely=0.55, relwidth=.9)
        self.set_display(TEMPO_ZERADO)

    def inicia_botoes(self):
        Button(self.root, name=START, text=START.upper(),
               style=SUCCESS,
               command=self.inicia_contagem)
        Button(self.root, name=CANCELAR, text=CANCELAR.upper(),
               style=DANGER,
               command=self.encerrar_contagem)

        self.posiciona_botao_start_cancelar()

    def validate_hour_input_cmd(self, tempo):
        return valida_entrada(tempo, 24)

    def validate_minute_second_input_cmd(self, tempo):
        return valida_entrada(tempo, 60)

    def encerrar_contagem(self, texto='Cancelado!'):
        self.root.after_cancel(self.afterid.get())
        self.display.config(text=texto)
        self.escreve_arquivo_de_contagem(TEMPO_ZERADO)
        self.posiciona_botao_start_cancelar()
        self.entry_nome_do_arquivo.config(state=NORMAL)
        self.contando.set(False)
        self.root.children.get('toplevel').destroy()

    def set_display(self, text):
        self.display.config(text=text)

    def posiciona_botao_start_cancelar(self, botao=START):
        var_tipo_bt = botao == START
        estado = NORMAL if var_tipo_bt else READONLY
        self.root.children.get(START if var_tipo_bt else CANCELAR).place(relx=0.15, rely=0.8, relwidth=0.7)
        self.root.children.get(CANCELAR if var_tipo_bt else START).place_forget()

        self.root.children.get(HORA_INICIO).configure(state=estado)
        self.root.children.get(MINUTO_INICIO).configure(state=estado)
        self.root.children.get(HORA_ENCERRAMENTO).configure(state=estado)
        self.root.children.get(MINUTO_ENCERRAMENTO).configure(state=estado)

    def escreve_arquivo_de_contagem(self, text=''):
        with open(self.get_local_do_arquivo, W) as arquivo:
            arquivo.write(text)

    def tempo_restante(self, tempo_limite: datetime) -> str:
        tempo_restante = tempo_limite - self.horario_atual
        horas_totais, segundos = divmod(tempo_restante.seconds, 3600)
        minutos_totais, segundos = divmod(segundos, 60)
        return f'{horas_totais:02}:{minutos_totais:02}:{segundos:02}' if horas_totais else f'{minutos_totais:02}:{segundos:02}'

    def inicia_contagem(self):
        if self.horario_atual > self.horario_fim_timer:
            showerror(
                'O horário já passou...',
                'Não é possível iniciar um timer com o tempo de término menor que o horário atual!'
            )
            return

        self.contando.set(True)
        self.entry_nome_do_arquivo.config(state=READONLY)
        self.escreve_arquivo_de_contagem(TEMPO_ZERADO)
        self.informa_local_do_arquivo()
        self.conta_tempo()

    def conta_tempo(self):
        self.posiciona_botao_start_cancelar(CANCELAR)
        self.atualiza_horario_atual()

        if self.horario_atual < self.horario_inicio_timer:
            self.set_display(f'Faltam {self.tempo_restante(self.horario_inicio_timer)}')

        elif self.horario_atual < self.horario_fim_timer:
            minutos_restantes_str = self.tempo_restante(self.horario_fim_timer)
            self.set_display(minutos_restantes_str)
            self.escreve_arquivo_de_contagem(minutos_restantes_str)

        else:
            self.set_display(text='Timer finalizado!')
            self.escreve_arquivo_de_contagem(TEMPO_ZERADO)
            self.posiciona_botao_start_cancelar()
            self.encerrar_contagem('Tempo encerrado')

        self.afterid.set(self.root.after(500, self.conta_tempo))

    def atualiza_horario_atual(self):
        horario_atual_str = datetime.now().strftime(FORMATO_HORA_MINUTO_SEGUNDO)
        self.horario_atual = datetime.strptime(horario_atual_str, FORMATO_HORA_MINUTO_SEGUNDO)

    def evento_de_fechamento(self):
        if self.contando.get():
            r = askyesno(
                'Contagem em andamento',
                'Tem certeza que deseja cancelar a contagem atual?'
            )
            if not r:
                return

        sys.exit()

    def informa_local_do_arquivo(self):
        top = Toplevel(resizable=(False, False), topmost=True, name='toplevel')
        top.title(TITULO_JANELA)
        top.config(takefocus=True)

        txt = Entry(top, width=100)
        txt.insert(0, str(self.get_local_do_arquivo.absolute()))
        txt.config(state=READONLY)
        txt.pack(padx=5, pady=5)
        txt.bind('<Button-1>', self.copia_texto)

    def copia_texto(self, event):
        widget = event.widget
        txt = widget.get()
        self.root.clipboard_clear()
        self.root.clipboard_append(txt)
        label = Label(widget.master, text='Texto copiado!')
        label.pack()
        widget.after(1000, label.pack_forget)

    @property
    def get_nome_do_arquivo(self) -> str:
        return f'{self.entry_nome_do_arquivo.get()}.txt'

    @property
    def get_local_do_arquivo(self):
        local = self.BASE / self.get_nome_do_arquivo
        return local

    @property
    def horario_inicio_str(self) -> str:
        return f'{self.root.children.get(HORA_INICIO).get()}:{self.root.children.get(HORA_ENCERRAMENTO).get()}'

    @property
    def horario_inicio_timer(self) -> datetime:
        return datetime.strptime(self.horario_inicio_str, FORMATO_HORA_MINUTO)

    @property
    def horario_fim_str(self) -> str:
        return f'{self.root.children.get(HORA_ENCERRAMENTO).get()}:{self.root.children.get(MINUTO_ENCERRAMENTO).get()}'

    @property
    def horario_fim_timer(self) -> datetime:
        return datetime.strptime(self.horario_fim_str, FORMATO_HORA_MINUTO)


if __name__ == '__main__':
    root = Window(iconphoto=LOCAL_IMAGEM_ICONE, themename=TEMA, size=(600, 300), title=TITULO_JANELA, resizable=(False, False))
    Temporizador(root)
    root.mainloop()
