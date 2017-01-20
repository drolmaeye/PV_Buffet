from Tkinter import *
from tktable import *
from epics import *
import collections

d = collections.OrderedDict()

cenxmdesc = PV('XPSGP:m1.DESC')
cenxmrbv = PV('XPSGP:m1.RBV')
cenymdesc = PV('XPSGP:m2.DESC')
cenymrbv = PV('XPSGP:m2.RBV')

print cenxmdesc.value
print cenxmrbv.value
print cenymdesc.value
print cenymrbv.value

d[cenxmdesc.value] = cenxmrbv.value
d[cenymdesc.value] = cenymrbv.value

print d.values()
