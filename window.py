from threading import Thread
from tkinter import *
from time import sleep

class MyTk(Tk):

    def __init__(self, shared, lock, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textVariable = StringVar(self, '')
        self.label = Label(self, textvariable=self.textVariable)
        self.label.pack(fill=BOTH, expand=1)
        self.thread = Thread(target=self.thread_loop, args=(shared, lock), daemon=False)
        self.thread.start()
        self.alive = True

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
            sleep(0.05)
        print('out of loop')
        if self.alive:
            self.after(0, self.destroy)
        print('after destroy')

    def destroy(self):
        self.alive = False
        print('in')
        self.thread.join()
        print('out')
        super().destroy()

    @classmethod
    def start_window(cls, shared, lock):
        lock.acquire()
        alive = shared['Window']
        lock.release()
        while alive:
            root = cls(shared, lock)
            root.mainloop()
            root = cls(shared, lock)
            root.mainloop()
            lock.acquire()
            alive = shared['Window']
            lock.release()

class VariableLabel(Label):
    def __init__(self, master, *args, **kwargs):
        self.textvariable = StringVar(master, kwargs['textvariable'])
        kwargs['textvariable'] = self.textvariable
        super().__init__(master=master, *args, **kwargs)

    def set(self, text):    self.textvariable.set(text)
    def get(self):          self.textvariable.get()