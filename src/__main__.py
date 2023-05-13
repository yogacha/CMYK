import tkinter as tk
from src.widget import CMYKColor, LabelSlider
from src import color


def main_widgets():
    global window, before_frame, after_frame, lab_consist, hue_consist
    window = tk.Tk()
    before_frame = CMYKColor(
        window,
        frame=tk.Frame(window, width=400, height=400)
    )
    before_frame.frame.pack(side=tk.LEFT)
    before_frame.place(10, 40)

    after_frame = CMYKColor(
        window,
        frame=tk.Frame(window, width=400, height=400)
    )
    after_frame.frame.pack(side=tk.RIGHT)
    after_frame.place(410, 40)

    lab_consist = tk.Scale(window, from_=0, to=20, resolution=0.5,
                           orient=tk.VERTICAL,
                           command=optimize_after_color)
    lab_consist.place(x=350, y=60)
    lab_consist.set(3)

    hue_consist = tk.Scale(window, from_=0, to=1, resolution=0.01,
                           orient=tk.VERTICAL,
                           command=optimize_after_color)
    hue_consist.place(x=300, y=60)
    hue_consist.set(0.01)

    before_frame.bind("<ButtonRelease-1>", optimize_after_color)


def print_ink(event):
    print(
        "Ink: {0:.2f}% -> {1:.2f}%".format(
            100 * color.total_ink(before_frame.cmyk),
            100 * color.total_ink(after_frame.cmyk)
        )
    )


def optimize_after_color(event):
    after = color.minimize_ink(
        before_frame.cmyk, lab_consist.get(), hue_consist.get())
    after_frame.cmyk = after

    print_ink(None)


main_widgets()
window.mainloop()
