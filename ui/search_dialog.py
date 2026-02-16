import tkinter as tk


class SearchDialog:

    def __init__(self, root, text_widget):
        self.root = root
        self.text = text_widget

        self.win = tk.Toplevel(root)
        self.win.title("Buscar e Substituir")
        self.win.geometry("350x140")
        self.win.transient(root)

        # ========= BUSCA =========
        tk.Label(self.win, text="Buscar").pack(anchor="w", padx=10)
        self.search_entry = tk.Entry(self.win)
        self.search_entry.pack(fill="x", padx=10)
        self.search_entry.focus()

        # ========= SUBSTITUIR =========
        tk.Label(self.win, text="Substituir por").pack(anchor="w", padx=10, pady=(8, 0))
        self.replace_entry = tk.Entry(self.win)
        self.replace_entry.pack(fill="x", padx=10)

        # ========= BOTÕES =========
        btn_frame = tk.Frame(self.win)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Buscar", command=self.search).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Substituir", command=self.replace_one).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Substituir tudo", command=self.replace_all).pack(side="left", padx=5)

        self.search_entry.bind("<Return>", self.search)

    # =============================
    def search(self, event=None):
        term = self.search_entry.get()

        self.text.tag_remove("search", "1.0", "end")

        if not term:
            return

        start = "1.0"
        count = 0

        while True:
            pos = self.text.search(term, start, stopindex="end")

            if not pos:
                break

            end = f"{pos}+{len(term)}c"
            self.text.tag_add("search", pos, end)
            start = end
            count += 1

        self.text.tag_config("search", background="#44475a", foreground="white")

        self.win.title(f"{count} ocorrências")

    # =============================
    def replace_one(self):
        term = self.search_entry.get()
        replacement = self.replace_entry.get()

        if not term:
            return

        # pega seleção atual se existir
        try:
            start = self.text.index("sel.first")
            end = self.text.index("sel.last")

            selected = self.text.get(start, end)

            if selected == term:
                self.text.delete(start, end)
                self.text.insert(start, replacement)

                next_pos = self.text.search(term, start, stopindex="end")

                if next_pos:
                    next_end = f"{next_pos}+{len(term)}c"
                    self.text.tag_remove("sel", "1.0", "end")
                    self.text.tag_add("sel", next_pos, next_end)
                    self.text.mark_set("insert", next_end)
                    self.text.see(next_pos)

                self.search()
                return
        except:
            pass

        # se nada selecionado → busca primeira
        pos = self.text.search(term, "1.0", stopindex="end")

        if pos:
            end = f"{pos}+{len(term)}c"
            self.text.tag_remove("sel", "1.0", "end")
            self.text.tag_add("sel", pos, end)
            self.text.mark_set("insert", end)
            self.text.see(pos)

    # =============================
    def replace_all(self):
        term = self.search_entry.get()
        replacement = self.replace_entry.get()

        if not term:
            return

        content = self.text.get("1.0", "end-1c")
        new_content = content.replace(term, replacement)

        self.text.delete("1.0", "end")
        self.text.insert("1.0", new_content)

        self.search()