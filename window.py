from threading import Thread
from tkinter import *
from time import sleep

class MyTk(Tk):

    def __init__(self, shared, lock, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alive = True
        self.withdraw() # hide window
        self.textVariable = StringVar(self, '')
        self.label = Label(self, textvariable=self.textVariable)
        self.label.pack(fill=BOTH, expand=1)
        # Start thread_loop in separate thread
        self.thread = Thread(target=self.thread_loop, args=(shared, lock), daemon=False)
        self.thread.start()

    def thread_loop(self, shared, lock):
        "Function is running in separate thread."
        while True:
            lock.acquire()
            alive = shared['Window']
            inText = shared['Window input text']
            lock.release()
            # Break loop if got signal to break (alive=False)
            # or if user closed the window (self.alive=False)
            if not alive or not self.alive: break
            if inText is not None:
                lock.acquire()
                shared['Window input text'] = None
                lock.release()
                self.textVariable.set(inText)
                self.deiconify() # show window
            sleep(0.05)
        # If got signal to close window from other process
        if self.alive:
            self.after(0, self.destroy)

    def destroy(self):
        # Kill thread_loop
        self.alive = False
        # Wait for thread to finish
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
            sleep(1)
            lock.acquire()
            alive = shared['Window']
            lock.release()