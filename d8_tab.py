# -*- python -*-
# (subset) table for "DumbAss8" embedded computing core
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.

from pta.BasicWordInstruction import *

Insn('ldib *',    I8, 0x01)
Insn('stab *',   I10, 0xB1)
Insn('jmp *',    I11, 0x10)
Insn('nop',       I0, 0x00)

Insn('ldab @x',   I0, 0x74)
Insn('ldab @x,*', I7, 0x74)
