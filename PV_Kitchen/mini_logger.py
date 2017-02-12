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

        for key in dropdown_dict.keys():
            menu = Menu(self.main_menu)
            self.main_menu.add_cascade(label=key, menu=menu)
            for value in dropdown_dict[key]:
                menu.add_radiobutton(label=value, variable=self.pv_choice, value=value)

        self.menubutton.pack()
        self.pv_choice.trace('w', self.pv_append)

    def pv_append(self, *kargs):
        self.menubutton.configure(indicatoron=False)#, state=DISABLED)
        pv_name = self.pv_choice.get()
        pv_label = Label(text=pv_name)
        pv_value = StringVar()
        pv_object = PV(master_dict[pv_name])
        pv_object.add_callback(lambda **kwargs: pv_value.set(pv_object.value))
        pv_object.run_callbacks()
        entry = (pv_name, [pv_label, pv_value, pv_object, master_dict[pv_name]])
        # print entry
        logger_list.append(entry)
        print logger_list
        # print number_of_pvs


class LogLine:
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.grid()

        global line_index
        column = 0
        for keys in logger_dict.iterkeys():
            print column
            # current_value = logger_dict[keys][1].get()
            line_label = Label(self.frame, text=logger_dict[keys][1].get())
            line_label.grid(row=line_index, column=column)
            column += 1
        line_index += 1


class LoggerWindow:
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.grid(row=2)

        self.line_index = 1
        self.make_headings()
        self.canvas = Canvas(self.frame, width=800, borderwidth=0, background='#ffffff')
        self.inner_frame = Frame(self.canvas, background='#ffffff')
        self.vsb = Scrollbar(self.frame, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.hsb = Scrollbar(self.frame, orient='horizontal', command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.hsb.set)
        self.vsb.grid(row=1, column=1, sticky=NS)
        self.hsb.grid(row=2, column=0, sticky=EW)
        self.canvas.grid(row=1, column=0)
        # self.vsb.pack(side='right', fill='y')
        # self.hsb.pack(side='bottom', fill='x')
        # self.canvas.pack(side='left', fill='both', expand=True)
        self.canvas.create_window((4, 4), window=self.inner_frame, anchor='nw',
                                  tags='self.inner_frame')

        self.inner_frame.bind('<Configure>', self.on_frame_configure)


        self.button4 = Button(root, text='Log', command=self.log_it)
        self.button4.grid(row=0, column=3, padx=5)

    def make_headings(self):
        column = 0
        for keys in logger_dict.iterkeys():
            column_head = Label(self.frame, text=keys)
            column_head.grid(row=0, column=column)
            column += 1

    def on_frame_configure(self, event):
        pass
        # auto-increase scroll region
        # self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        # automatically scroll to last line
        # self.canvas.yview_moveto(1.0)

    def log_it(self):
        column = 0
        for keys in logger_dict.iterkeys():
            print column
            # current_value = logger_dict[keys][1].get()
            line_label = Label(self.inner_frame, text=logger_dict[keys][1].get())
            line_label.grid(row=self.line_index, column=column)
            column += 1
        self.line_index += 1
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        self.canvas.yview_moveto(1.0)
        

def log_it():
    LogLine(root)

def create_entry():
    MasterDropdown(root)
    global number_of_pvs
    # print number_of_pvs
    number_of_pvs += 1


def create_pvs():
    global logger_dict
    logger_dict = collections.OrderedDict(logger_list)
    print logger_dict
    LoggerWindow(root)


def print_it():
    for keys in logger_dict.iterkeys():
        print keys, logger_dict[keys][1].get(), logger_dict[keys][2].value













root = Tk()

number_of_pvs = 0
line_index = 0

# Dropdown collected in list first to accommodate ordered dictionary
dropdown_list = [('Timestamp', ['Timestamp']),
               ('Sample stages', ['XPS Cen X', 'XPS Cen Y', 'XPS Sam Z', 'XPS Omega']),
               ('Counts', ['Ring current', 'IDA-IC', 'IDB-IC', 'Beamstop'])
               ]

# dropdown menus put into proper, ordered list
dropdown_dict = collections.OrderedDict(dropdown_list)

# master dictionry shouold probably be read from file, but hard-coded for development convenience
master_dict = {'Timestamp': 'S:IOC:timeOfDayForm1SI',
              'XPS Cen X': 'XPSGP:m1.RBV',
              'XPS Cen Y': 'XPSGP:m2.RBV',
              'XPS Sam Z': 'XPSGP:m3.RBV',
              'XPS Omega': 'XPSGP:m4.RBV',
              'Ring current': 'S:SRcurrentAI.VAL',
              'IDA-IC': '16IDB:scaler1_cts2.A',
              'IDB-IC': '16IDB:scaler1_cts1.C',
              'Beamstop': '16IDB:scaler1_cts2.B'}

# logger list and dictionary will contain only the logged PVs and associated objects
logger_list = []
logger_dict = {}

button = Button(root, text='New PV', command=create_entry)
button.grid(row=0, column=0, padx=5)
button2 = Button(root, text='Create_PVs', command=create_pvs)
button2.grid(row=0, column=1, padx=5)
button3 = Button(root, text='Print', command=print_it)
button3.grid(row=0, column=2, padx=5)
# button4 = Button(root, text='Log', command=log_it)
# button4.grid(row=0, column=3, padx=5)
root.mainloop()