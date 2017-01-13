__author__ = 'j.smith'

# import necessary modules
from Tkinter import *
from epics import *


class LogEntry:
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.pack()

        self.new_pv = None
        self.new_pv_var = StringVar()

        self.pv_entry = Entry(self.frame, textvariable=self.new_pv_var, width=30)
        self.pv_entry.grid(row=0, column=0, padx=10, pady=10)
        self.pv_entry.bind('<Return>', self.pv_connect)
        self.pv_entry.bind_all('<B2-Motion>', self.on_motion)
        self.pv_entry.bind('<ButtonRelease-2>', self.pv_print)

    def on_motion(self, event):
        widget = root.winfo_containing(event.x_root, event.y_root)
        widget.focus_set()

    def pv_connect(self, event):
        print 'connect it'
        self.new_pv = PV(self.new_pv_var.get())
        print self.new_pv.value

    def pv_print(self, event):
        print 'write it'
        omg = root.clipboard_get()
        self.new_pv_var.set(omg)







root = Tk()
entry1 = LogEntry(root)
entry2 = LogEntry(root)
root.bind('<Enter>', lambda event: root.focus_set())
root.mainloop()
