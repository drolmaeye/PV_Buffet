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


class Source:
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.grid(row=0, column=0)

        # define instance variables
        self.gap = StringVar()
        self.harmonic = IntVar()
        self.current = StringVar()

        # create PVs, add callbacks, and run callbacks
        self.sgap = PV('ID16ds:Gap.VAL')
        self.sharmonic = PV('ID16:HarmonicValue.VAL')
        self.scurrent = PV('S:SRcurrentAI.VAL')

        self.sgap.add_callback(self.update_gap)
        self.sharmonic.add_callback(self.update_harmonic)
        self.scurrent.add_callback(self.update_current)

        self.sgap.run_callbacks()
        self.sharmonic.run_callbacks()
        self.scurrent.run_callbacks()

        # make display line widgets
        self.gap_label1 = Label(self.frame, text='Undulator gap', width=16, anchor='e')
        self.gap_label2 = Label(self.frame, textvariable=self.gap, width=6, anchor='e', relief=SUNKEN)
        self.gap_label3 = Label(self.frame, text='mm', anchor='w')
        self.harmonic_label1 = Label(self.frame, text='Harmonic', width=10, anchor='e')
        self.harmonic_label2 = Label(self.frame, textvariable=self.harmonic, width=4, anchor='e', relief=SUNKEN)
        self.current_label1 = Label(self.frame, text='Storage ring current', width=16, anchor='e')
        self.current_label2 = Label(self.frame, textvariable=self.current, width=6, anchor='e', relief=SUNKEN)
        self.current_label3 = Label(self.frame, text='mA', width=8, anchor='w')

        # place display line widgets
        self.gap_label1.grid(row=0, column=0, padx=10, pady=10)
        self.gap_label2.grid(row=0, column=1)
        self.gap_label3.grid(row=0, column=2)
        # ###self.harmonic_label1.grid(row=0, column=3, padx=10, pady=10)
        # ###self.harmonic_label2.grid(row=0, column=4)
        self.current_label1.grid(row=0, column=5, padx=10, pady=10)
        self.current_label2.grid(row=0, column=6)
        self.current_label3.grid(row=0, column=7)

    def update_gap(self, **kwargs):
        self.gap.set('%.3f' % self.sgap.value)

    def update_harmonic(self, **kwargs):
        self.harmonic.set(int(self.sharmonic.value))

    def update_current(self, **kwargs):
        self.current.set('%.1f' % self.scurrent.value)


class MotorHeading:
    def __init__(self, master, label, color='light goldenrod'):
        self.frame = Frame(master, bg=color)
        self.frame.pack()

        # create header labels
        self.desc_head_label = Label(self.frame, text=label, width=20, anchor='w', bg=color)
        self.rbv_head_label = Label(self.frame, text='RBV', width=10, anchor='w', bg=color)
        self.drbv_head_label = Label(self.frame, text='DRBV', width=10, anchor='w', bg=color)
        self.egu_head_label = Label(self.frame, text='EGU', width=6, anchor='w', bg=color)

        # place label widgets
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

        # create PVs, add callbacks, and run callbacks
        self.mdesc = PV(motor + '.DESC')
        self.mrbv = PV(motor + '.RBV')
        self.mdrbv = PV(motor + '.DRBV')
        self.megu = PV(motor + '.EGU')

        self.mdesc.add_callback(self.update_desc)
        self.mrbv.add_callback(self.update_rbv)
        self.mdrbv.add_callback(self.update_drbv)
        self.megu.add_callback(self.update_egu)

        self.mdesc.run_callbacks()
        self.mrbv.run_callbacks()
        self.mdrbv.run_callbacks()
        self.megu.run_callbacks()

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

        # create PVs, add callbacks, and run callbacks
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

        # make display line widgets
        self.name_label = Label(self.frame, textvariable=self.name, width=8, anchor='w')
        self.counts_label = Label(self.frame, textvariable=self.counts, width=6, anchor='e', relief=SUNKEN)
        self.sens_label = Label(self.frame, textvariable=self.combined_unit, width=7, anchor='e')

        # place display line widgets
        self.name_label.grid(row=0, column=0, padx=4, pady=2)
        self.counts_label.grid(row=0, column=1, padx=5, pady=2)
        self.sens_label.grid(row=0, column=2, padx=5, pady=2)

    def update_name(self, **kwargs):
        self.name.set(self.cname.value)

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

        # define instance variables and get initial values
        self.pv1_var = StringVar()
        self.pv2_var = StringVar()

        # create precision string
        self.p_string = '%.' + str(precision) + 'f'

        # create PVs, add callbacks, and run callbacks
        self.pv1 = PV(prefix + suffix1)
        self.pv2 = PV(prefix + suffix2)

        self.pv1.add_callback(self.update_pv1)
        self.pv2.add_callback(self.update_pv2)

        self.pv1.run_callbacks()
        self.pv2.run_callbacks()

        # create precision string
        self.p_string = '%.' + str(precision) + 'f'

        # make display line
        self.pv1_var_label = Label(self.frame, textvariable=self.pv1_var, width=20, anchor='w')
        self.pv2_var_label = Label(self.frame, textvariable=self.pv2_var, width=10, anchor='w', relief=SUNKEN)

        # place display line widgets
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
        self.ioc_time = PV('S:IOC:timeOfDayForm1SI')
        self.ioc_time.add_callback(self.update_time)
        self.ioc_time.run_callbacks()

        # make and place display label
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
frameTopIDA = Frame(ida.popup)
frameTopIDA.grid(row=0, column=0, columnspan=2)

