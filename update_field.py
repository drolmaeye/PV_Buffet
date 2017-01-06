__author__ = 'j.smith'

# import necessary modules
from Tkinter import *
from epics import *


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

        # create PVs
        self.mdesc = PV(motor + '.DESC', callback=self.update_desc)
        self.mrbv = PV(motor + '.RBV', callback=self.update_rbv)
        self.mdrbv = PV(motor + '.DRBV', callback=self.update_drbv)
        self.megu = PV(motor + '.EGU', callback=self.update_egu)

        # create precision string
        self.p_string = '%.' + str(precision) + 'f'

        # define instance variables and get initial values
        self.desc = StringVar()
        self.rbv = StringVar()
        self.drbv = StringVar()
        self.egu = StringVar()
        self.desc.set(self.mdesc.value)
        self.rbv.set(self.p_string % self.mrbv.value)
        self.drbv.set(self.p_string % self.mdrbv.value)
        self.egu.set(self.megu.value)

        # ###print self.desc.get()
        # ###print self.rbv.get()
        # ###print self.drbv.get()
        # ###print self.egu.get()

        # make display line
        self.desc_label = Label(self.frame, textvariable=self.desc, width=20, anchor='w')
        self.rbv_label = Label(self.frame, textvariable=self.rbv, width=10, anchor='w', relief=SUNKEN)
        self.drbv_label = Label(self.frame, textvariable=self.drbv, width=10, anchor='w', relief=SUNKEN)
        self.egu_label = Label(self.frame, textvariable=self.egu, width=6, anchor='w')

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


root = Tk()
root.title('Update Field')

# Primary frames for displaying objects
frameLeft = Frame(root)
frameLeft.grid(row=0, column=0)
frameXPS = Frame(frameLeft, bd=5, relief=RIDGE)
frameXPS.grid(row=0, column=0)
frameHighLoad = Frame(frameLeft, bd=5, relief=RIDGE)
frameHighLoad.grid(row=1, column=0)
frameCommon = Frame(frameLeft, bd=5, relief=RIDGE)
frameCommon.grid(row=2, column=0)
frameDetector = Frame(frameLeft, bd=5, relief=RIDGE)
frameDetector.grid(row=3, column=0)
frameLKBPinhole = Frame(frameLeft, bd=5, relief=RIDGE)
frameLKBPinhole.grid(row=4, column=0)
frameSKBPinhole = Frame(frameLeft, bd=5, relief=RIDGE)
frameSKBPinhole.grid(row=5, column=0)
frameBeamstop = Frame(frameLeft, bd=5, relief=RIDGE)
frameBeamstop.grid(row=6, column=0)
frameSlits = Frame(frameLeft, bd=5, relief=RIDGE)
frameSlits.grid(row=7, column=0)


frameRight = Frame(root)
frameRight.grid(row=0, column=1)
frameLKBX = Frame(frameRight, bd=5, relief=RIDGE)
frameLKBX.grid(row=0, column=1)
frameVLKB = Frame(frameRight, bd=5, relief=RIDGE)
frameVLKB.grid(row=1, column=1)
frameHLKB = Frame(frameRight, bd=5, relief=RIDGE)
frameHLKB.grid(row=2, column=1)
frameVSKB = Frame(frameRight, bd=5, relief=RIDGE)
frameVSKB.grid(row=3, column=1)
frameHSKB = Frame(frameRight, bd=5, relief=RIDGE)
frameHSKB.grid(row=4, column=1)


# objects to be places in primary frames
high_precision = MotorHeading(frameXPS, 'High precision sample')
xps_cen_x = OneMotor(frameXPS, 'XPSGP:m1', 4)
xps_cen_y = OneMotor(frameXPS, 'XPSGP:m2', 4)
xps_sam_z = OneMotor(frameXPS, 'XPSGP:m3', 4)
xps_omega = OneMotor(frameXPS, 'XPSGP:m4', 3)

high_load = MotorHeading(frameHighLoad, 'High load sample')
cen_x = OneMotor(frameHighLoad, '16IDB:m31', 3)
cen_y = OneMotor(frameHighLoad, '16IDB:m32', 3)

shared_sample = MotorHeading(frameCommon, 'Shared sample')
sam_z = OneMotor(frameCommon, '16IDB:m5', 3)
gp_omega = OneMotor(frameCommon, 'XPSGP:m5', 3)
sam_y = OneMotor(frameCommon, '16IDB:m4', 3)

detector = MotorHeading(frameDetector, 'Detector')
detector_x = OneMotor(frameDetector, '16IDB:m7', 3)
detector_y = OneMotor(frameDetector, '16IDB:m6', 3)

