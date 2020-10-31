import multiprocessing as mp
from threading import Thread
from observer import MyObserver as Observer
from icon import Icon

PATH2SCAN = 'test_folder'
PATH2LOG = 'log.csv'
FIELDNAMES = ['timestamp', 'operation', 'source', 'destination', 'size']


if __name__ == "__main__":
    with mp.Manager() as manager:
        lock = mp.Lock()
        shared = manager.dict({
            'Observer'          : True,
            'Observer looping'  : False,
            'Icon'              : True,
        })
        processes = [
            mp.Process(name='Tray', target=Icon.start_tray, args=(shared, lock)),
            mp.Process(name='Observer', target=Observer.start_observer, args=(shared, lock, PATH2SCAN, PATH2LOG, FIELDNAMES)),
        ]
        for i in range(len(processes)):
            processes[i].start()
        for i in range(len(processes)):
            processes[i].join()