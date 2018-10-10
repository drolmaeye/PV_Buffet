from Tkinter import *
import collections
from epics import *


class CoreData:
    def __init__(self):

        self.number_of_pvs = 0
        self.line_index = 0
        self.logger_list = []
        self.logger_dict = {}


class LoggerConfig:
    def __init__(self, master):
        self.config_window = Toplevel(master)
        self.config_window.title('Data logger initialization and reconfiguration')

        # make and place primary frames
        self.frame_labels = Frame(self.config_window)
        self.frame_buttons = Frame(self.config_window)
        self.frame_pvs = Frame(self.config_window)

        self.frame_labels.pack(side='left', fill='both', expand=True)
        self.frame_buttons.pack(side='top', fill='both', expand=True)
        self.frame_pvs.pack(side='top', fill='both', expand=True)

        # create and place frame label widgets
        # create and place frame button widgets
        add_pv_button = Button(self.frame_buttons, text='Add New PV', command=self.create_entry)
        remove_pv_button = Button(self.frame_buttons, text='Remove PV', command=self.remove_entry)
        launch_logger_button = Button(self.frame_buttons, text='Launch logger window', command=self.create_pvs)

        add_pv_button.grid(row=0, column=0, padx=5, pady=5)
        remove_pv_button.grid(row=1, column=0, padx=5, pady=5)
        launch_logger_button.grid(row=2, column=0, padx=5, pady=5)

    def create_entry(self):
        MasterDropdown(self.frame_pvs)
        core.number_of_pvs += 1

    def remove_entry(self):
        print len(core.logger_list)
        core.logger_list.pop()
        print len(core.logger_list)

    def create_pvs(self):
        core.logger_dict = collections.OrderedDict(core.logger_list)
        LoggerWindow(root)
        root.deiconify()


class MasterDropdown:

    def __init__(self, master):

        self.pv_choice = StringVar()
        self.pv_choice.set('Select a PV')
        self.pv_index = core.number_of_pvs

        self.menubutton = Menubutton(master, textvariable=self.pv_choice, indicatoron=True)
        self.main_menu = Menu(self.menubutton, tearoff=False)
        self.menubutton.configure(menu=self.main_menu)

        for key in dropdown_dict.keys():
            menu = Menu(self.main_menu, tearoff=False)
            self.main_menu.add_cascade(label=key, menu=menu)
            for value in dropdown_dict[key]:
                menu.add_radiobutton(label=value, variable=self.pv_choice, value=value)

        self.menubutton.grid(row=1, column=core.number_of_pvs)
        self.pv_choice.trace('w', self.pv_append)
        core.logger_list.append(self.pv_index)

    def pv_append(self, *kargs):
        self.menubutton.configure(indicatoron=False)#, state=DISABLED)
        pv_name = self.pv_choice.get()
        pv_label = Label(text=pv_name)
        pv_value = StringVar()
        pv_object = PV(master_dict[pv_name])
        pv_object.add_callback(lambda **kwargs: pv_value.set(pv_object.value))
        pv_object.run_callbacks()
        entry = (pv_name, [pv_label, pv_value, pv_object, master_dict[pv_name]])
        core.logger_list[self.pv_index] = entry
        print core.logger_list



class LoggerWindow:
    def __init__(self, master):
        self.frame = Frame(master, bg='yellow', width=900)
        self.frame.pack(fill='both', expand=True)



        self.line_index = 1

        self.top_canvas = Canvas(self.frame, borderwidth=0, height=21, background='#ffffff')
        self.top_frame = Frame(self.top_canvas, background='#ffffff')
        self.bottom_canvas = Canvas(self.frame, borderwidth=0, background='#ffffff', highlightthickness=0)
        self.bottom_canvas.bind('<Configure>', self.on_resize)
        self.bottom_frame = Frame(self.bottom_canvas, background='#ffffff')
        self.make_headings()
        self.vsb = Scrollbar(self.frame, orient='vertical', command=self.bottom_canvas.yview)
        self.bottom_canvas.configure(yscrollcommand=self.vsb.set)
        self.hsb = Scrollbar(self.frame, orient='horizontal', command=self.special_view)
        # self.top_canvas.configure(xscrollcommand=self.hsb.set)
        self.bottom_canvas.configure(xscrollcommand=self.hsb.set)
        # ###self.vsb.grid(row=1, column=1, sticky=NS)
        # ###self.hsb.grid(row=2, column=0, sticky=EW)
        # ###self.top_canvas.grid(row=0, column=0)
        # ###self.bottom_canvas.grid(row=1, column=0)
        self.vsb.pack(side='right', fill='y')
        self.hsb.pack(side='bottom', fill='x')
        self.top_canvas.pack(side='top', fill='x', expand=True)
        self.bottom_canvas.pack(side='top', fill='both', expand=True)
        self.top_canvas.create_window((4, 4), window=self.top_frame, anchor='nw',
                                      tags='self.top_frame')
        self.bottom_canvas.create_window((4, 29), window=self.bottom_frame, anchor='nw',
                                         tags='self.bottom_frame')
        self.button4 = Button(button_frame, text='Log', command=self.log_it)
        self.button4.grid(row=0, column=3, padx=5)

    def special_view(self, *args):
        apply(self.top_canvas.xview, args)
        apply(self.bottom_canvas.xview, args)

    def make_headings(self):
        column = 0
        for keys in core.logger_dict.iterkeys():
            column_head = Label(self.top_frame, text=keys, bg='#ffffff')
            column_head.grid(row=0, column=column)
            line_head = Label(self.bottom_frame, text=keys)
            line_head.grid(row=0, column=column)
            column += 1

    def log_it(self):
        column = 0
        if not self.line_index % 2 == 0:
            line_color = 'gray64'
        else:
            line_color = '#ffffff'
        for keys in core.logger_dict.iterkeys():
            line_label = Label(self.bottom_frame, text=core.logger_dict[keys][1].get(), bg=line_color, padx=10)
            line_label.grid(row=self.line_index, column=column, sticky=W+E)
            line_label.update_idletasks()
            new_width = line_label.winfo_width()
            self.top_frame.grid_columnconfigure(index=column, minsize=new_width)
            column += 1
        self.line_index += 1
        self.bottom_canvas.configure(scrollregion=self.bottom_canvas.bbox('self.bottom_frame'))
        self.top_canvas.configure(scrollregion=self.top_canvas.bbox('self.top_frame'))
        self.bottom_canvas.yview_moveto(1.0)

    def on_resize(self, event):
        frame_width = event.width
        frame_height = event.height
        self.bottom_canvas.config(width=frame_width, height=frame_height)


def hide_config():
    config.config_window.withdraw()


def close_quit():
    # add dialog box back in and indent following code after testing period
    # ##if askyesno('Quit PV Buffet', 'Do you want to quit?'):
    root.destroy()
    root.quit()


root = Tk()
root.configure(bg='blue')
root.withdraw()




# Dropdown collected in list first to accommodate ordered dictionary
dropdown_list = [('Timestamp', ['Timestamp']),
                 ('Sample stages', ['XPS Cen X', 'XPS Cen Y', 'XPS Sam Z', 'XPS Omega']),
                 ('Counts', ['Ring current', 'IDA-IC', 'IDB-IC', 'Beamstop']),
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
core = CoreData()
config = LoggerConfig(root)
config.config_window.protocol('WM_DELETE_WINDOW', hide_config)
root.protocol('WM_DELETE_WINDOW', close_quit)
button_frame = Frame(root, bg='red')
button_frame.pack(fill='x')
pv_frame = Frame(root, bg='green')
pv_frame.pack(fill='x')
root.mainloop()