frameLeftIDA = Frame(ida.popup)
frameLeftIDA.grid(row=1, column=0)
frameBDCM1IDA = Frame(frameLeftIDA, bd=5, relief=RIDGE)
frameBDCM1IDA.grid(row=0, column=0)
frameBDCM2IDA = Frame(frameLeftIDA, bd=5, relief=RIDGE)
frameBDCM2IDA.grid(row=1, column=0)
frameTimeStampIDA = Frame(frameLeftIDA, bd=5, relief=RIDGE)
frameTimeStampIDA.grid(row=2, column=0)

frameRightIDA = Frame(ida.popup)
frameRightIDA.grid(row=1, column=1)
frameSlitsIDA = Frame(frameRightIDA, bd=5, relief=RIDGE)
frameSlitsIDA.grid(row=0, column=0)
frameDiagnosticIDA = Frame(frameRightIDA, bd=5, relief=RIDGE)
frameDiagnosticIDA.grid(row=1, column=0)
frameCounterIDA = Frame(frameRightIDA, bd=5, relief=RIDGE)
frameCounterIDA.grid(row=2, column=0)

# objects for ida
ida_ring = Source(frameTopIDA)

ida_bdcm1 = MotorHeading(frameBDCM1IDA, 'BDCM-1')
ida_bdcm1_bragg1 = OneMotor(frameBDCM1IDA, '16IDA:m29', 6)
ida_bdcm1_tilt = OneMotor(frameBDCM1IDA, '16IDA:m31', 3)
ida_bdcm1_xtal_z = OneMotor(frameBDCM1IDA, '16IDA:m30', 3)
ida_bdcm1_piezo = OneCustom(frameBDCM1IDA, '16IDA:DAC1_2', '.DESC', '.VAL', 3)

ida_bdcm2 = MotorHeading(frameBDCM2IDA, 'BDCM-2')
ida_bdcm2_x = OneMotor(frameBDCM2IDA, '16IDA:m33', 3)
ida_bdcm2_y = OneMotor(frameBDCM2IDA, '16IDA:m22', 3)
ida_bdcm2_bragg = OneMotor(frameBDCM2IDA, '16IDA:m32', 6)
ida_bdcm2_tilt = OneMotor(frameBDCM2IDA, '16IDA:m23', 3)
ida_bdcm2_xtal_z = OneMotor(frameBDCM2IDA, '16IDA:m24', 3)

ida_time = TimeStamp(frameTimeStampIDA, 29, 14)

