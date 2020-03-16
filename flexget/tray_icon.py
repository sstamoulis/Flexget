import logging
from pathlib import Path

from PIL import Image
from pystray import Icon, Menu, MenuItem

from flexget import __version__


class TrayIcon:
    def __init__(self, manager, path_to_image: Path):
        self.manager = manager
        self.path_to_image = path_to_image
        self.icon = None
        self._menu = None
        self.menu_items = []
        self.running = False
        self.add_default_menu_items()

    def add_menu_item(self, menu_item: MenuItem):
        self.menu_items.append(menu_item)

    def add_default_menu_items(self):
        self.add_menu_item(MenuItem(f'Flexget {__version__}', None, enabled=False))
        self.add_menu_item(Menu.SEPARATOR)
        self.add_menu_item(MenuItem('Shutdown', self.manager.shutdown))
        self.add_menu_item(MenuItem('Reload Config', self.manager.load_config))

    @property
    def menu(self) -> Menu:
        if not self._menu:
            self._menu = Menu(*self.menu_items)
        return self._menu

    def run(self):
        logging.getLogger('PIL.PngImagePlugin').setLevel(logging.INFO)  # Silence PIL noisy logging
        logging.getLogger('PIL.Image').setLevel(logging.INFO)  # Silence PIL noisy logging
        self.icon = Icon('Flexget', Image.open(self.path_to_image), menu=self.menu)
        self.running = True
        self.icon.run()  # This call is blocking and must be done from main thread

    def stop(self):
        self.icon.stop()
        self.running = False
