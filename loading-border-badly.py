import csv
import random
from textual.app import App, ComposeResult, RenderableType
from textual.containers import Container
from textual.renderables.gradient import LinearGradient
from textual.widgets import Static



with open('zxdbdump.txt') as fin:
    games = list(csv.reader(fin, delimiter='|'))



class LoadingBorder(Container):

    DEFAULT_CSS = """
    Splash {
        align: center middle;
    }
    Static {
        min-width: 85%;
        max-width: 85%;
        min-height: 70%;
        align: center middle;
        text-align: center;
    }
    """

    def on_mount(self) -> None:
        self.auto_refresh = 1 / 8 

    def compose(self) -> ComposeResult:
        yield Static('KNICKERS!', id='game')  

    def render(self) -> RenderableType:
        colours = random.choices(['#FF00FF', '#000000'], weights=[0.3, 0.7], k=50)
        stops = [(i / (len(colours) - 1), colour) for i, colour in enumerate(colours)]
        return LinearGradient(90, stops)  


class LoadingApp(App):
    def compose(self) -> ComposeResult:
        yield LoadingBorder()
        self.set_interval(0.05, self.set_static)

    def set_static(self):
        game = random.choice(games)
        self.query_one('Static').update('{1} - {2} ({3})'.format(*game))
        


if __name__ == "__main__":
    app = LoadingApp()
    app.run()