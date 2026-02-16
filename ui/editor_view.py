import tkinter as tk
from tkinter import ttk
from ui.status_bar import StatusBar
from ui.components.closable_notebook import ClosableNotebook
from ui.highlighter import Highlighter


class EditorView:

    def __init__(self, root):
        self.root = root

        # cria notebook
        self.notebook = ClosableNotebook(root, on_tab_close=self._on_tab_close)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.status = StatusBar(root)

        self.tabs = {}

        # cria a primeira aba
        text = self.create_new_tab()
        Highlighter(text)

    # =================================
    def create_new_tab(self, title="Sem título"):

        frame = tk.Frame(self.notebook)
        frame.pack(fill=tk.BOTH, expand=True)

        scroll = tk.Scrollbar(frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        text = tk.Text(
            frame,
            undo=True,
            yscrollcommand=scroll.set,
            bg="#1e1e1e",
            fg="white",
            insertbackground="white",
            font=("Consolas", 12),
            padx=10,
            pady=10
        )
        text.pack(fill=tk.BOTH, expand=True)

        scroll.config(command=text.yview)

        self.notebook.add(frame, text=title)
        self.notebook.select(frame)

        tab_id = self.notebook.select()
        self.tabs[tab_id] = text

        return text

    # =================================
    def _on_tab_close(self, tab_id):
        """Remove do dict quando fechar"""
        if tab_id in self.tabs:
            del self.tabs[tab_id]

        # se fechar tudo → cria nova aba
        if not self.tabs:
            self.create_new_tab()

    # =================================
    def get_current_text(self):
        tab_id = self.notebook.select()
        return self.tabs.get(tab_id)

    def set_tab_title(self, title):
        tab_id = self.notebook.select()
        self.notebook.tab(tab_id, text=title)

    # =================================
    def create_menu(self, controller):
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)

        file_menu.add_command(label="New", command=controller.new)
        file_menu.add_command(label="Open", command=controller.open)
        file_menu.add_command(label="Save", command=controller.save)
        file_menu.add_command(label="Save As", command=controller.save_as)

        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=controller.on_close)

        menu_bar.add_cascade(label="File", menu=file_menu)

        self.root.config(menu=menu_bar)