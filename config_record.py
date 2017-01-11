__author__ = 'j.smith'

# import necessary modules
from Tkinter import *
from epics import *
import tkFont


class TableSheet:
    def __init__(self, master, title, buttontext, row=0, column=0):
        self.popup = Toplevel(master)
        self.popup.title(title)

        bigfont = tkFont.Font(size=10, weight='bold')

        # place a button on the HomeWindow
        self.button = Button(root, text=buttontext, height=2, width=14, font=bigfont, command=self.show_window)
        self.button.grid(row=row, column=column, padx=8, pady=20)

        # specify hide protocol
        self.popup.protocol('WM_DELETE_WINDOW', self.hide_window)

        # hide window on startup
        self.hide_window()

    def show_window(self):
        if not self.popup.winfo_viewable():
            # ###xtop = root.winfo_x()
            # ###ytop = root.winfo_y() + root.winfo_height() + 40
            # ###ida.popup.geometry('+%d+%d' % (xtop, ytop))
            self.popup.deiconify()

    def hide_window(self):
        self.popup.withdraw()


class MotorHeading:
    def __init__(self, master, label, color='light goldenrod'):
        self.frame = Frame(master, bg=color)
        self.frame.pack()

        self.desc_head_label = Label(self.frame, text=label, width=20, anchor='w', bg=color)
        self.rbv_head_label = Label(self.frame, text='RBV', width=10, anchor='w', bg=color)
        self.drbv_head_label = Label(self.frame, text='DRBV', width=10, anchor='w', bg=color)
        self.egu_head_label = Label(self.frame, text='EGU', width=6, anchor='w', bg=color)

        self.desc_head_label.grid(row=0, column=0, padx=5, pady=5)
        self.rbv_head_label.grid(row=0, column=1, padx=5, pady=5)
        self.drbv_head_label.grid(row=0, column=2, padx=5, pady=5)
        self.egu_head_label.grid(row=0, column=3, padx=5, pady=5)


class OneMotor:
    def __init__(self, master, motor, precision=3):
        self.frame = Frame(master)
        self.frame.pack()

        # define instance variables
        self.desc = StringVar()
        self.rbv = StringVar()
        self.drbv = StringVar()
        self.egu = StringVar()

        # create precision string
        self.p_string = '%.' + str(precision) + 'f'

        # create PVs
        self.mdesc = PV(motor + '.DESC', callback=self.update_desc)
        self.mrbv = PV(motor + '.RBV', callback=self.update_rbv)
        self.mdrbv = PV(motor + '.DRBV', callback=self.update_drbv)
        self.megu = PV(motor + '.EGU', callback=self.update_egu)

        # make display line widgets
        self.desc_label = Label(self.frame, textvariable=self.desc, width=20, anchor='w')
        self.rbv_label = Label(self.frame, textvariable=self.rbv, width=10, anchor='w', relief=SUNKEN)
        self.drbv_label = Label(self.frame, textvariable=self.drbv, width=10, anchor='w', relief=SUNKEN)
        self.egu_label = Label(self.frame, textvariable=self.egu, width=6, anchor='w')

        # place display line widgets
        self.desc_label.grid(row=0, column=0, padx=5, pady=2)
        self.rbv_label.grid(row=0, column=1, padx=5, pady=2)
        self.drbv_label.grid(row=0, column=2, padx=5, pady=2)
        self.egu_label.grid(row=0, column=3, padx=5, pady=2)

    def update_desc(self, **kwargs):
        self.desc.set(self.mdesc.value)

    def update_rbv(self, **kwargs):
        self.rbv.set(self.p_string % self.mrbv.value)

    def update_drbv(self, **kwargs):
        self.drbv.set(self.p_string % self.mdrbv.value)

    def update_egu(self, **kwargs):
        self.egu.set(self.megu.value)


