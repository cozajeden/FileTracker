from multiprocessing import Process, Manager, Lock
from observer import MyObserver as Observer
from window import MyTk as Tk
from icon import Icon

PATH2SCAN = 'test_folder'
PATH2LOG = 'log.csv'
FIELDNAMES = ['timestamp', 'operation', 'source', 'destination', 'size']


if __name__ == "__main__":
    with Manager() as manager:
        lock = Lock()
        shared = manager.dict({
            'Observer'          : True,
            'Observer looping'  : False,
            'Icon'              : True,
            'Window'            : True,
            'Window input text' : None,
        })
        processes = [
            Process(name='Tray', target=Icon.start_tray, args=(shared, lock)),
            Process(name='Window', target=Tk.start_window, args=(shared, lock)),
            Process(name='Observer', target=Observer.start_observer, args=(shared, lock, PATH2SCAN, PATH2LOG, FIELDNAMES)),
        ]
        for i in range(len(processes)):
            processes[i].start()
        for i in range(len(processes)):
            processes[i].join()