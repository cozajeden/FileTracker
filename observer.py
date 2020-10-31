import time, os, csv, datetime
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class PMEHandler(PatternMatchingEventHandler):
    def __init__(self, path2log, fieldnames, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fieldnames = fieldnames
        self.path2log = path2log
        if path2log not in os.listdir():
            with open(path2log, 'w', newline ='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

    def on_created(self, event):
        self.save_row(event, 'created')

    def on_deleted(self, event):
        self.save_row(event, 'deleted')

    def on_modified(self, event):
        self.save_row(event, 'modified')

    def on_moved(self, event):
        self.save_row(event, 'moved')

    def save_row(self, event, operation):
        with open(self.path2log, 'a+', newline ='') as log:
            writer = csv.DictWriter(log, fieldnames=self.fieldnames)

            row = {
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                'operation': operation,
                'source': event.src_path
            }

            if operation == 'moved':
                row['destination'] = event.dest_path
            else:
                row['destination'] = None

            if operation != 'deleted':
                row['size'] = os.stat(event.src_path).st_size
            else:
                row['size'] = 0

            writer.writerow(row)


class MyObserver(Observer):
    
    @classmethod
    def start_observer(cls, shared, lock, path2scan, path2log, fieldnames):
        observing = False
        observer = None
        while True:
            lock.acquire()
            alive =  shared['Observer']
            loop =  shared['Observer looping']
            lock.release()
            if not alive: 
                break
            if not observing and loop:
                my_event_handler = PMEHandler(path2log=path2log, fieldnames=fieldnames, patterns='*', ignore_patterns='', ignore_directories=False, case_sensitive=False)
                observer = cls()
                observer.schedule(my_event_handler, path=path2scan, recursive=True)
                observer.start()
                observing = True
            if observing and not loop:
                observer.stop()
                observer.join()
                observing = False
            time.sleep(1)