ida_slits = MotorHeading(frameSlitsIDA, 'FOE Slits')
ida_slits_vsize = OneMotor(frameSlitsIDA, '16IDA:m9', 3)
ida_slits_vpos = OneMotor(frameSlitsIDA, '16IDA:m10', 3)
ida_slits_hsize = OneMotor(frameSlitsIDA, '16IDA:m11', 3)
ida_slits_hpos = OneMotor(frameSlitsIDA, '16IDA:m12', 3)

ida_bdcm_diagnostic = MotorHeading(frameDiagnosticIDA, 'BDCM Diagnostic')
ida_bdcm_diagnostic_y = OneMotor(frameDiagnosticIDA, '16IDA:m6', 3)
ida_bdcm_diagnostic_vsize = OneMotor(frameDiagnosticIDA, '16IDA:m18', 3)
ida_bdcm_diagnostic_vpos = OneMotor(frameDiagnosticIDA, '16IDA:m19', 3)
ida_bdcm_diagnostic_hsize = OneMotor(frameDiagnosticIDA, '16IDA:m20', 3)
ida_bdcm_diagnostic_hpos = OneMotor(frameDiagnosticIDA, '16IDA:m21', 3)

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
# frameCommonGP = Frame(frameLeftGP, bd=5, relief=RIDGE)
# frameCommonGP.grid(row=2, column=0)
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
# ###gp_high_precision = MotorHeading(frameXPSGP, 'High precision sample')
# ###gp_xps_cen_x = OneMotor(frameXPSGP, 'XPSGP:m1', 4)
# ###gp_xps_cen_y = OneMotor(frameXPSGP, 'XPSGP:m2', 4)
# ###gp_xps_sam_z = OneMotor(frameXPSGP, 'XPSGP:m3', 4)
# ###gp_xps_omega = OneMotor(frameXPSGP, 'XPSGP:m4', 3)
# ###
# ###gp_high_load = MotorHeading(frameHighLoadGP, 'High load sample')
# ###gp_cen_x = OneMotor(frameHighLoadGP, '16IDB:m31', 3)
# ###gp_cen_y = OneMotor(frameHighLoadGP, '16IDB:m32', 3)
# ###
# ###gp_shared_sample = MotorHeading(frameCommonGP, 'Shared sample')
# ###gp_sam_z = OneMotor(frameCommonGP, '16IDB:m5', 3)
# ###gp_gp_omega = OneMotor(frameCommonGP, 'XPSGP:m5', 3)
# ###gp_sam_y = OneMotor(frameCommonGP, '16IDB:m4', 3)

gp_high_precision = MotorHeading(frameXPSGP, 'High precision sample')
gp_small_x = OneMotor(frameXPSGP, 'XPSGP:m1', 4)
gp_small_y = OneMotor(frameXPSGP, 'XPSGP:m2', 4)
gp_hex_z = OneMotor(frameXPSGP, '16HEXGP:m3', 4)
gp_small_w = OneMotor(frameXPSGP, 'XPSGP:m3', 3)
gp_base_y = OneMotor(frameXPSGP, 'XPSGP:m5', 3)

gp_high_load = MotorHeading(frameHighLoadGP, 'High load sample')
gp_hex_x = OneMotor(frameHighLoadGP, '16HEXGP:m1', 4)
gp_hex_y = OneMotor(frameHighLoadGP, '16HEXGP:m2', 4)
gp_hex_z = OneMotor(frameHighLoadGP, '16HEXGP:m3', 4)
gp_large_w = OneMotor(frameHighLoadGP, 'XPSGP:m4', 3)
gp_base_y = OneMotor(frameHighLoadGP, 'XPSGP:m5', 3)

gp_detector = MotorHeading(frameDetectorGP, 'Detector')
gp_detector_x = OneMotor(frameDetectorGP, '16IDB:m7', 3)
gp_detector_y = OneMotor(frameDetectorGP, '16IDB:m6', 3)

