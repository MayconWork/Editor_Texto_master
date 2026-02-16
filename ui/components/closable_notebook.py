import tkinter as tk
from tkinter import ttk


class ClosableNotebook(ttk.Notebook):
    def __init__(self, master, on_tab_close=None, **kwargs):
        super().__init__(master, **kwargs)

        self.on_tab_close_callback = on_tab_close
        self._create_style()

        self.bind("<Button-1>", self._on_click, True)

    # ==========================
    # STYLE
    # ==========================
    def _create_style(self):
        style = ttk.Style()

        # cria imagem X
        self.close_img = tk.PhotoImage(width=12, height=12)
        self.close_img.put(("red",), to=(3, 3, 9, 9))

        style.element_create("close", "image", self.close_img)

        style.layout("ClosableNotebook.TNotebook.Tab", [
            ("Notebook.tab", {
                "sticky": "nswe",
                "children": [
                    ("Notebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("Notebook.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("Notebook.label", {"side": "left", "sticky": ""}),
                                    ("close", {"side": "left", "sticky": ""}),
                                ]
                            })
                        ]
                    })
                ]
            })
        ])

        self.configure(style="ClosableNotebook.TNotebook")

    # ==========================
    # CLICK
    # ==========================
    def _on_click(self, event):
        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index(f"@{event.x},{event.y}")
            tab_id = self.tabs()[index]

            if self.on_tab_close_callback:
                self.on_tab_close_callback(tab_id)

            self.forget(index)