class OneCounter:

    sens_list = ['1', '2', '5', '10', '20', '50', '100', '200', '500']
    unit_list = ['pA/V', 'nA/V', 'uA/V', 'mA/V']

    def __init__(self, master, hutch='16IDB:', scaler='scaler1', counts='_cts2.A', nm='.NM5', sr='A1', row=0, column=0):
        self.frame = Frame(master)
        self.frame.grid(row=row, column=column)

        # define instance variables
        self.name = StringVar()
        self.counts = IntVar()
        self.sens = StringVar()
        self.unit = StringVar()
        self.combined_unit = StringVar()

        # create PVs
        self.cname = PV(hutch + scaler + nm)
        self.ccounts = PV(hutch + scaler + counts)
        self.csens = PV(hutch + sr + 'sens_num.VAL')
        self.cunit = PV(hutch + sr + 'sens_unit.VAL')

        self.cname.add_callback(self.update_name)
        self.ccounts.add_callback(self.update_counts)
        self.csens.add_callback(self.update_sens)
        self.cunit.add_callback(self.update_unit)

        self.cname.run_callbacks()
        self.ccounts.run_callbacks()
        self.csens.run_callbacks()
        self.cunit.run_callbacks()

        # make display line
        self.name_label = Label(self.frame, textvariable=self.name, width=8, anchor='w')
        self.counts_label = Label(self.frame, textvariable=self.counts, width=6, anchor='e', relief=SUNKEN)
        self.sens_label = Label(self.frame, textvariable=self.combined_unit, width=7, anchor='e')

        self.name_label.grid(row=0, column=0, padx=4, pady=2)
        self.counts_label.grid(row=0, column=1, padx=5, pady=2)
        self.sens_label.grid(row=0, column=2, padx=5, pady=2)

    def update_name(self, **kwargs):
        self.name.set(self.cname.value)
        print 'ran it'

    def update_counts(self, **kwargs):
        self.counts.set(int(self.ccounts.value))

    def update_sens(self, **kwargs):
        self.sens.set(OneCounter.sens_list[self.csens.value])
        self.combined_unit.set(self.sens.get() + ' ' + self.unit.get())

    def update_unit(self, **kwargs):
        self.unit.set(OneCounter.unit_list[self.cunit.value])
        self.combined_unit.set(self.sens.get() + ' ' + self.unit.get())


class OneCustom:
    def __init__(self, master, prefix, suffix1, suffix2, precision=3):
        self.frame = Frame(master)
        self.frame.pack(side=LEFT)

        # create PVs
        self.pv1 = PV(prefix + suffix1, callback=self.update_pv1)
        self.pv2 = PV(prefix + suffix2, callback=self.update_pv2)

        # create precision string
        self.p_string = '%.' + str(precision) + 'f'

        # define instance variables and get initial values
        self.pv1_var = StringVar()
        self.pv2_var = StringVar()
        self.pv1_var.set(self.pv1.value)
        self.pv2_var.set(self.p_string % self.pv2.value)

        # make display line
        self.pv1_var_label = Label(self.frame, textvariable=self.pv1_var, width=20, anchor='w')
        self.pv2_var_label = Label(self.frame, textvariable=self.pv2_var, width=10, anchor='w', relief=SUNKEN)

        self.pv1_var_label.grid(row=0, column=0, padx=5, pady=2, sticky='W')
        self.pv2_var_label.grid(row=0, column=1, padx=5, pady=2)

    def update_pv1(self, **kwargs):
        self.pv1_var.set(self.pv1.value)

    def update_pv2(self, **kwargs):
        self.pv2_var.set(self.p_string % self.pv2.value)


class TimeStamp:
    def __init__(self, master, padx=0, pady=0):
        self.frame = Frame(master, bg='CadetBlue3')
        self.frame.pack()

        # define instance variables
        self.time_stamp = StringVar()

        # timestamp PV
        self.ioc_time = PV('S:IOC:timeOfDayForm1SI') #, callback=self.update_time)
        self.ioc_time.add_callback(self.update_time)

        # make display label
        self.time_stamp_label = Label(self.frame, textvariable=self.time_stamp, width=46, bg='CadetBlue3')
        self.time_stamp_label.grid(row=0, column=0, padx=padx, pady=pady)

    def update_time(self, **kwargs):
        self.time_stamp.set(self.ioc_time.value)


def close_quit():
    # add dialog box back in and indent following code after testing period
    # ##if askyesno('Quit Diptera', 'Do you want to quit?'):
    root.destroy()
    root.quit()


root = Tk()
root.title('Table Records (January 2017 Configuration)')
# root.geometry('300x300')

# create sheets
ida = TableSheet(root, 'IDA', 'IDA', 0, 0)
idb_gp = TableSheet(root, 'IDB General Purpose Table', 'IDB-GP', 0, 1)
idb_lh = TableSheet(root, 'IDB Laser Heating Table', 'IDB-LH', 0, 2)


# ##########################################
# ida start
# ##########################################
frameLeftIDA = Frame(ida.popup)
frameLeftIDA.grid(row=0, column=0)
frameBDCM1IDA = Frame(frameLeftIDA, bd=5, relief=RIDGE)
frameBDCM1IDA.grid(row=0, column=0)
frameBDCM2IDA = Frame(frameLeftIDA, bd=5, relief=RIDGE)
frameBDCM2IDA.grid(row=1, column=0)
frameTimeStampIDA = Frame(frameLeftIDA, bd=5, relief=RIDGE)
frameTimeStampIDA.grid(row=2, column=0)