gp_lkb_pinhole = MotorHeading(frameLKBPinholeGP, 'LKB Pinhole')
gp_lkb_pinhole_x = OneMotor(frameLKBPinholeGP, '16IDB:m2', 3)
gp_lkb_pinhole_y = OneMotor(frameLKBPinholeGP, '16IDB:m19', 3)
gp_lkb_pinhole_z = OneMotor(frameLKBPinholeGP, '16IDB:m24', 3)
gp_lkb_pinhole_pt = OneMotor(frameLKBPinholeGP, '16IDB:m26', 3)
gp_lkb_pinhole_yw = OneMotor(frameLKBPinholeGP, '16IDB:m74', 3)

gp_skb_pinhole = MotorHeading(frameSKBPinholeGP, 'SKB Pinhole')
gp_skb_pinhole_x = OneMotor(frameSKBPinholeGP, '16IDB:m16', 3)
gp_skb_pinhole_y = OneMotor(frameSKBPinholeGP, '16IDB:m17', 3)
gp_skb_pinhole_z = OneMotor(frameSKBPinholeGP, '16IDB:m18', 3)
gp_skb_pinhole_pt = OneMotor(frameSKBPinholeGP, '16IDB:m36', 3)
gp_skb_pinhole_yw = OneMotor(frameSKBPinholeGP, '16IDB:m66', 3)

gp_beamstop = MotorHeading(frameBeamstopGP, 'Beamstop')
gp_beamstop_y = OneMotor(frameBeamstopGP, '16IDB:m34', 3)
gp_beamstop_z = OneMotor(frameBeamstopGP, '16IDB:m35', 3)

gp_idb_slits = MotorHeading(frameSlitsGP, 'IDB Slits')
gp_idb_hpos = OneMotor(frameSlitsGP, '16IDB:m21', 3)
gp_idb_hsize = OneMotor(frameSlitsGP, '16IDB:m23', 3)
gp_idb_vpos = OneMotor(frameSlitsGP, '16IDB:m22', 3)
gp_idb_vsize = OneMotor(frameSlitsGP, '16IDB:m20', 3)

idb_gp_time = TimeStamp(frameTimeStampGP, 29, 3)

# objects to placed in right frame
gp_lkb_mirror_x = MotorHeading(frameLKBXGP, 'LKB Mirror X')
gp_lkb_x_position = OneMotor(frameLKBXGP, '16IDB:m1', 3)

gp_vlkb_mirror = MotorHeading(frameVLKBGP, 'Vertical LKB Mirror')
gp_vlkb_stripe = OneMotor(frameVLKBGP, '16IDB:m15', 3)
gp_vlkb_usz = OneMotor(frameVLKBGP, '16IDB:m41', 3)
gp_vlkb_dsf = OneMotor(frameVLKBGP, '16IDB:m59', 3)
gp_vlkb_usf = OneMotor(frameVLKBGP, '16IDB:m43', 3)
gp_vlkb_dsz = OneMotor(frameVLKBGP, '16IDB:m42', 3)
gp_vlkb_pitch = OneMotor(frameVLKBGP, '16IDB:pm18', 3)
gp_vlkb_height = OneMotor(frameVLKBGP, '16IDB:pm17', 3)
gp_vlkb_curvature = OneMotor(frameVLKBGP, '16IDB:pm15', 3)
gp_vlkb_ellipticity = OneMotor(frameVLKBGP, '16IDB:pm16', 3)

gp_hlkb_mirror = MotorHeading(frameHLKBGP, 'Horizontal LKB Mirror')
gp_hlkb_stripe = OneMotor(frameHLKBGP, '16IDB:m14', 3)
gp_hlkb_usz = OneMotor(frameHLKBGP, '16IDB:m25', 3)
gp_hlkb_dsf = OneMotor(frameHLKBGP, '16IDB:m29', 3)
gp_hlkb_usf = OneMotor(frameHLKBGP, '16IDB:m28', 3)
gp_hlkb_dsz = OneMotor(frameHLKBGP, '16IDB:m27', 3)
gp_hlkb_pitch = OneMotor(frameHLKBGP, '16IDB:pm22', 3)
gp_hlkb_height = OneMotor(frameHLKBGP, '16IDB:pm21', 3)
gp_hlkb_curvature = OneMotor(frameHLKBGP, '16IDB:pm19', 3)
gp_hlkb_ellipticity = OneMotor(frameHLKBGP, '16IDB:pm20', 3)

