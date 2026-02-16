import tkinter as tk

class StatusBar(tk.Label):

    def __init__(self, root):
        super().__init__(root, anchor="e")
        self.pack(fill=tk.X, side=tk.BOTTOM, ipady=2)

    def update_position(self, row: str, col: str):
        self.config(text=f"Linha {row} | Coluna {int(col)+1}")
        