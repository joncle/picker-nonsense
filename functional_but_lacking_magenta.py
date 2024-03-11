import csv
from datetime import datetime
from io import BytesIO
from pathlib import Path
import random
import requests
from zipfile import ZipFile

from textual.app import App
from textual.widgets import Label


ZX_GAME_DUMP_FILE = 'zxdbdump.txt'
BASE_URL = 'https://spectrumcomputing.co.uk'
DOWNLOAD_DIR = Path('downloads') / datetime.now().strftime('%Y-%m-%d')
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)


class LoaderApp(App):
    def __init__(self, game_file, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open(game_file) as fin:
            self._games = list(csv.reader(fin, delimiter='|'))
        
    CSS = """
        Screen {
            layout: grid;
            grid-size: 2 3;
            grid-columns: 1fr 9fr;
            grid-rows: 84% 8% 8%;
            background: white;
            color: black;
        }
        .span2 { column-span: 2; width: 100%; }
        #tape-loader {
            background: black;
            color: white;
        }
    """
    BINDINGS = [
        ('space', 'space_pressed', 'Stop'),
        ('enter', 'enter_pressed', 'Download')
    ]
    
    def compose(self):
        yield Label('Program:  ')
        yield Label('Press SPACE to start the nonsense!', id='game-name')
        yield Label('Tape Loader', id='tape-loader', classes='span2')
        yield Label('To stop - press SPACE', id='status-line', classes='span2')

    def on_mount(self):
        self.rg_timer = self.set_interval(0.05, self.randomise_game)
        self.rg_timer_running = True

    def randomise_game(self):
        self._game = random.choice(self._games)
        self.query_one('#game-name').update(self._game[1])

    def action_space_pressed(self):
        if self.rg_timer_running:
            self.rg_timer.pause()
            self.query_one('#status-line').update('To download {5} - press ENTER. To resume randomising - press SPACE'.format(*self._game))
        else:
            self.rg_timer.resume()
            self.query_one('#status-line').update('To stop - press SPACE')
        self.rg_timer_running = not self.rg_timer_running

    def action_enter_pressed(self):
        if not self.rg_timer_running:
            r = requests.get(BASE_URL + self._game[5])
            zf = ZipFile(BytesIO(r.content))
            for filename in zf.namelist():
                file_location = zf.extract(filename, path=DOWNLOAD_DIR)
                self.query_one('#status-line').update(f'Saved as {file_location} - ENJOY!. To resume randomising - press SPACE')
                
            
if __name__ == '__main__':
    app = LoaderApp(ZX_GAME_DUMP_FILE)
    app.run()
            
        