gp_vskb_mirror = MotorHeading(frameVSKBGP, 'Vertical SKB Mirror')
gp_vskb_z = OneMotor(frameVSKBGP, '16IDB:m81', 1)
gp_vskb_pitch = OneMotor(frameVSKBGP, '16IDB:m82')
gp_vskb_usf = OneMotor(frameVSKBGP, '16IDB:m83', 1)
gp_vskb_dsf = OneMotor(frameVSKBGP, '16IDB:m84', 1)
gp_vskb_curvature = OneMotor(frameVSKBGP, '16IDB:pm5', 1)
gp_vskb_ellipticity = OneMotor(frameVSKBGP, '16IDB:pm6', 1)

gp_hskb_mirror = MotorHeading(frameHSKBGP, 'Horizontal SKB Mirror')
gp_hskb_z = OneMotor(frameHSKBGP, '16IDB:m85', 1)
gp_hskb_pitch = OneMotor(frameHSKBGP, '16IDB:m86')
gp_hskb_usf = OneMotor(frameHSKBGP, '16IDB:m87', 1)
gp_hskb_dsf = OneMotor(frameHSKBGP, '16IDB:m88', 1)
gp_hskb_curvature = OneMotor(frameHSKBGP, '16IDB:pm3', 1)
gp_hskb_ellipticity = OneMotor(frameHSKBGP, '16IDB:pm4', 1)

gp_counter_ida_ic = OneCounter(frameCounterGP, '16IDB:', 'scaler1', '_cts2.A', '.NM5', sr='A1', row=0, column=0)
gp_counter_idb_ic = OneCounter(frameCounterGP, '16IDB:', 'scaler1', '_cts1.C', '.NM3', sr='A3', row=1, column=0)
gp_counter_diode = OneCounter(frameCounterGP, '16IDB:', 'scaler1', '_cts1.D', '.NM4', sr='A4', row=0, column=1)
gp_counter_beamstop = OneCounter(frameCounterGP, '16IDB:', 'scaler1', '_cts2.B', '.NM6', sr='A5', row=1, column=1)

# ##########################################
# idb_lh start
# ##########################################
frameLeftLH = Frame(idb_lh.popup)
frameLeftLH.grid(row=0, column=0)
frameXPSLH = Frame(frameLeftLH, bd=5, relief=RIDGE)
frameXPSLH.grid(row=0, column=0)
frameTableLH = Frame(frameLeftLH, bd=5, relief=RIDGE)
frameTableLH.grid(row=1, column=0)
frameDetectorLH = Frame(frameLeftLH, bd=5, relief=RIDGE)
frameDetectorLH.grid(row=2, column=0)
frameLKBPinholeLH = Frame(frameLeftLH, bd=5, relief=RIDGE)
frameLKBPinholeLH.grid(row=3, column=0)
frameSKBPinholeLH = Frame(frameLeftLH, bd=5, relief=RIDGE)
frameSKBPinholeLH.grid(row=4, column=0)
frameBeamstopLH = Frame(frameLeftLH, bd=5, relief=RIDGE)
frameBeamstopLH.grid(row=5, column=0)
frameSlitsLH = Frame(frameLeftLH, bd=5, relief=RIDGE)
frameSlitsLH.grid(row=6, column=0)

frameRightLH = Frame(idb_lh.popup)
frameRightLH.grid(row=0, column=1)
frameVLKBLH = Frame(frameRightLH, bd=5, relief=RIDGE)
frameVLKBLH.grid(row=0, column=0)
frameHLKBLH = Frame(frameRightLH, bd=5, relief=RIDGE)
frameHLKBLH.grid(row=1, column=0)
frameVSKBLH = Frame(frameRightLH, bd=5, relief=RIDGE)
frameVSKBLH.grid(row=2, column=0)
frameHSKBLH = Frame(frameRightLH, bd=5, relief=RIDGE)
frameHSKBLH.grid(row=3, column=0)
frameCounterLH = Frame(frameRightLH, bd=5, relief=RIDGE)
frameCounterLH.grid(row=4, column=0)
frameTimeStampLH = Frame(frameRightLH, bd=5, relief=RIDGE)
frameTimeStampLH.grid(row=7, column=0)

