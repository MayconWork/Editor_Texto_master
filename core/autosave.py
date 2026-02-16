import threading
import time

class AutoSave:
    def __init__(self, controller, interval=5):
        self.controller = controller
        self.interval = interval
        self.running = True
        self.start()

    def start(self):
        thread = threading.Thread(target=self._loop, daemon=True)
        thread.start()

    def _loop(self):
        while self.running:
            time.sleep(self.interval)
            self.controller.autosave()