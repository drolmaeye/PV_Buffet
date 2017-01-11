__author__ = 'j.smith'

# import necessary modules
from Tkinter import *
from epics import *

class LogEntry:
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.pack()

        self.new_pv = StringVar()

        self.pv_entry = Entry(self.frame, textvariable=self.new_pv, width=30)
        self.pv_entry.grid(row=0, column=0)
        self.pv_entry.bind('<Return>', self.pv_connect)

    def pv_connect(self, event):
        global alpha
        alpha = PV(self.new_pv.get())
        print alpha.value

root = Tk()

entry1 = LogEntry(root)
root.mainloop()