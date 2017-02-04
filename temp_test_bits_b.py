import collections

mpv = [('Timestamp', ['Timestamp']),
       ('Sample stages', ['XPS Cen X', 'XPS Cen Y', 'XPS Sam Z', 'XPS Omega']),
       ('Counts', ['Ring current', 'IDA-IC', 'IDB-IC', 'Beamstop'])
       ]

print type(mpv)


mpv = collections.OrderedDict(mpv)










print type(mpv)


print mpv.items()
print mpv.keys()
print mpv.values()

for keys in mpv.keys():
    print len(mpv[keys])

mpv2 = {'Timestamp': ['Timestamp'],
        'Sample stages': ['XPS Cen X', 'XPS Cen Y', 'XPS Sam Z', 'XPS Omega'],
        'Counts': ['Ring current', 'IDA-IC', 'IDB-IC', 'Beamstop']}

print type(mpv2)

print mpv2.items()
print mpv2.keys()
print mpv2.values()

for keys in mpv2.keys():
    print len(mpv2[keys])