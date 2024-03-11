import dataset
from datetime import datetime
from io import BytesIO
from pathlib import Path
import random
import requests
from zipfile import ZipFile

from textual.app import App
from textual.widgets import DataTable, Footer


db = dataset.connect('sqlite:///games.db')
history = db['history']
download_dir = Path('downloads') / datetime.now().strftime('%Y-%m-%d')
download_dir.mkdir(parents=True, exist_ok=True)


class PenguinApp(App):

    BINDINGS = [
        ('r', 'r_pressed', 'Randomise')
    ]

    COLUMNS = {'name', 'by', 'category', 'year', 'download'}

    def compose(self):
        self.games = DataTable()
        yield self.games
        yield Footer()

    def on_mount(self):
        self.rows = list(db.query('select name, by, category, year, download, id, url from history'))
        self.url_lookup = {row['id']: row['url'] for row in self.rows}
        self.ids = [row['id'] for row in self.rows]
        for column in self.rows[0]:
            if column in self.COLUMNS:
                self.games.add_column(column, key=column)
        for row in self.rows:
            self.games.add_row(*[v[:50] for k, v in row.items() if k in self.COLUMNS], key=row['id'])
        self.games.cursor_type = 'row'

    def action_r_pressed(self):
        self.games.sort(key=lambda _: random.random())

    def on_data_table_row_selected(self, row):
        download_url = 'https://spectrumcomputing.co.uk/' + self.url_lookup[row.row_key.value]
        r = requests.get(download_url)
        zf = ZipFile(BytesIO(r.content))
        zf.extractall(download_dir)


if __name__ == '__main__':
    app = PenguinApp()
    app.run()
    
        
        
    

