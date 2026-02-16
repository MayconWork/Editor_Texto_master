import tkinter as tk
from ui.editor_view import EditorView
from core.editor_controller import EditorController
from utils.constants import APP_NAME, DEFAULT_GEOMETRY

def main():
    root = tk.Tk()
    root.title(APP_NAME)
    root.geometry(DEFAULT_GEOMETRY)

    view = EditorView(root)
    EditorController(root, view)

    root.mainloop()

if __name__ == "__main__":
    main() 