from queue import Queue
from threading import Thread, Event

from src.app.backend.types import ActorExit


class Actor:
    def __init__(self):
        self._mailbox = Queue()
        self._terminated = None

    def start(self):
        self._terminated = Event()
        t = Thread(target=self._bootstrap, daemon=True)
        t.start()

    def _bootstrap(self):
        try:
            self.run()
        except ActorExit:
            pass
        finally:
            self._terminated.set()

    def run(self):
        while True:
            self.recv()

    def send(self, msg):
        self._mailbox.put(msg)

    def recv(self):
        msg = self._mailbox.get()
        if msg is ActorExit:
            raise ActorExit()
        return msg

    def close(self):
        self.send(ActorExit)

    def join(self):
        self._terminated.wait()
