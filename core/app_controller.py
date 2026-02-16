from ui.search_dialog import SearchDialog

def open_Search(self):
    text = self.view.get_current_text()

    if not text:
        return
    
    SearchDialog(self.view.root, text)