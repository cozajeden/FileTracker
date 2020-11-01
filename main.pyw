from multiprocessing import Process, Manager, Lock
from observer import MyObserver as Observer
from window import MyTk as Tk
from icon import Icon

if __name__ == "__main__":
    with Manager() as manager:
        lock = Lock()
        shared = manager.dict({
            'Observer'          : True,
            'Observer looping'  : False,
            'Icon'              : True,
            'Window'            : True,
            'Window input text' : None,
            'path2scan'         : 'test_folder',
            'path2log'          : 'log.csv',
            'fieldnames'        : ['timestamp', 'operation', 'source', 'destination', 'size'],
        })
        processes = [
            Process(name='Tray', target=Icon.start_tray, args=(shared, lock)),
            Process(name='Window', target=Tk.start_window, args=(shared, lock)),
            Process(name='Observer', target=Observer.start_observer, args=(shared, lock)),
        ]
        for i in range(len(processes)):
            processes[i].start()
        for i in range(len(processes)):
            processes[i].join()