from Tkinter import *
import collections
from epics import *


class MasterDropdown:
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.grid(row=1, column=number_of_pvs)

        self.pv_choice = StringVar()
        self.pv_choice.set('Select a PV')

        self.menubutton = Menubutton(self.frame, textvariable=self.pv_choice, indicatoron=True)
        self.main_menu = Menu(self.menubutton)
        self.menubutton.configure(menu=self.main_menu)

        for key in mpv_od.keys():
            menu = Menu(self.main_menu)
            self.main_menu.add_cascade(label=key, menu=menu)
            for value in mpv_od[key]:
                menu.add_radiobutton(label=value, variable=self.pv_choice, value=value)

        self.menubutton.pack()

        self.pv_choice.trace('w', self.connect)

    # ###def clear(self, *kargs):
    # ###    self.menubutton.configure(indicatoron=False)
    # ###    pv_name = self.pv_choice.get()
    # ###    pv = master_map[pv_name]
    # ###    a = PV(pv)
    # ###    print a.char_value
    # ###    print a.info

    def connect(self, *kargs):
        self.menubutton.configure(indicatoron=False)
        pv_name = self.pv_choice.get()
        pv = master_map[pv_name]
        a = PV(pv)
        print a.char_value
        print a.info


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






def create_pv():
    MasterDropdown(root)
    global number_of_pvs
    number_of_pvs += 1
    # return number_of_pvs

master_map = {'Timestamp': 'S:IOC:timeOfDayForm1SI',
              'XPS Cen X': 'XPSGP:m1.RBV',
              'XPS Cen Y': 'XPSGP:m2.RBV',
              'XPS Sam Z': 'XPSGP:m3.RBV',
              'XPS Omega': 'XPSGP:m4.RBV',
              'Ring current': 'S:SRcurrentAI.VAL',
              'IDA-IC': '16IDB:scaler1_cts2.A',
              'IDB-IC': '16IDB:scaler1_cts1.C',
              'Beamstop': '16IDB:scaler1_cts2.B'}

mpv = [('Timestamp', ['Timestamp']),
       ('Sample stages', ['XPS Cen X', 'XPS Cen Y', 'XPS Sam Z', 'XPS Omega']),
       ('Counts', ['Ring current', 'IDA-IC', 'IDB-IC', 'Beamstop'])]

mpv_od = collections.OrderedDict(mpv)



root = Tk()
number_of_pvs = 0
allClasses = []
button = Button(root, text='New PV', command=create_pv)
button.grid(row=0, column=0)
root.mainloop()



