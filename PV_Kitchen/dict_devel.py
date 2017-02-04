from Tkinter import *
import collections



class MasterDropdown:

    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.grid(row=1, column=number_of_pvs)

        mpv = [('Timestamp', ['Timestamp']),
               ('Sample stages', ['XPS Cen X', 'XPS Cen Y', 'XPS Sam Z', 'XPS Omega']),
               ('Counts', ['Ring current', 'IDA-IC', 'IDB-IC', 'Beamstop'])
               ]

        mpv = collections.OrderedDict(mpv)

        self.pv_choice = StringVar()

        self.menubutton = Menubutton(self.frame, textvariable=self.pv_choice, indicatoron=True)
        self.main_menu = Menu(self.menubutton)
        self.menubutton.configure(menu=self.main_menu)

        for key in mpv.keys():
            menu = Menu(self.main_menu)
            self.main_menu.add_cascade(label=key, menu=menu)
            for value in mpv[key]:
                menu.add_radiobutton(label=value, variable=self.pv_choice, value=value)

        self.menubutton.pack()

        self.pv_choice.trace('w', self.clear)

    def clear(self, *kargs):
        self.menubutton.configure(indicatoron=False)


def create_pv():
    MasterDropdown(root)
    print number_of_pvs
    global number_of_pvs
    number_of_pvs += 1
    print number_of_pvs
    return number_of_pvs







root = Tk()
number_of_pvs = 0
button = Button(root, text='New PV', command=create_pv)
button.grid(row=0, column=0)
root.mainloop()

