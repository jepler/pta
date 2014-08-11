#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2014 Jeff Epler http://emergent.unpythonic.net
#
# This program is is licensed under a disjunctive dual license giving you
# the choice of one of the two following sets of free software/open source
# licensing terms:
#
#    * GNU General Public License (GPL), version 2.0 or later
#    * 3-clause BSD License
#
#
# The GNU GPL License:
#
#     This program is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 2 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program; if not, write to the Free Software
#     Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
#
#
# The 3-clause BSD License:
#
#     Redistribution and use in source and binary forms, with or without
#     modification, are permitted provided that the following conditions
#     are met:
#
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
#   * Redistributions in binary form must reproduce the above
#     copyright notice, this list of conditions and the following
#     disclaimer in the documentation and/or other materials
#     provided with the distribution.
#
#   * Neither the name of Mesa Electronics nor the names of its
#     contributors may be used to endorse or promote products
#     derived from this software without specific prior written
#     permission.
#
#
# Disclaimer:
#
#     THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#     "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#     LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#     FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#     COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#     INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#     BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#     LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#     CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#     LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
#     ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#     POSSIBILITY OF SUCH DAMAGE.
import getopt
import os
import sys
import pta

from pta.grammar import *

Instruction = Forward()

Org = (Literal("org") + Combine(Expression)).setResultsName("origin")

Grammar = (
    Assignment
    #| (PyCode).setResultsName("pycode")
    | (Label + Optional(Colon) + Instruction.setResultsName("instruction"))
    | (White() * STAR + Instruction.setResultsName("instruction"))
    | (White() * STAR + Org)
    | (Label + Optional(Colon))
    | Empty())

def strip(line):
    return line.split(";", 1)[0].rstrip()

class Assembler:
    def __init__(self):
        self.InstructionSet = []

    def run(self, program, filename):
        self.rom = {}
        self.symbols = {}

        self.input(program, filename)
        self.pass1()
        self.pass2()

    def input(self, program, filename):
        self.filename = filename
        program = ((i+1, strip(line))
            for i, line in enumerate(program.split("\n")))
        self.program = [(i, Grammar.parseString(line, True))
            for i, line in program if line]

    def symval(self, expr):
        if not expr: return 0
        return eval(expr, self.symbols)

    def error(self, lno, err):
        print "%s:%d: %s" % (self.filename, lno, err)
        raise SystemExit

    def pass1(self):
        self.symbols['__passno__'] = 1
        addr = 0
        lno = 0

        for lno, line in self.program:
            self.symbols['__lno__'] = lno
            self.symbols['__addr__'] = addr
            if line.origin:
                addr = self.symval(line.origin[1])
            if line.label:
                self.symbols[line.label] = addr
            if line.instruction:
                instruction = line.instruction[0]
                addr += instruction.length
            if line.assignment:
                self.symbols[line.id] = self.symval(line.expr)

    def pass2(self):
        self.symbols['__passno__'] = 2
        addr = 0

        for lno, line in self.program:
            self.symbols['__lno__'] = lno
            self.symbols['__addr__'] = addr

            if line.origin:
                addr = self.symval(line.origin[1])
            if line.instruction:
                instruction = line.instruction[0]
                for i, w in enumerate(instruction.assemble(self)):
                    self.rom[addr + i] = w
                addr += instruction.length

def resolve(fn, *args):
    if os.sep in fn: return fn
    for path in args:
        fn1 = os.path.join(path, fn)
        if os.path.exists(fn1): return fn1
    return fn

def main():
    tabname = "d8_tab.py"
    opts, args = getopt.getopt(sys.argv[1:], "t:")

    if not args:
        filename = '-'
    elif len(args) > 1:
        raise SystemExit, "usage: %s [-t table] [filename]" % sys.argv[0]
    else: filename = args[0]

    for k, v in opts:
        if k == '-t': tabname = v

    if filename == '-': program = sys.stdin.read()
    else: program = open(filename).read()

    assembler = Assembler()

    def Insn(a, b, *args, **kw):
        def inner(*toks):
            if toks is None: return
            return b(*args + toks,  **kw)
        assembler.InstructionSet.append((a, inner))

    resolved_tabname = resolve(tabname, os.curdir, os.path.dirname(pta.__file__), os.path.dirname(__file__))
    Value = lambda v: assembler.symval(v)
    ns = {'__name__': os.path.splitext(os.path.basename(tabname))[0],
          '__file__': resolved_tabname,
            'Insn': Insn, 'assembler': assembler, 'Value': Value}
    execfile(resolved_tabname, ns)


    global Instruction
    Instruction <<= Or(Group(InstructionPatternToParseElement(k, v))
        for k, v in assembler.InstructionSet)

    assembler.run(program, filename)
    max_insn = max(assembler.rom.keys())
    rom = [assembler.rom.get(i) for i in range(max_insn + 1)]

    for i in range(0, len(rom), 8):
        print "%04x:" % i,
        for b in rom[i:i+8]:
            print "%04x" % (b or 0),
        print

if __name__ == '__main__': main()