# objects to be places in left frame
lh_high_precision = MotorHeading(frameXPSLH, 'High precision sample')
lh_cen_x = OneMotor(frameXPSLH, 'XPSLH:m1', 4)
lh_cen_y = OneMotor(frameXPSLH, 'XPSLH:m2', 4)
lh_sam_z = OneMotor(frameXPSLH, 'XPSLH:m3', 4)
lh_omega = OneMotor(frameXPSLH, 'XPSLH:m4', 3)
lh_sam_y = OneMotor(frameXPSLH, '16IDB:m10', 3)

lh_table = MotorHeading(frameTableLH, 'Optical Table')
lh_table_y = OneMotor(frameTableLH, '16IDB:m37', 3)
lh_table_z = OneMotor(frameTableLH, '16IDB:m8', 3)

lh_detector = MotorHeading(frameDetectorLH, 'Detector')
lh_detector_x = OneMotor(frameDetectorLH, '16IDB:m12', 3)
lh_detector_y = OneMotor(frameDetectorLH, '16IDB:m13', 3)

lh_lkb_pinhole = MotorHeading(frameLKBPinholeLH, 'LKB Pinhole')
lh_lkb_pinhole_x = OneMotor(frameLKBPinholeLH, '16IDB:m61', 3)
lh_lkb_pinhole_y = OneMotor(frameLKBPinholeLH, '16IDB:m62', 3)
lh_lkb_pinhole_z = OneMotor(frameLKBPinholeLH, '16IDB:m63', 3)
lh_lkb_pinhole_pt = OneMotor(frameLKBPinholeLH, '16IDB:m64', 3)
lh_lkb_pinhole_yw = OneMotor(frameLKBPinholeLH, '16IDB:m65', 3)

lh_skb_pinhole = MotorHeading(frameSKBPinholeLH, 'SKB Pinhole')
lh_skb_pinhole_x = OneMotor(frameSKBPinholeLH, '16IDB:m16', 3)
lh_skb_pinhole_y = OneMotor(frameSKBPinholeLH, '16IDB:m17', 3)
lh_skb_pinhole_z = OneMotor(frameSKBPinholeLH, '16IDB:m18', 3)
lh_skb_pinhole_pt = OneMotor(frameSKBPinholeLH, '16IDB:m36', 3)
lh_skb_pinhole_yw = OneMotor(frameSKBPinholeLH, '16IDB:m66', 3)

lh_beamstop = MotorHeading(frameBeamstopLH, 'Beamstop')
lh_beamstop_y = OneMotor(frameBeamstopLH, '16IDB:m67', 3)
lh_beamstop_z = OneMotor(frameBeamstopLH, '16IDB:m68', 3)

lh_slits = MotorHeading(frameSlitsLH, 'IDB Slits')
lh_vupr = OneMotor(frameSlitsLH, '16IDB:m57', 3)
lh_vlwr = OneMotor(frameSlitsLH, '16IDB:m58', 3)
lh_vpos = OneMotor(frameSlitsLH, '16IDB:pm11', 3)
lh_vsize = OneMotor(frameSlitsLH, '16IDB:pm12', 3)
lh_hinb = OneMotor(frameSlitsLH, '16IDB:m69', 3)
lh_hotb = OneMotor(frameSlitsLH, '16IDB:m60', 3)
lh_hpos = OneMotor(frameSlitsLH, '16IDB:pm13', 3)
lh_hsize = OneMotor(frameSlitsLH, '16IDB:pm14', 3)

