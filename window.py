from threading import Thread
from tkinter import *
from time import sleep

class MyTk(Tk):

    def __init__(self, shared, lock, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alive = True
        self.withdraw()
        self.textVariable = StringVar(self, '')
        self.label = Label(self, textvariable=self.textVariable)
        self.label.pack(fill=BOTH, expand=1)
        self.thread = Thread(target=self.thread_loop, args=(shared, lock), daemon=False)
        self.thread.start()

    def thread_loop(self, shared, lock):
        while True:
            lock.acquire()
            alive = shared['Window']
            inText = shared['Window input text']
            lock.release()
            if not alive or not self.alive: break
            if inText is not None:
                lock.acquire()
                shared['Window input text'] = None
                lock.release()
                self.textVariable.set(inText)
                self.deiconify()
            sleep(0.05)
        if self.alive:
            self.after(0, self.destroy)

    def destroy(self):
        self.alive = False
        self.thread.join()
        super().destroy()

    @classmethod
    def start_window(cls, shared, lock):
        lock.acquire()
        alive = shared['Window']
        lock.release()
        while alive:
            root = cls(shared, lock)
            root.mainloop()
            lock.acquire()
            alive = shared['Window']
            lock.release()