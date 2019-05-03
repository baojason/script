#!/usr/bin/python3
from tkinter import *
window = Tk()
window.title("Welcom to python gui")
window.geometry('350x200')
lbl = Label(window, text="Hello", font=("Arial Bold", 12))
lbl.grid(column=0, row=0)
txt = Entry(window, width=10)
txt.grid(column=1, row=0)
def clicked():
    res = "Welcom to " + txt.get()
    lbl.configure(text=res)
btn = Button(window, text="Click Me", command=clicked)
btn.grid(column=0, row=1)
window.mainloop()
