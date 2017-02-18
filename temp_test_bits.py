from Tkinter import *

root = Tk()


class App:
    def __init__(self, master):
        scrollbar = Scrollbar(master, orient=VERTICAL)
        self.b1 = Listbox(master, yscrollcommand=scrollbar.set)
        self.b2 = Listbox(master, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.b1.pack(side=LEFT, fill=BOTH, expand=1)
        self.b2.pack(side=LEFT, fill=BOTH, expand=1)

    def yview(self, *args):
        apply(self.b1.yview, args)
        apply(self.b2.yview, args)


app = App(root)
for item in range(0, 100):
    app.b1.insert(0, item)
    app.b2.insert(0, item)

root.mainloop()