frameRightIDA = Frame(ida.popup)
frameRightIDA.grid(row=0, column=1)
frameSlitsIDA = Frame(frameRightIDA, bd=5, relief=RIDGE)
frameSlitsIDA.grid(row=0, column=0)
frameDiagnosticIDA = Frame(frameRightIDA, bd=5, relief=RIDGE)
frameDiagnosticIDA.grid(row=1, column=0)
frameCounterIDA = Frame(frameRightIDA, bd=5, relief=RIDGE)
frameCounterIDA.grid(row=2, column=0)

# objects for ida
bdcm1 = MotorHeading(frameBDCM1IDA, 'BDCM-1')
bdcm1_bragg1 = OneMotor(frameBDCM1IDA, '16IDA:m29', 6)
bdcm1_tilt = OneMotor(frameBDCM1IDA, '16IDA:m31', 3)
bdcm1_xtal_z = OneMotor(frameBDCM1IDA, '16IDA:m30', 3)
bdcm1_piezo = OneCustom(frameBDCM1IDA, '16IDA:DAC1_2', '.DESC', '.VAL', 3)

bdcm2 = MotorHeading(frameBDCM2IDA, 'BDCM-2')
bdcm2_x = OneMotor(frameBDCM2IDA, '16IDA:m33', 3)
bdcm2_y = OneMotor(frameBDCM2IDA, '16IDA:m22', 3)
bdcm2_bragg = OneMotor(frameBDCM2IDA, '16IDA:m32', 6)
bdcm2_tilt = OneMotor(frameBDCM2IDA, '16IDA:m23', 3)
bdcm2_xtal_z = OneMotor(frameBDCM2IDA, '16IDA:m24', 3)

ida_time = TimeStamp(frameTimeStampIDA, 29, 3)

ida_slits = MotorHeading(frameSlitsIDA, 'FOE Slits')
ida_slits_vsize = OneMotor(frameSlitsIDA, '16IDA:m9', 3)
ida_slits_vpos = OneMotor(frameSlitsIDA, '16IDA:m10', 3)
ida_slits_hsize = OneMotor(frameSlitsIDA, '16IDA:m11', 3)
ida_slits_hpos = OneMotor(frameSlitsIDA, '16IDA:m12', 3)

bdcm_diagnostic = MotorHeading(frameDiagnosticIDA, 'BDCM Diagnostic')
bdcm_diagnostic_y = OneMotor(frameDiagnosticIDA, '16IDA:m6', 3)
bdcm_diagnostic_vsize = OneMotor(frameDiagnosticIDA, '16IDA:m18', 3)
bdcm_diagnostic_vpos = OneMotor(frameDiagnosticIDA, '16IDA:m19', 3)
bdcm_diagnostic_hsize = OneMotor(frameDiagnosticIDA, '16IDA:m20', 3)
bdcm_diagnostic_hpos = OneMotor(frameDiagnosticIDA, '16IDA:m21', 3)

ida_counter_ida_ic = OneCounter(frameCounterIDA, '16IDB:', 'scaler1', '_cts2.A', '.NM5', sr='A1', row=0, column=0)
ida_counter_idb_ic = OneCounter(frameCounterIDA, '16IDB:', 'scaler1', '_cts1.C', '.NM3', sr='A3', row=1, column=0)
ida_counter_diode = OneCounter(frameCounterIDA, '16IDB:', 'scaler1', '_cts1.D', '.NM4', sr='A4', row=0, column=1)
ida_counter_beamstop = OneCounter(frameCounterIDA, '16IDB:', 'scaler1', '_cts2.B', '.NM6', sr='A5', row=1, column=1)

# ##########################################
# idb_gp start
# ##########################################
frameLeftGP = Frame(idb_gp.popup)
frameLeftGP.grid(row=0, column=0)
frameXPSGP = Frame(frameLeftGP, bd=5, relief=RIDGE)
frameXPSGP.grid(row=0, column=0)
frameHighLoadGP = Frame(frameLeftGP, bd=5, relief=RIDGE)
frameHighLoadGP.grid(row=1, column=0)
frameCommonGP = Frame(frameLeftGP, bd=5, relief=RIDGE)
frameCommonGP.grid(row=2, column=0)
frameDetectorGP = Frame(frameLeftGP, bd=5, relief=RIDGE)
frameDetectorGP.grid(row=3, column=0)
frameLKBPinholeGP = Frame(frameLeftGP, bd=5, relief=RIDGE)
frameLKBPinholeGP.grid(row=4, column=0)
frameSKBPinholeGP = Frame(frameLeftGP, bd=5, relief=RIDGE)
frameSKBPinholeGP.grid(row=5, column=0)
frameBeamstopGP = Frame(frameLeftGP, bd=5, relief=RIDGE)
frameBeamstopGP.grid(row=6, column=0)
frameSlitsGP = Frame(frameLeftGP, bd=5, relief=RIDGE)
frameSlitsGP.grid(row=7, column=0)
frameTimeStampGP = Frame(frameLeftGP, bd=5, relief=RIDGE)
frameTimeStampGP.grid(row=8, column=0)

