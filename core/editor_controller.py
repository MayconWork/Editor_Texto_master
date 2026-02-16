import os
from tkinter import filedialog, messagebox
from core.file_service import FileService
from utils.constants import FILE_TYPES
from core.logger import logger
from ui.search_dialog import SearchDialog

def open(self):
    logger.info("FUNCAO OPEN CHAMADA")


class EditorController:

    def __init__(self, root, view):
        self.root = root
        self.view = view

        self.files = {}  # tab_id → path
        self.modified = {}

        self.view.create_menu(self)
        self.bind_events()

    # =====================
    # EVENTS
    # =====================
    def bind_events(self):
        self.root.bind("<Control-s>", lambda e: self.save())
        self.root.bind("<Control-o>", lambda e: self.open())
        self.root.bind("<Control-n>", lambda e: self.new())
        self.root.bind("<Control-f>", self._on_ctrl_f)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.view.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def get_current_text(self):
        return self.view.get_current_text()

    def get_current_tab(self):
        return self.view.notebook.select()

    # =====================
    # NEW TAB
    # =====================
    def new(self):
        text = self.view.create_new_tab()
        tab = self.get_current_tab()

        self.files[tab] = None
        self.modified[tab] = False

        text.bind("<KeyRelease>", self.update_status)
        text.bind("<<Modified>>", self.on_modified)

    # =====================
    # OPEN
    # =====================
    def open(self):
        path = filedialog.askopenfilename(filetypes=FILE_TYPES)
        print("OPEN FOI CHAMADO")
        logger.info("OPEN FOI CHAMADO")
        
        if not path:
            logger.info("Ação abrir cancelada pelo usuário")
            return

        try:
            content = FileService.read_file(path)

            text = self.view.create_new_tab(os.path.basename(path))
            text.insert("1.0", content)

            tab = self.get_current_tab()
            self.files[tab] = path
            self.modified[tab] = False

            text.bind("<KeyRelease>", self.update_status)
            text.bind("<<Modified>>", self.on_modified)

            logger.info(f"Arquivo aberto: {path}")

        except Exception as e:
            logger.error(f"Erro ao abrir arquivo {path}: {e}")

    # =====================
    # SAVE
    # =====================
    def save(self):
        tab = self.get_current_tab()
        text = self.view.get_current_text()

        if tab not in self.files:
            return self.save_as()

        path = self.files[tab]

        try:
            content = text.get("1.0", "end-1c")
            FileService.write_file(path, content)

            self.modified[tab] = False
            self.view.set_tab_title(os.path.basename(path))

            logger.info(f"Arquivo salvo: {path}")

        except Exception as e:
            logger.error(f"Erro ao salvar {path}: {e}")

    def save_as(self):
        tab = self.get_current_tab()

        path = filedialog.asksaveasfilename(filetypes=FILE_TYPES, defaultextension=".txt")
        if not path:
            return

        self.files[tab] = path
        self.view.set_tab_title(os.path.basename(path))
        self.save()

    # =====================
    # STATUS
    # =====================
    def update_status(self, event=None):
        text = self.get_current_text()
        row, col = text.index("insert").split(".")
        self.view.status.update_position(row, col)

    def on_modified(self, event=None):
        tab = self.get_current_tab()
        text = self.get_current_text()

        self.modified[tab] = text.edit_modified()
        text.edit_modified(False)

    def on_tab_change(self, event=None):
        self.update_status()

    # =====================
    # CLOSE
    # =====================
    def on_close(self):
        for tab, mod in self.modified.items():
            if mod:
                res = messagebox.askyesno("Sair", "Há arquivos não salvos. Deseja sair?")
                if not res:
                    return
                break

        self.root.destroy()

    # ===========
    # SEARCH
    # ===========

    def _on_ctrl_f(self, event=None):
        self.open_search()

    def open_search(self):
        text = self.get_current_text()

        if not text:
            return

        SearchDialog(self.root, text)