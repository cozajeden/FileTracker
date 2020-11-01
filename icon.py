import pystray
from PIL import Image, ImageDraw

class Icon(pystray.Icon):

    def __init__(self, shared, lock, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shared = shared
        self.lock = lock
        self.menu = menu=pystray.Menu(
            pystray.MenuItem('start Watchdog', self.start_loop),
            pystray.MenuItem('stop Watchdog', self.stop_loop),
            pystray.MenuItem('exit', self.stop, default=True),
        )
        self.icon = Icon.img()

    def stop(self, *args, **kwargs):
        self.stop_loop()
        # Send kill signal to other processes
        self.lock.acquire()
        self.shared['Observer'] = False
        self.shared['Window'] = False
        self.lock.release()
        super().stop(*args, **kwargs)

    def start_loop(self, *args, **kwargs):
        self.lock.acquire()
        self.shared['Observer looping'] = True
        self.lock.release()

    def stop_loop(self, *args, **kwargs):
        self.lock.acquire()
        self.shared['Observer looping'] = False
        self.lock.release()

    @classmethod
    def start_tray(cls, shared, lock):
        icon = cls(shared=shared, lock=lock, name='main')
        icon.run()

    @classmethod
    def img(cls):
        "Generate an image and draw a pattern."
        pixels = 32
        color1, color2 =  '#00ff00', '#0000ff'
        image = Image.new('RGB', (pixels, pixels), color1)
        dc = ImageDraw.Draw(image)
        dc.rectangle(
            (pixels // 2, 0, pixels, pixels // 2),
            fill=color2
        )
        dc.rectangle(
            (0, pixels // 2, pixels // 2, pixels),
            fill=color2
        )
        return image