frameRightGP = Frame(idb_gp.popup)
frameRightGP.grid(row=0, column=1)
frameLKBXGP = Frame(frameRightGP, bd=5, relief=RIDGE)
frameLKBXGP.grid(row=0, column=1)
frameVLKBGP = Frame(frameRightGP, bd=5, relief=RIDGE)
frameVLKBGP.grid(row=1, column=1)
frameHLKBGP = Frame(frameRightGP, bd=5, relief=RIDGE)
frameHLKBGP.grid(row=2, column=1)
frameVSKBGP = Frame(frameRightGP, bd=5, relief=RIDGE)
frameVSKBGP.grid(row=3, column=1)
frameHSKBGP = Frame(frameRightGP, bd=5, relief=RIDGE)
frameHSKBGP.grid(row=4, column=1)
frameCounterGP = Frame(frameRightGP, bd=5, relief=RIDGE)
frameCounterGP.grid(row=5, column=1)

# objects to be places in left frame
high_precision = MotorHeading(frameXPSGP, 'High precision sample')
xps_cen_x = OneMotor(frameXPSGP, 'XPSGP:m1', 4)
xps_cen_y = OneMotor(frameXPSGP, 'XPSGP:m2', 4)
xps_sam_z = OneMotor(frameXPSGP, 'XPSGP:m3', 4)
xps_omega = OneMotor(frameXPSGP, 'XPSGP:m4', 3)

high_load = MotorHeading(frameHighLoadGP, 'High load sample')
cen_x = OneMotor(frameHighLoadGP, '16IDB:m31', 3)
cen_y = OneMotor(frameHighLoadGP, '16IDB:m32', 3)

shared_sample = MotorHeading(frameCommonGP, 'Shared sample')
sam_z = OneMotor(frameCommonGP, '16IDB:m5', 3)
gp_omega = OneMotor(frameCommonGP, 'XPSGP:m5', 3)
sam_y = OneMotor(frameCommonGP, '16IDB:m4', 3)

detector = MotorHeading(frameDetectorGP, 'Detector')
detector_x = OneMotor(frameDetectorGP, '16IDB:m7', 3)
detector_y = OneMotor(frameDetectorGP, '16IDB:m6', 3)

lkb_pinhole = MotorHeading(frameLKBPinholeGP, 'LKB Pinhole')
lkb_pinhole_x = OneMotor(frameLKBPinholeGP, '16IDB:m2', 3)
lkb_pinhole_y = OneMotor(frameLKBPinholeGP, '16IDB:m19', 3)
lkb_pinhole_z = OneMotor(frameLKBPinholeGP, '16IDB:m24', 3)
lkb_pinhole_pt = OneMotor(frameLKBPinholeGP, '16IDB:m26', 3)
lkb_pinhole_yw = OneMotor(frameLKBPinholeGP, '16IDB:m74', 3)

skb_pinhole = MotorHeading(frameSKBPinholeGP, 'SKB Pinhole')
skb_pinhole_x = OneMotor(frameSKBPinholeGP, '16IDB:m16', 3)
skb_pinhole_y = OneMotor(frameSKBPinholeGP, '16IDB:m17', 3)
skb_pinhole_z = OneMotor(frameSKBPinholeGP, '16IDB:m18', 3)
skb_pinhole_pt = OneMotor(frameSKBPinholeGP, '16IDB:m36', 3)
skb_pinhole_yw = OneMotor(frameSKBPinholeGP, '16IDB:m66', 3)

beamstop = MotorHeading(frameBeamstopGP, 'Beamstop')
beamstop_y = OneMotor(frameBeamstopGP, '16IDB:m34', 3)
beamstop_z = OneMotor(frameBeamstopGP, '16IDB:m35', 3)

idb_slits = MotorHeading(frameSlitsGP, 'IDB Slits')
idb_hpos = OneMotor(frameSlitsGP, '16IDB:m21', 3)
idb_hsize = OneMotor(frameSlitsGP, '16IDB:m23', 3)
idb_vpos = OneMotor(frameSlitsGP, '16IDB:m22', 3)
idb_vsize = OneMotor(frameSlitsGP, '16IDB:m20', 3)

