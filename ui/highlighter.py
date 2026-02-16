import keyword
import re


class Highlighter:

    def __init__(self, text):
        self.text = text
        self._setup_tags()

        self.text.bind("<KeyRelease>", self.highlight)

    # =========================
    def _setup_tags(self):

        self.text.tag_config("keyword", foreground="#ff79c6")
        self.text.tag_config("string", foreground="#f1fa8c")
        self.text.tag_config("comment", foreground="#6272a4")
        self.text.tag_config("number", foreground="#bd93f9")
        self.text.tag_config("defclass", foreground="#50fa7b")

    # =========================
    def highlight(self, event=None):

        content = self.text.get("1.0", "end-1c")

        for tag in ["keyword", "string", "comment", "number", "defclass"]:
            self.text.tag_remove(tag, "1.0", "end")

        self._highlight_keywords(content)
        self._highlight_strings(content)
        self._highlight_comments(content)
        self._highlight_numbers(content)
        self._highlight_def_class(content)

    # =========================
    def _highlight_keywords(self, content):
        for kw in keyword.kwlist:
            for match in re.finditer(rf"\b{kw}\b", content):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.text.tag_add("keyword", start, end)

    # =========================
    def _highlight_strings(self, content):
        for match in re.finditer(r"(\".*?\"|\'.*?\')", content):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.text.tag_add("string", start, end)

    # =========================
    def _highlight_comments(self, content):
        for match in re.finditer(r"#.*", content):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.text.tag_add("comment", start, end)

    # =========================
    def _highlight_numbers(self, content):
        for match in re.finditer(r"\b\d+\b", content):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.text.tag_add("number", start, end)

    # =========================
    def _highlight_def_class(self, content):
        for match in re.finditer(r"\b(def|class)\s+(\w+)", content):
            start = f"1.0+{match.start(2)}c"
            end = f"1.0+{match.end(2)}c"
            self.text.tag_add("defclass", start, end)