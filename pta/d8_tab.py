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
Insn("DW *",              I16, 0x0000)

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
Insn("NOP",                I0, 0x0000)
Insn("DATAPIPE",           I0, 0x0001)
Insn("INDEXPIPE",          I0, 0x0002)
Insn("JUMPSHADOWPIPE",     I0, 0x0003)
#  0000 0001 kkkk kkkk
#  BYTE OPERAND
Insn("LDIB *",             I8, 0x0100)
#  0000 00rr xxxx xxxx
#  OPERAND
Insn("RCLB",               I0, 0x0200)
Insn("RCRB",               I0, 0x0300)
Insn("SHLN",               I0, 0x0280)
Insn("SHRN",               I0, 0x0380)
#  0000 rrii ixxx xxxx
Insn("LDAB XL",            I0, 0x0400)
Insn("LDAB YL",            I0, 0x0500)
Insn("LDAB ZL",            I0, 0x0600)
Insn("LDAB TL",            I0, 0x0700)
Insn("LDAB XH",            I0, 0x0480)
Insn("LDAB YH",            I0, 0x0580)
Insn("LDAB ZH",            I0, 0x0680)
Insn("LDAB TH",            I0, 0x0780)
Insn("STAB XL",            I0, 0x0800)
Insn("STAB YL",            I0, 0x0900)
Insn("STAB ZL",            I0, 0x0a00)
Insn("STAB TL",            I0, 0x0b00)
Insn("STAB XH",            I0, 0x0880)
Insn("STAB YH",            I0, 0x0980)
Insn("STAB ZH",            I0, 0x0a80)
Insn("STAB TH",            I0, 0x0b80)
Insn("ADDIX *",            I7, 0x0c00)
Insn("ADDIY *",            I7, 0x0d00)
Insn("ADDIZ *",            I7, 0x0e00)
Insn("ADDIT *",            I7, 0x0f00)
Insn("POP",                I0, 0x0c80)
Insn("PUSH",               I0, 0x0d80)
Insn("LDAB SP",            I0, 0x0e80)
Insn("STAB SP",            I0, 0x0f80)
#  BIT OPERAND, PROGRAM ADDRESS FOR JUMPS
#  iiii 0aaa aaaa aaaa DIRECT INSTRUCTIONS
Insn("JMP *",             I11, 0x1000)
Insn("JMPNZ *",           I11, 0x2000)
Insn("JMPZ *",            I11, 0x3000)
Insn("JMPNC *",           I11, 0x4000)
Insn("JMPC *",            I11, 0x5000)
Insn("JSR *",             I11, 0x6000)
#  8 BIT OFFSET,
#  iiii 0100 0000 0000 INDIRECT INSTRUCTIONS
Insn("LDAB @X",            I0, 0x7400)
Insn("ORB @X",             I0, 0x8400)
Insn("XORB @X",            I0, 0x9400)
Insn("ANDB @X",            I0, 0xa400)
Insn("STAB @X",            I0, 0xb400)
Insn("ADDB @X",            I0, 0xc400)
Insn("ADDCB @X",           I0, 0xd400)
Insn("SUBB @X",            I0, 0xe400)
Insn("SUBCB @X",           I0, 0xf400)
#  8 BIT OPERAND,
#  iiii 0100 oooo oooo INDIRECT INSTRUCTIONS
Insn("LDAB @X,*",          I7, 0x7400)
Insn("ORB @X,*",           I7, 0x8400)
Insn("XORB @X,*",          I7, 0x9400)
Insn("ANDB @X,*",          I7, 0xa400)
Insn("STAB @X,*",          I7, 0xb400)
Insn("ADDB @X,*",          I7, 0xc400)
Insn("ADDCB @X,*",         I7, 0xd400)
Insn("SUBB @X,*",          I7, 0xe400)
Insn("SUBCB @X,*",         I7, 0xf400)
#  8 BIT OFFSET,
#  iiii 1100 0000 0000 INDIRECT INSTRUCTIONS
Insn("ORTOB @X",           I0, 0x8c00)
Insn("XORTOB @X",          I0, 0x9c00)
Insn("ANDTOB @X",          I0, 0xac00)
Insn("STATOB @X",          I0, 0xbc00)
Insn("ADDTOB @X",          I0, 0xcc00)
Insn("ADDCTOB @X",         I0, 0xdc00)
Insn("SUBTOB @X",          I0, 0xec00)
Insn("SUBCTOB @X",         I0, 0xfc00)
#  8 BIT OPERAND,
#  iiii 1100 oooo oooo INDIRECT INSTRUCTIONS
Insn("ORTOB @X,*",         I7, 0x8c00)
Insn("XORTOB @X,*",        I7, 0x9c00)
Insn("ANDTOB @X,*",        I7, 0xac00)
Insn("STATOB @X,*",        I7, 0xbc00)
Insn("ADDTOB @X,*",        I7, 0xcc00)
Insn("ADDCTOB @X,*",       I7, 0xdc00)
Insn("SUBTOB @X,*",        I7, 0xec00)
Insn("SUBCTOB @X,*",       I7, 0xfc00)
#  iiii 0101 0000 0000 INDIRECT INSTRUCTIONS
Insn("LDAB @Y",            I0, 0x7580)
Insn("ORB @Y",             I0, 0x8580)
Insn("XORB @Y",            I0, 0x9580)
Insn("ANDB @Y",            I0, 0xa580)
Insn("STAB @Y",            I0, 0xb580)
Insn("ADDB @Y",            I0, 0xc580)
Insn("ADDCB @Y",           I0, 0xd580)
Insn("SUBB @Y",            I0, 0xe580)
Insn("SUBCB @Y",           I0, 0xf580)
#  iiii 0101 oooo oooo INDIRECT INSTRUCTIONS
Insn("LDAB @Y,*",          I7, 0x7580)
Insn("ORB @Y,*",           I7, 0x8580)
Insn("XORB @Y,*",          I7, 0x9580)
Insn("ANDB @Y,*",          I7, 0xa580)
Insn("STAB @Y,*",          I7, 0xb580)
Insn("ADDB @Y,*",          I7, 0xc580)
Insn("ADDCB @Y,*",         I7, 0xd580)
Insn("SUBB @Y,*",          I7, 0xe580)
Insn("SUBCB @Y,*",         I7, 0xf580)
#  iiii 1101 0000 0000 INDIRECT INSTRUCTIONS
Insn("ORTOB @Y",           I0, 0x8d80)
Insn("XORTOB @Y",          I0, 0x9d80)
Insn("ANDTOB @Y",          I0, 0xad80)
Insn("STATOB @Y",          I0, 0xbd80)
Insn("ADDTOB @Y",          I0, 0xcd80)
Insn("ADDCTOB @Y",         I0, 0xdd80)
Insn("SUBTOB @Y",          I0, 0xed80)
Insn("SUBCTOB @Y",         I0, 0xfd00)
#  iiii 1101 oooo oooo INDIRECT INSTRUCTIONS
Insn("ORTOB @Y,*",         I7, 0x8d80)
Insn("XORTOB @Y,*",        I7, 0x9d80)
Insn("ANDTOB @Y,*",        I7, 0xad80)
Insn("STATOB @Y,*",        I7, 0xbd80)
Insn("ADDTOB @Y,*",        I7, 0xcd80)
Insn("ADDCTOB @Y,*",       I7, 0xdd80)
Insn("SUBTOB @Y,*",        I7, 0xed80)
Insn("SUBCTOB @Y,*",       I7, 0xfd80)
#  iiii 0110 0000 0000 INDIRECT INSTRUCTIONS
Insn("LDAB @Z",            I0, 0x7600)
Insn("ORB @Z",             I0, 0x8600)
Insn("XORB @Z",            I0, 0x9600)
Insn("ANDB @Z",            I0, 0xa600)
Insn("STAB @Z",            I0, 0xb600)
Insn("ADDB @Z",            I0, 0xc600)
Insn("ADDCB @Z",           I0, 0xd600)
Insn("SUBB @Z",            I0, 0xe600)
Insn("SUBCB @Z",           I0, 0xf600)
#  iiii 0110 oooo oooo INDIRECT INSTRUCTIONS
Insn("LDAB @Z,*",          I7, 0x7600)
Insn("ORB @Z,*",           I7, 0x8600)
Insn("XORB @Z,*",          I7, 0x9600)
Insn("ANDB @Z,*",          I7, 0xa600)
Insn("STAB @Z,*",          I7, 0xb600)
Insn("ADDB @Z,*",          I7, 0xc600)
Insn("ADDCB @Z,*",         I7, 0xd600)
Insn("SUBB @Z,*",          I7, 0xe600)
Insn("SUBCB @Z,*",         I7, 0xf600)
#  iiii 1110 0000 0000 INDIRECT INSTRUCTIONS
Insn("ORTOB @Z",           I0, 0x8e00)
Insn("XORTOB @Z",          I0, 0x9e00)
Insn("ANDTOB @Z",          I0, 0xae00)
Insn("STATOB @Z",          I0, 0xbe00)
Insn("ADDTOB @Z",          I0, 0xce00)
Insn("ADDCTOB @Z",         I0, 0xde00)
Insn("SUBTOB @Z",          I0, 0xee00)
Insn("SUBCTOB @Z",         I0, 0xfe00)
#  iiii 1110 oooo oooo INDIRECT INSTRUCTIONS
Insn("ORTOB @Z,*",         I7, 0x8e00)
Insn("XORTOB @Z,*",        I7, 0x9e00)
Insn("ANDTOB @Z,*",        I7, 0xae00)
Insn("STATOB @Z,*",        I7, 0xbe00)
Insn("ADDTOB @Z,*",        I7, 0xce00)
Insn("ADDCTOB @Z,*",       I7, 0xde00)
Insn("SUBTOB @Z,*",        I7, 0xee00)
Insn("SUBCTOB @Z,*",       I7, 0xfe00)
#  iiii 0111 0000 0000 INDIRECT INSTRUCTIONS
Insn("LDAB @T",            I0, 0x7700)
Insn("ORB @T",             I0, 0x8700)
Insn("XORB @T",            I0, 0x9700)
Insn("ANDB @T",            I0, 0xa700)
Insn("STAB @T",            I0, 0xb700)
Insn("ADDB @T",            I0, 0xc700)
Insn("ADDCB @T",           I0, 0xd700)
Insn("SUBB @T",            I0, 0xe700)
Insn("SUBCB @T",           I0, 0xf700)
#  iiii 0111 oooo oooo INDIRECT INSTRUCTIONS
Insn("LDAB @T,*",          I7, 0x7700)
Insn("ORB @T,*",           I7, 0x8700)
Insn("XORB @T,*",          I7, 0x9700)
Insn("ANDB @T,*",          I7, 0xa700)
Insn("STAB @T,*",          I7, 0xb700)
Insn("ADDB @T,*",          I7, 0xc700)
Insn("ADDCB @T,*",         I7, 0xd700)
Insn("SUBB @T,*",          I7, 0xe700)
Insn("SUBCB @T,*",         I7, 0xf700)
#  iiii 1111 0000 0000 INDIRECT INSTRUCTIONS
Insn("ORTOB @T",           I0, 0x8f00)
Insn("XORTOB @T",          I0, 0x9f00)
Insn("ANDTOB @T",          I0, 0xaf00)
Insn("STATOB @T",          I0, 0xbf00)
Insn("ADDTOB @T",          I0, 0xcf00)
Insn("ADDCTOB @T",         I0, 0xdf00)
Insn("SUBTOB @T",          I0, 0xef00)
Insn("SUBCTOB @T",         I0, 0xff00)
#  iiii 1111 oooo oooo INDIRECT INSTRUCTIONS
Insn("ORTOB @T,*",         I7, 0x8f00)
Insn("XORTOB @T,*",        I7, 0x9f00)
Insn("ANDTOB @T,*",        I7, 0xaf00)
Insn("STATOB @T,*",        I7, 0xbf00)
Insn("ADDTOB @T,*",        I7, 0xcf00)
Insn("ADDCTOB @T,*",       I7, 0xdf00)
Insn("SUBTOB @T,*",        I7, 0xef00)
Insn("SUBCTOB @T,*",       I7, 0xff00)
#  BIT return addresses
#  iiii 1aaa aaaa aaaa DIRECT INSTRUCTIONS
Insn("RET",                I0, 0x1800)
Insn("RETNZ",              I0, 0x2800)
Insn("RETZ",               I0, 0x3800)
Insn("RETNC",              I0, 0x4800)
Insn("RETC",               I0, 0x5800)
Insn("RET@",               I0, 0x6800)
#  REF INST 10 BIT OPERAND ADDRESS
#  iiii 00nn nnnn nnnn DIRECT INSTRUCTIONS
Insn("LDAB *",            I10, 0x7000)
Insn("ORB *",             I10, 0x8000)
Insn("XORB *",            I10, 0x9000)
Insn("ANDB *",            I10, 0xa000)
Insn("STAB *",            I10, 0xb000)
Insn("ADDB *",            I10, 0xc000)
Insn("ADDCB *",           I10, 0xd000)
Insn("SUBB *",            I10, 0xe000)
Insn("SUBCB *",           I10, 0xf000)
#  REF TO INST 10 BIT OPERAND ADDRESS
#  iiii 10nn nnnn nnnn DIRECT INSTRUCTIONS
Insn("ORTOB *",           I10, 0x8800)
Insn("XORTOB *",          I10, 0x9800)
Insn("ANDTOB *",          I10, 0xa800)
Insn("STATOB *",          I10, 0xb800)
Insn("ADDTOB *",          I10, 0xc800)
Insn("ADDCTOB *",         I10, 0xd800)
Insn("SUBTOB *",          I10, 0xe800)
Insn("SUBCTOB *",         I10, 0xf800)
