#!/usr/bin/python
import sys

address_spaces = {'eword': 'eeprom', 'ebyte': 'eeprom'}
hardoffsets = {None: 0, 'eeprom': 0}
offsets = {None: 0, 'eeprom': 0}
numformat = "0%Xh"
sizes = {
    'byte': 1, 'bint': 1, 'ebyte': 1, 'enum': 1,
    'ulong': 4, 'long':4,
    'double': 8,
}

if len(sys.argv) > 1 and sys.argv[1] == "--8i20":
    hardoffsets[None] = 2048
    numformat = "%d"

def calc(value, kind):
    address_space = address_spaces.get(kind)
    size = sizes.get(kind, 2)
    if value == "#":
        result = offsets[address_space]
    elif value == "$":
        result = offsets[address_space]
        offsets[address_space] += size
    else:
        value = value.lower()
        if value.endswith("h"): value = int(value[:-1], 16)
        else: value = int(value)
        result = value
        offsets[address_space] = result + size
    return numformat % (
        result + hardoffsets.get(address_space, hardoffsets[None]))

for line in sys.stdin:
    line = line.strip("\032")
    line = line.strip()
    if not line:
        print
        continue
    if line.startswith(";"):
        print line
        continue
    
    if ';' in line:
        line, comment = line.split(";", 1)
        line = line.strip()
    else:
        comment = ""

    parts = line.split(None, 3)

    if len(parts) == 2:
        print "%s equ 0%s" % (parts[0], parts[1])
        continue

    name, value, kind = parts[:3]

    kind = kind.strip("%")
    value = calc(value, kind)

    name = name + "_" + kind
    print "%(name)-20s equ %(value)-20s ; %(comment)s" % {
        'name': name, 'value': value, 'comment': comment
    }