# objects to placed in right frame
lh_vlkb_mirror = MotorHeading(frameVLKBLH, 'Vertical LKB Mirror')
lh_vlkb_stripe = OneMotor(frameVLKBLH, '16IDB:m11', 3)
lh_vlkb_usz = OneMotor(frameVLKBLH, '16IDB:m40', 3)
lh_vlkb_dsf = OneMotor(frameVLKBLH, '16IDB:m39', 3)
lh_vlkb_usf = OneMotor(frameVLKBLH, '16IDB:m38', 3)
lh_vlkb_dsz = OneMotor(frameVLKBLH, '16IDB:m75', 3)
lh_vlkb_pitch = OneMotor(frameVLKBLH, '16IDB:pm26', 3)
lh_vlkb_height = OneMotor(frameVLKBLH, '16IDB:pm25', 3)
lh_vlkb_curvature = OneMotor(frameVLKBLH, '16IDB:pm23', 3)
lh_vlkb_ellipticity = OneMotor(frameVLKBLH, '16IDB:pm24', 3)

lh_hlkb_mirror = MotorHeading(frameHLKBLH, 'Horizontal LKB Mirror')
lh_hlkb_stripe = OneMotor(frameHLKBLH, '16IDB:m9', 3)
lh_hlkb_usz = OneMotor(frameHLKBLH, '16IDB:m78', 3)
lh_hlkb_dsf = OneMotor(frameHLKBLH, '16IDB:m77', 3)
lh_hlkb_usf = OneMotor(frameHLKBLH, '16IDB:m76', 3)
lh_hlkb_dsz = OneMotor(frameHLKBLH, '16IDB:m79', 3)
lh_hlkb_pitch = OneMotor(frameHLKBLH, '16IDB:pm30', 3)
lh_hlkb_height = OneMotor(frameHLKBLH, '16IDB:pm29', 3)
lh_hlkb_curvature = OneMotor(frameHLKBLH, '16IDB:pm27', 3)
lh_hlkb_ellipticity = OneMotor(frameHLKBLH, '16IDB:pm28', 3)

lh_vskb_mirror = MotorHeading(frameVSKBLH, 'Vertical SKB Mirror')
lh_vskb_z = OneMotor(frameVSKBLH, '16IDB:m89', 1)
lh_vskb_pitch = OneMotor(frameVSKBLH, '16IDB:m90')
lh_vskb_usf = OneMotor(frameVSKBLH, '16IDB:m92', 1)
lh_vskb_dsf = OneMotor(frameVSKBLH, '16IDB:m91', 1)
lh_vskb_curvature = OneMotor(frameVSKBLH, '16IDB:pm9', 1)
lh_vskb_ellipticity = OneMotor(frameVSKBLH, '16IDB:pm10', 1)

lh_hskb_mirror = MotorHeading(frameHSKBLH, 'Horizontal SKB Mirror')
lh_hskb_z = OneMotor(frameHSKBLH, '16IDB:m93', 1)
lh_hskb_pitch = OneMotor(frameHSKBLH, '16IDB:m94')
lh_hskb_usf = OneMotor(frameHSKBLH, '16IDB:m96', 1)
lh_hskb_dsf = OneMotor(frameHSKBLH, '16IDB:m95', 1)
lh_hskb_curvature = OneMotor(frameHSKBLH, '16IDB:pm7', 1)
lh_hskb_ellipticity = OneMotor(frameHSKBLH, '16IDB:pm8', 1)

lh_counter_ida_ic = OneCounter(frameCounterLH, '16IDB:', 'scaler1', '_cts2.A', '.NM5', sr='A1', row=0, column=0)
lh_counter_idb_ic = OneCounter(frameCounterLH, '16IDB:', 'scaler1', '_cts1.C', '.NM3', sr='A3', row=1, column=0)
lh_counter_diode = OneCounter(frameCounterLH, '16IDB:', 'scaler1', '_cts1.D', '.NM4', sr='A4', row=0, column=1)
lh_counter_beamstop = OneCounter(frameCounterLH, '16IDB:', 'scaler1', '_cts2.B', '.NM6', sr='A5', row=1, column=1)

idb_lh_time = TimeStamp(frameTimeStampLH, 29, 3)

# closing protocol
root.protocol('WM_DELETE_WINDOW', close_quit)

root.mainloop()
