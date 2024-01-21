from typing import Optional
from .listener import Change, Listener
from dtos import Graph, Flow
from common import Core
from tempfile import TemporaryDirectory
import time
from PIL import Image
import os

class Plotter(Listener):
    def __init__(self) -> None:
        self.temp_directory = None

    def on_start(self, graph: Graph, core: Core) -> None:
        if self.temp_directory is None:
            self.temp_directory = TemporaryDirectory()
        else:
            print("Warning: Writer already entered")

    def on_iteration(self, flow: Flow, change: Optional[Change]) -> None:
        fig = flow.draw()
        fig.savefig(f'{self.temp_directory.name}/{time.time()}.png')

    def on_end(self) -> None:
        frames=[]
        for file in (os.listdir(self.temp_directory.name)):
            frames.append(Image.open(self.temp_directory.name+"/"+file))
        frames = frames[0:1]+frames+frames[-1:]
        frames[0].save(f'outputs/{time.time()}.gif', save_all=True, append_images=frames[1:], duration=len(frames)*155, loop=0)