lkb_pinhole = MotorHeading(frameLKBPinhole, 'LKB Pinhole')
lkb_pinhole_x = OneMotor(frameLKBPinhole, '16IDB:m2', 3)
lkb_pinhole_y = OneMotor(frameLKBPinhole, '16IDB:m19', 3)
lkb_pinhole_z = OneMotor(frameLKBPinhole, '16IDB:m24', 3)
lkb_pinhole_pt = OneMotor(frameLKBPinhole, '16IDB:m26', 3)
lkb_pinhole_yw = OneMotor(frameLKBPinhole, '16IDB:m74', 3)

skb_pinhole = MotorHeading(frameSKBPinhole, 'SKB Pinhole')
skb_pinhole_x = OneMotor(frameSKBPinhole, '16IDB:m16', 3)
skb_pinhole_y = OneMotor(frameSKBPinhole, '16IDB:m17', 3)
skb_pinhole_z = OneMotor(frameSKBPinhole, '16IDB:m18', 3)
skb_pinhole_pt = OneMotor(frameSKBPinhole, '16IDB:m36', 3)
skb_pinhole_yw = OneMotor(frameSKBPinhole, '16IDB:m66', 3)

beamstop = MotorHeading(frameBeamstop, 'Beamstop')
beamstop_y = OneMotor(frameBeamstop, '16IDB:m34', 3)
beamstop_z = OneMotor(frameBeamstop, '16IDB:m35', 3)

idb_slits = MotorHeading(frameSlits, 'IDB Slits')
idb_hpos = OneMotor(frameSlits, '16IDB:m21', 3)
idb_hsize = OneMotor(frameSlits, '16IDB:m23', 3)
idb_vpos = OneMotor(frameSlits, '16IDB:m22', 3)
idb_vsize = OneMotor(frameSlits, '16IDB:m20', 3)

lkb_mirror_x = MotorHeading(frameLKBX, 'LKB Mirror X')
lkb_x_position = OneMotor(frameLKBX, '16IDB:m1', 3)

vlkb_mirror = MotorHeading(frameVLKB, 'Vertical LKB Mirror')
vlkb_stripe = OneMotor(frameVLKB, '16IDB:m15', 3)
vlkb_usz = OneMotor(frameVLKB, '16IDB:m41', 3)
vlkb_dsf = OneMotor(frameVLKB, '16IDB:m59', 3)
vlkb_usf = OneMotor(frameVLKB, '16IDB:m43', 3)
vlkb_dsz = OneMotor(frameVLKB, '16IDB:m42', 3)
vlkb_pitch = OneMotor(frameVLKB, '16IDB:pm18', 3)
vlkb_height = OneMotor(frameVLKB, '16IDB:pm17', 3)
vlkb_curvature = OneMotor(frameVLKB, '16IDB:pm15', 3)
vlkb_ellipticity = OneMotor(frameVLKB, '16IDB:pm16', 3)

hlkb_mirror = MotorHeading(frameHLKB, 'Horizontal LKB Mirror')
hlkb_stripe = OneMotor(frameHLKB, '16IDB:m14', 3)
hlkb_usz = OneMotor(frameHLKB, '16IDB:m25', 3)
hlkb_dsf = OneMotor(frameHLKB, '16IDB:m29', 3)
hlkb_usf = OneMotor(frameHLKB, '16IDB:m28', 3)
hlkb_dsz = OneMotor(frameHLKB, '16IDB:m27', 3)
hlkb_pitch = OneMotor(frameHLKB, '16IDB:pm22', 3)
hlkb_height = OneMotor(frameHLKB, '16IDB:pm21', 3)
hlkb_curvature = OneMotor(frameHLKB, '16IDB:pm19', 3)
hlkb_ellipticity = OneMotor(frameHLKB, '16IDB:pm20', 3)

vskb_mirror = MotorHeading(frameVSKB, 'Vertical SKB Mirror')
vskb_z = OneMotor(frameVSKB, '16IDB:m81', 1)
vskb_pitch = OneMotor(frameVSKB, '16IDB:m82')
vskb_usf = OneMotor(frameVSKB, '16IDB:m83', 1)
vskb_dsf = OneMotor(frameVSKB, '16IDB:m84', 1)
vskb_curvature = OneMotor(frameVSKB, '16IDB:pm5', 1)
vskb_ellipticity = OneMotor(frameVSKB, '16IDB:pm6', 1)

hskb_mirror = MotorHeading(frameHSKB, 'Horizontal SKB Mirror')
hskb_z = OneMotor(frameHSKB, '16IDB:m85', 1)
hskb_pitch = OneMotor(frameHSKB, '16IDB:m86')
hskb_usf = OneMotor(frameHSKB, '16IDB:m87', 1)
hskb_dsf = OneMotor(frameHSKB, '16IDB:m88', 1)
hskb_curvature = OneMotor(frameHSKB, '16IDB:pm3', 1)
hskb_ellipticity = OneMotor(frameHSKB, '16IDB:pm4', 1)

root.mainloop()