idb_gp_time = TimeStamp(frameTimeStampGP, 29, 3)

# objects to placed in right frame
lkb_mirror_x = MotorHeading(frameLKBXGP, 'LKB Mirror X')
lkb_x_position = OneMotor(frameLKBXGP, '16IDB:m1', 3)

vlkb_mirror = MotorHeading(frameVLKBGP, 'Vertical LKB Mirror')
vlkb_stripe = OneMotor(frameVLKBGP, '16IDB:m15', 3)
vlkb_usz = OneMotor(frameVLKBGP, '16IDB:m41', 3)
vlkb_dsf = OneMotor(frameVLKBGP, '16IDB:m59', 3)
vlkb_usf = OneMotor(frameVLKBGP, '16IDB:m43', 3)
vlkb_dsz = OneMotor(frameVLKBGP, '16IDB:m42', 3)
vlkb_pitch = OneMotor(frameVLKBGP, '16IDB:pm18', 3)
vlkb_height = OneMotor(frameVLKBGP, '16IDB:pm17', 3)
vlkb_curvature = OneMotor(frameVLKBGP, '16IDB:pm15', 3)
vlkb_ellipticity = OneMotor(frameVLKBGP, '16IDB:pm16', 3)

hlkb_mirror = MotorHeading(frameHLKBGP, 'Horizontal LKB Mirror')
hlkb_stripe = OneMotor(frameHLKBGP, '16IDB:m14', 3)
hlkb_usz = OneMotor(frameHLKBGP, '16IDB:m25', 3)
hlkb_dsf = OneMotor(frameHLKBGP, '16IDB:m29', 3)
hlkb_usf = OneMotor(frameHLKBGP, '16IDB:m28', 3)
hlkb_dsz = OneMotor(frameHLKBGP, '16IDB:m27', 3)
hlkb_pitch = OneMotor(frameHLKBGP, '16IDB:pm22', 3)
hlkb_height = OneMotor(frameHLKBGP, '16IDB:pm21', 3)
hlkb_curvature = OneMotor(frameHLKBGP, '16IDB:pm19', 3)
hlkb_ellipticity = OneMotor(frameHLKBGP, '16IDB:pm20', 3)

vskb_mirror = MotorHeading(frameVSKBGP, 'Vertical SKB Mirror')
vskb_z = OneMotor(frameVSKBGP, '16IDB:m81', 1)
vskb_pitch = OneMotor(frameVSKBGP, '16IDB:m82')
vskb_usf = OneMotor(frameVSKBGP, '16IDB:m83', 1)
vskb_dsf = OneMotor(frameVSKBGP, '16IDB:m84', 1)
vskb_curvature = OneMotor(frameVSKBGP, '16IDB:pm5', 1)
vskb_ellipticity = OneMotor(frameVSKBGP, '16IDB:pm6', 1)

hskb_mirror = MotorHeading(frameHSKBGP, 'Horizontal SKB Mirror')
hskb_z = OneMotor(frameHSKBGP, '16IDB:m85', 1)
hskb_pitch = OneMotor(frameHSKBGP, '16IDB:m86')
hskb_usf = OneMotor(frameHSKBGP, '16IDB:m87', 1)
hskb_dsf = OneMotor(frameHSKBGP, '16IDB:m88', 1)
hskb_curvature = OneMotor(frameHSKBGP, '16IDB:pm3', 1)
hskb_ellipticity = OneMotor(frameHSKBGP, '16IDB:pm4', 1)

counter_ida_ic = OneCounter(frameCounterGP, '16IDB:', 'scaler1', '_cts2.A', '.NM5', sr='A1', row=0, column=0)
counter_idb_ic = OneCounter(frameCounterGP, '16IDB:', 'scaler1', '_cts1.C', '.NM3', sr='A3', row=1, column=0)
counter_diode = OneCounter(frameCounterGP, '16IDB:', 'scaler1', '_cts1.D', '.NM4', sr='A4', row=0, column=1)
counter_beamstop = OneCounter(frameCounterGP, '16IDB:', 'scaler1', '_cts2.B', '.NM6', sr='A5', row=1, column=1)

# ###counter_ida_ic.cname.run_callbacks()
# ###counter_ida_ic.ccounts.run_callbacks()
# ###counter_ida_ic.csens.run_callbacks()
# ###counter_ida_ic.cunit.run_callbacks()

# closing protocol
root.protocol('WM_DELETE_WINDOW', close_quit)

root.mainloop()
