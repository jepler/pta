# -*- python -*-
# table for "DumbAss8",embedded computing core
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.
#
# Converted mostly automtaically from TASMD8SS.TAB
#

from pta.BasicWordInstruction import *

#  This is the instruction set definition table for the Dumb8SQW
#
#  No (unconditional jumps or calls) or (reads with side effects) in the 2 instruction shadow of conditional jumps
#  Three pipes required after stab or xxto of variable until ldab
#  Three pipes required after stab of Index until ldab @
#
#  Gilbert Eldredge, CopyRight MESA Electronics, 2011.
#
#  iiii WInn nnnn nnnn DIRECT INSTRUCTIONS
#  iiii is instruction, Writeback, Indirect,
#  4 index registers
#  addresses extended to 11 bits 7-2009
#  added SHLN,SHRN 5-2011
#  reduced address field
#  added to instructions ldatob left out for simple decode
#
#  ARGS OPCODE BYTES MOD CLASS SHIFT OR */
#  r : operate opcode
#  x : don't care
#  k : constant
#  a : address
#  p : page
#  o : offset
#  0000 0000 xxxx xxxx
#  OPERAND
Insn("NOP",                I0, 0x00)
Insn("DATAPIPE",           I0, 0x00)
Insn("INDEXPIPE",          I0, 0x00)
Insn("JUMPSHADOWPIPE",     I0, 0x00)
#  0000 0001 kkkk kkkk
#  BYTE OPERAND
Insn("LDIB *",             I8, 0x01)
#  0000 00rr xxxx xxxx
#  OPERAND
Insn("RCLB",               I0, 0x02)
Insn("RCRB",               I0, 0x03)
Insn("SHLN",               I0, 0x02)
Insn("SHRN",               I0, 0x03)
#  0000 rrii ixxx xxxx
Insn("LDAB XL",            I0, 0x04)
Insn("LDAB YL",            I0, 0x05)
Insn("LDAB ZL",            I0, 0x06)
Insn("LDAB TL",            I0, 0x07)
Insn("LDAB XH",            I0, 0x04)
Insn("LDAB YH",            I0, 0x05)
Insn("LDAB ZH",            I0, 0x06)
Insn("LDAB TH",            I0, 0x07)
Insn("STAB XL",            I0, 0x08)
Insn("STAB YL",            I0, 0x09)
Insn("STAB ZL",            I0, 0x0a)
Insn("STAB TL",            I0, 0x0b)
Insn("STAB XH",            I0, 0x08)
Insn("STAB YH",            I0, 0x09)
Insn("STAB ZH",            I0, 0x0a)
Insn("STAB TH",            I0, 0x0b)
Insn("ADDIX *",            I7, 0x0c)
Insn("ADDIY *",            I7, 0x0d)
Insn("ADDIZ *",            I7, 0x0e)
Insn("ADDIT *",            I7, 0x0f)
Insn("POP",                I0, 0x0c)
Insn("PUSH",               I0, 0x0d)
Insn("LDAB SP",            I0, 0x0e)
Insn("STAB SP",            I0, 0x0f)
#  BIT OPERAND, PROGRAM ADDRESS FOR JUMPS
#  iiii 0aaa aaaa aaaa DIRECT INSTRUCTIONS
Insn("JMP *",             I11, 0x10)
Insn("JMPNZ *",           I11, 0x20)
Insn("JMPZ *",            I11, 0x30)
Insn("JMPNC *",           I11, 0x40)
Insn("JMPC *",            I11, 0x50)
Insn("JSR *",             I11, 0x60)
#  8 BIT OFFSET,
#  iiii 0100 0000 0000 INDIRECT INSTRUCTIONS
Insn("LDAB @X",            I0, 0x74)
Insn("ORB @X",             I0, 0x84)
Insn("XORB @X",            I0, 0x94)
Insn("ANDB @X",            I0, 0xa4)
Insn("STAB @X",            I0, 0xb4)
Insn("ADDB @X",            I0, 0xc4)
Insn("ADDCB @X",           I0, 0xd4)
Insn("SUBB @X",            I0, 0xe4)
Insn("SUBCB @X",           I0, 0xf4)
#  8 BIT OPERAND,
#  iiii 0100 oooo oooo INDIRECT INSTRUCTIONS
Insn("LDAB @X,*",          I7, 0x74)
Insn("ORB @X,*",           I7, 0x84)
Insn("XORB @X,*",          I7, 0x94)
Insn("ANDB @X,*",          I7, 0xa4)
Insn("STAB @X,*",          I7, 0xb4)
Insn("ADDB @X,*",          I7, 0xc4)
Insn("ADDCB @X,*",         I7, 0xd4)
Insn("SUBB @X,*",          I7, 0xe4)
Insn("SUBCB @X,*",         I7, 0xf4)
#  8 BIT OFFSET,
#  iiii 1100 0000 0000 INDIRECT INSTRUCTIONS
Insn("ORTOB @X",           I0, 0x8c)
Insn("XORTOB @X",          I0, 0x9c)
Insn("ANDTOB @X",          I0, 0xac)
Insn("STATOB @X",          I0, 0xbc)
Insn("ADDTOB @X",          I0, 0xcc)
Insn("ADDCTOB @X",         I0, 0xdc)
Insn("SUBTOB @X",          I0, 0xec)
Insn("SUBCTOB @X",         I0, 0xfc)
#  8 BIT OPERAND,
#  iiii 1100 oooo oooo INDIRECT INSTRUCTIONS
Insn("ORTOB @X,*",         I7, 0x8c)
Insn("XORTOB @X,*",        I7, 0x9c)
Insn("ANDTOB @X,*",        I7, 0xac)
Insn("STATOB @X,*",        I7, 0xbc)
Insn("ADDTOB @X,*",        I7, 0xcc)
Insn("ADDCTOB @X,*",       I7, 0xdc)
Insn("SUBTOB @X,*",        I7, 0xec)
Insn("SUBCTOB @X,*",       I7, 0xfc)
#  iiii 0101 0000 0000 INDIRECT INSTRUCTIONS
Insn("LDAB @Y",            I0, 0x75)
Insn("ORB @Y",             I0, 0x85)
Insn("XORB @Y",            I0, 0x95)
Insn("ANDB @Y",            I0, 0xa5)
Insn("STAB @Y",            I0, 0xb5)
Insn("ADDB @Y",            I0, 0xc5)
Insn("ADDCB @Y",           I0, 0xd5)
Insn("SUBB @Y",            I0, 0xe5)
Insn("SUBCB @Y",           I0, 0xf5)
#  iiii 0101 oooo oooo INDIRECT INSTRUCTIONS
Insn("LDAB @Y,*",          I7, 0x75)
Insn("ORB @Y,*",           I7, 0x85)
Insn("XORB @Y,*",          I7, 0x95)
Insn("ANDB @Y,*",          I7, 0xa5)
Insn("STAB @Y,*",          I7, 0xb5)
Insn("ADDB @Y,*",          I7, 0xc5)
Insn("ADDCB @Y,*",         I7, 0xd5)
Insn("SUBB @Y,*",          I7, 0xe5)
Insn("SUBCB @Y,*",         I7, 0xf5)
#  iiii 1101 0000 0000 INDIRECT INSTRUCTIONS
Insn("ORTOB @Y",           I0, 0x8d)
Insn("XORTOB @Y",          I0, 0x9d)
Insn("ANDTOB @Y",          I0, 0xad)
Insn("STATOB @Y",          I0, 0xbd)
Insn("ADDTOB @Y",          I0, 0xcd)
Insn("ADDCTOB @Y",         I0, 0xdd)
Insn("SUBTOB @Y",          I0, 0xed)
Insn("SUBCTOB @Y",         I0, 0xfd)
#  iiii 1101 oooo oooo INDIRECT INSTRUCTIONS
Insn("ORTOB @Y,*",         I7, 0x8d)
Insn("XORTOB @Y,*",        I7, 0x9d)
Insn("ANDTOB @Y,*",        I7, 0xad)
Insn("STATOB @Y,*",        I7, 0xbd)
Insn("ADDTOB @Y,*",        I7, 0xcd)
Insn("ADDCTOB @Y,*",       I7, 0xdd)
Insn("SUBTOB @Y,*",        I7, 0xed)
Insn("SUBCTOB @Y,*",       I7, 0xfd)
#  iiii 0110 0000 0000 INDIRECT INSTRUCTIONS
Insn("LDAB @Z",            I0, 0x76)
Insn("ORB @Z",             I0, 0x86)
Insn("XORB @Z",            I0, 0x96)
Insn("ANDB @Z",            I0, 0xa6)
Insn("STAB @Z",            I0, 0xb6)
Insn("ADDB @Z",            I0, 0xc6)
Insn("ADDCB @Z",           I0, 0xd6)
Insn("SUBB @Z",            I0, 0xe6)
Insn("SUBCB @Z",           I0, 0xf6)
#  iiii 0110 oooo oooo INDIRECT INSTRUCTIONS
Insn("LDAB @Z,*",          I7, 0x76)
Insn("ORB @Z,*",           I7, 0x86)
Insn("XORB @Z,*",          I7, 0x96)
Insn("ANDB @Z,*",          I7, 0xa6)
Insn("STAB @Z,*",          I7, 0xb6)
Insn("ADDB @Z,*",          I7, 0xc6)
Insn("ADDCB @Z,*",         I7, 0xd6)
Insn("SUBB @Z,*",          I7, 0xe6)
Insn("SUBCB @Z,*",         I7, 0xf6)
#  iiii 1110 0000 0000 INDIRECT INSTRUCTIONS
Insn("ORTOB @Z",           I0, 0x8e)
Insn("XORTOB @Z",          I0, 0x9e)
Insn("ANDTOB @Z",          I0, 0xae)
Insn("STATOB @Z",          I0, 0xbe)
Insn("ADDTOB @Z",          I0, 0xce)
Insn("ADDCTOB @Z",         I0, 0xde)
Insn("SUBTOB @Z",          I0, 0xee)
Insn("SUBCTOB @Z",         I0, 0xfe)
#  iiii 1110 oooo oooo INDIRECT INSTRUCTIONS
Insn("ORTOB @Z,*",         I7, 0x8e)
Insn("XORTOB @Z,*",        I7, 0x9e)
Insn("ANDTOB @Z,*",        I7, 0xae)
Insn("STATOB @Z,*",        I7, 0xbe)
Insn("ADDTOB @Z,*",        I7, 0xce)
Insn("ADDCTOB @Z,*",       I7, 0xde)
Insn("SUBTOB @Z,*",        I7, 0xee)
Insn("SUBCTOB @Z,*",       I7, 0xfe)
#  iiii 0111 0000 0000 INDIRECT INSTRUCTIONS
Insn("LDAB @T",            I0, 0x77)
Insn("ORB @T",             I0, 0x87)
Insn("XORB @T",            I0, 0x97)
Insn("ANDB @T",            I0, 0xa7)
Insn("STAB @T",            I0, 0xb7)
Insn("ADDB @T",            I0, 0xc7)
Insn("ADDCB @T",           I0, 0xd7)
Insn("SUBB @T",            I0, 0xe7)
Insn("SUBCB @T",           I0, 0xf7)
#  iiii 0111 oooo oooo INDIRECT INSTRUCTIONS
Insn("LDAB @T,*",          I7, 0x77)
Insn("ORB @T,*",           I7, 0x87)
Insn("XORB @T,*",          I7, 0x97)
Insn("ANDB @T,*",          I7, 0xa7)
Insn("STAB @T,*",          I7, 0xb7)
Insn("ADDB @T,*",          I7, 0xc7)
Insn("ADDCB @T,*",         I7, 0xd7)
Insn("SUBB @T,*",          I7, 0xe7)
Insn("SUBCB @T,*",         I7, 0xf7)
#  iiii 1111 0000 0000 INDIRECT INSTRUCTIONS
Insn("ORTOB @T",           I0, 0x8f)
Insn("XORTOB @T",          I0, 0x9f)
Insn("ANDTOB @T",          I0, 0xaf)
Insn("STATOB @T",          I0, 0xbf)
Insn("ADDTOB @T",          I0, 0xcf)
Insn("ADDCTOB @T",         I0, 0xdf)
Insn("SUBTOB @T",          I0, 0xef)
Insn("SUBCTOB @T",         I0, 0xff)
#  iiii 1111 oooo oooo INDIRECT INSTRUCTIONS
Insn("ORTOB @T,*",         I7, 0x8f)
Insn("XORTOB @T,*",        I7, 0x9f)
Insn("ANDTOB @T,*",        I7, 0xaf)
Insn("STATOB @T,*",        I7, 0xbf)
Insn("ADDTOB @T,*",        I7, 0xcf)
Insn("ADDCTOB @T,*",       I7, 0xdf)
Insn("SUBTOB @T,*",        I7, 0xef)
Insn("SUBCTOB @T,*",       I7, 0xff)
#  BIT return addresses
#  iiii 1aaa aaaa aaaa DIRECT INSTRUCTIONS
Insn("RET",                I0, 0x18)
Insn("RETNZ",              I0, 0x28)
Insn("RETZ",               I0, 0x38)
Insn("RETNC",              I0, 0x48)
Insn("RETC",               I0, 0x58)
Insn("RET@",               I0, 0x68)
#  REF INST 10 BIT OPERAND ADDRESS
#  iiii 00nn nnnn nnnn DIRECT INSTRUCTIONS
Insn("LDAB *",            I10, 0x70)
Insn("ORB *",             I10, 0x80)
Insn("XORB *",            I10, 0x90)
Insn("ANDB *",            I10, 0xa0)
Insn("STAB *",            I10, 0xb0)
Insn("ADDB *",            I10, 0xc0)
Insn("ADDCB *",           I10, 0xd0)
Insn("SUBB *",            I10, 0xe0)
Insn("SUBCB *",           I10, 0xf0)
#  REF TO INST 10 BIT OPERAND ADDRESS
#  iiii 10nn nnnn nnnn DIRECT INSTRUCTIONS
Insn("ORTOB *",           I10, 0x88)
Insn("XORTOB *",          I10, 0x98)
Insn("ANDTOB *",          I10, 0xa8)
Insn("STATOB *",          I10, 0xb8)
Insn("ADDTOB *",          I10, 0xc8)
Insn("ADDCTOB *",         I10, 0xd8)
Insn("SUBTOB *",          I10, 0xe8)
Insn("SUBCTOB *",         I10, 0xf8)
