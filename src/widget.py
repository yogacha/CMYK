import tkinter as tk
from collections import OrderedDict
from typing import Callable

from src import color


class _Polymer(object):
    def __init__(self):
        self.elements: OrderedDict[str, tk.Widget]

    def bind(self, sequence=None, func=None, add=None):
        for ele in self.elements.values():
            ele.bind(sequence, func, add)

    def __getitem__(self, key):
        return self.elements[key]


class Placeable(_Polymer):
    _dx: int = 0
    _dy: int = 0

    def place(self, x, y, dx=None, dy=None):
        dx = self._dx if dx is None else dx
        dy = self._dy if dy is None else dy
        for i, element in enumerate(self.elements.values()):
            element.place(x=x + dx * i, y=y + dy * i)


class SimpleSlider(tk.Scale):
    def __init__(self, master, from_=0, to=1, orient=tk.HORIZONTAL, command=None):
        resolution = (to - from_) / 100
        super().__init__(master, from_=from_, to=to, orient=orient,
                         resolution=resolution, command=command)


class LabelSlider(Placeable):
    _dx, _dy = 20, -20

    def __init__(self, master, text, default=0, command=None):
        self.elements = OrderedDict({
            "label": tk.Label(master, text=text),
            "slider": SimpleSlider(master, from_=0, to=1, command=command),
        })
        self["slider"].set(default)


class CMYKColor(Placeable):
    _dx, _dy = 0, 35

    def __init__(self, master, frame: tk.Frame):
        self.frame = frame
        self.elements = OrderedDict({
            "C": LabelSlider(master, "C:", command=self.__call__),
            "M": LabelSlider(master, "M:", command=self.__call__),
            "Y": LabelSlider(master, "Y:", command=self.__call__),
            "K": LabelSlider(master, "K:", command=self.__call__),
        })
        self.__callbacks = []
        self.add_callback(self.__update_frame)

    @property
    def cmyk(self):
        return (
            self["C"]["slider"].get(),
            self["M"]["slider"].get(),
            self["Y"]["slider"].get(),
            self["K"]["slider"].get(),
        )

    @cmyk.setter
    def cmyk(self, value: tuple[float, float, float, float]):
        for ele, val in zip(self.elements.values(), value):
            ele["slider"].set(val)

    @property
    def rgb(self):
        return color.cmyk2rgb(self.cmyk)

    def __call__(self, event):
        for callback in self.__callbacks:
            callback(event)

    def add_callback(self, callback: Callable):
        self.__callbacks.append(callback)

    def __update_frame(self, event=None):
        self.frame.config(bg="#{0:02x}{1:02x}{2:02x}".format(*self.rgb))
