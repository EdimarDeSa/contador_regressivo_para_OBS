import tkinter
from tkinter import messagebox
from typing import Literal

from ttkbootstrap import Button, Entry, Label, Spinbox, StringVar, Toplevel, Window

from abstracts.abstract_controller import AbstractController
from abstracts.abstract_view import AbstractView
from constants import *


class View(AbstractView):
    def start(self, controller: AbstractController) -> None:
        self.controller = controller

        self._setup_root()
        self._setup_variables()
        self._setup_ui()

    def main_loop(self) -> None:
        self._root.mainloop()

    def _setup_variables(self) -> None:
        self.validate_hour_input = self._root.register(
            self.controller.validate_hour_input_cmd
        )
        self.validate_minute_second_input = self._root.register(
            self.controller.validate_minute_second_input_cmd
        )

        self.fields = list()
        self._display = StringVar(value=TEMPO_ZERADO)

        Buttons.START.value['command'] = self.controller.start_count
        Buttons.STOP.value['command'] = self.controller.stop_count

    def _setup_root(self) -> None:
        self._root = Window(
            iconphoto=IMG_ICON,
            themename=TEMA,
            size=(600, 300),
            title=WINDOW_TITLE,
            resizable=(False, False),
        )

        self._root.wm_protocol('WM_DELETE_WINDOW', self.controller.evento_de_fechamento)

    def _setup_ui(self):
        self._create_time_form(INIT, 0.05)
        self._create_time_form(ENDING, 0.55)
        self._create_file_name_entry()
        self.inicia_display()
        self.inicia_botoes()

    def _create_time_form(self, field_name: str, relx: float) -> None:
        label_text = f'Horário de {field_name}'
        Label(self._root, text=label_text).place(relx=relx, rely=0.02)

        Label(self._root, text=HOUR).place(relx=relx, rely=0.1)
        hour_spinbox = Spinbox(
            self._root,
            name=f'hour_{field_name}',
            from_=0,
            to=24,
            validate=KEY,
            validatecommand=(self.validate_hour_input, '%P'),
        )
        hour_spinbox.place(relx=relx, rely=0.2, width=75)
        hour_spinbox.insert(
            0,
            DefaultStart.HOUR if field_name == INIT else DefaultEnd.HOUR,
        )
        self.fields.append(hour_spinbox)

        Label(self._root, text=':', font='times 25').place(
            relx=relx + 0.135, rely=0.155
        )

        Label(self._root, text=MINUT).place(relx=relx + 0.175, rely=0.1)
        minute_spinbox = Spinbox(
            self._root,
            name=f'minut_{field_name}',
            from_=0,
            to=60,
            validate=KEY,
            validatecommand=(self.validate_minute_second_input, '%P'),
        )
        minute_spinbox.place(relx=relx + 0.175, rely=0.2, width=75)
        minute_spinbox.insert(
            0,
            DefaultStart.MINUT if field_name == INIT else DefaultEnd.MINUT,
        )
        self.fields.append(minute_spinbox)

    def _create_file_name_entry(self) -> None:
        Label(self._root, text='Nome do timer:', font='-size 12').place(
            relx=0.05, rely=0.405
        )

        timer_name = Entry(self._root, name='timer_name')
        timer_name.place(relx=0.33, rely=0.4, relwidth=0.62)
        timer_name.insert(0, DEFAULT_NAME)
        self.fields.append(timer_name)

    def inicia_display(self):
        Label(
            self._root,
            textvariable=self._display,
            anchor=CENTER,
            font='-size 32',
        ).place(relx=0.05, rely=0.55, relwidth=0.9)

    def inicia_botoes(self) -> None:
        self._button = Button(self._root)
        self._button.place(relx=0.15, rely=0.8, relwidth=0.7)

        self.setup_start_cancel_button(Buttons.START)

    def setup_start_cancel_button(self, button: Buttons) -> None:
        self._button.config(**button.value)

    def set_time_fields(self, state: Literal['readonly', 'normal']) -> None:
        for field in self.fields:
            field.configure(state=state)

    def set_display(self, text: str) -> None:
        self._display.set(text)

    def askyesno(self, title: str, message: str) -> bool:
        return messagebox.askyesno(title, message)

    def alert(self, title: str, message: str) -> None:
        messagebox.showerror(title, message)

    def get_start_hour(self) -> str:
        return self._root.children.get(Start.HOUR).get()

    def get_start_minute(self) -> str:
        return self._root.children.get(Start.MINUT).get()

    def get_end_hour(self) -> str:
        return self._root.children.get(End.HOUR).get()

    def get_end_minute(self) -> str:
        return self._root.children.get(End.MINUT).get()

    def show_file_path(self, file_path: str) -> None:
        top = Toplevel(resizable=(False, False), topmost=True, name='toplevel')
        top.title(WINDOW_TITLE)
        top.config(takefocus=True)

        txt = Entry(top, width=100)
        txt.insert(0, file_path)
        txt.config(state=READONLY)
        txt.pack(padx=5, pady=5)
        txt.bind('<Button-1>', self.copia_texto)

    def copia_texto(self, event: tkinter.Event) -> None:
        widget = event.widget
        txt = widget.get()
        self._root.clipboard_clear()
        self._root.clipboard_append(txt)
        label = Label(widget.master, text='Texto copiado!')
        label.pack()
        widget.after(1000, label.pack_forget)

    def get_timer_name(self) -> str:
        return self._root.children.get('timer_name').get()
