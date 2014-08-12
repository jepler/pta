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
import collections
import struct

from pta.grammar import *

OptLabel = ((White() * PLUS)) ^ (Label + Optional(Colon))
OptArgs = Optional(Regex(r"([^;'\\]|\\.|'\\.'|'[^\\']')+")).setResultsName("args")
OptComment = Regex(r"\s*(;.*)?")

Mnemonic = Identifier.copy().setResultsName("mnemonic")
Directive = Word( ".", srange("[a-zA-Z0-9_]") ).setResultsName("pseudoop")


class Instruction:
    def __init__(self, op, args):
        self.op = op
        self.args = args

    def __str__(self): return "Instruction(%r, %r)" % (self.op, self.args)

    def length(self): return 1
    def assemble(self): return 0

class Pseudo:
    def __init__(self, op, args):
        self.op = op
        self.attr = "pseudo_" + self.op[1:]
        self.args = args
    def __str__(self): return "Pseudo(%r, %r)" % (self.op, self.args)

    def __call__(self, assembler, no, label):
        func = getattr(assembler, self.attr)
        return func(no, label, self.args)

class Assembler(object):
    def __init__(self):
        self.InstructionSet = collections.defaultdict(list)
        self.irules = {}

        Instr = ((Mnemonic + OptArgs).setResultsName("instruction")
                .setRawParseAction(self.parse_instr))
        Pseudo = ((Directive + OptArgs).setResultsName("pseudo")
                .setRawParseAction(self.parse_pseudo))
        IP = Optional(Instr ^ Pseudo)

        self.Grammar = (
            (White() + IP + OptComment) ^
            (Identifier.copy().setResultsName("label") + Optional(Colon) + IP + OptComment) ^
            OptComment)

        self.msfirst = False

    def exprlist(self, exprs):
        exprs = ValueList.parseString(exprs, True)
        return map(self.value, exprs[::2])

    def expr(self, expr):
        return self.value(Value.parseString(expr, True).value)

    def assignexpr(self, label, expr):
        self.assign(label, self.expr(expr))

    def pseudo_equ(self, no, label, expr):
        if no == 1: self.assignexpr(label, expr)

    def pseudo_org(self, no, label, expr):
        value = self.expr(expr)
        if no == 1 and label:
            self.assign(label, value)
        self.addr = value

    def pseudo_word(self, no, label, expr):
        if no == 1: return
        values = self.exprlist(expr)
        for addr, value in enumerate(values, self.addr):
            if not self.msfirst:
                value = struct.unpack("<H", struct.pack(">H", value))[0]
            self.rom[addr] = value
        self.addr += len(values)
    pseudo_dw = pseudo_word

    def pseudo_msfirst(self, no, label, expr):
        self.msfirst = True
    def pseudo_lsfirst(self, no, label, expr):
        self.msfirst = False

    def pseudo_end(self, no, label, expr):
        Empty().parseString(expr, True)
        pass # should touch flow control

    def makeirule(self, v):
        if not v in self.irules:
            self.irules[v] = MatchFirst([
                InstructionPatternToParseElement(func, func.pattern)
                    for func in self.InstructionSet[v]])
        return self.irules[v]

    def parse_instr(self, s, l, toks):
        try:
            rule = self.makeirule(toks.mnemonic.lower())
        except KeyError:
            self.error(self.lno, "No instructions matching %r" % toks.mnemonic)
        r = rule.parseString(toks.args, True)
        return [r]

    def parse_pseudo(self, s, l, toks):
        return [Pseudo(toks.pseudoop, toks.args)]

    def run(self, program, filename):
        self.rom = {}
        self.symbols = {}

        self.input(program, filename)
        # self.macro()
        self.pass1()
        self.pass2()

    def input_line(self, lno, line):
        self.lno = lno
        print "%s: %s" % (lno, line)
        p = self.Grammar.parseString(line, True)
        return lno, p

    def input(self, program, filename):
        self.filename = filename
        self.program = [self.input_line(i+1, line)
            for i, line in enumerate(program.split("\n"))]

    def value(self, expr):
        if not expr: return 0
        return eval(expr, self.symbols)

    def assign(self, name, value):
        print '# assign', name, repr(value)
        self.symbols[name] = value

    def error(self, lno, err):
        print "%s:%d: %s" % (self.filename, lno, err)
        raise SystemExit

    def flow_control(self):
        for i in range(0, len(self.program)):
            lno, line = self.program[i]
            self.symbols['__lno__'] = lno
            yield line

    @property
    def lno(self):
        return self.symbols['__lno__']
    @lno.setter
    def lno(self, v):
        self.symbols['__lno__'] = v

    @property
    def passno(self):
        return self.symbols['__passno__']

    @property
    def addr(self):
        return self.symbols['__addr__']

    @addr.setter
    def addr(self, v):
        self.symbols['__addr__'] = v

    @property
    def filename(self):
        return self.symbols['__filename__']

    @filename.setter
    def filename(self, v):
        self.symbols['__filename__'] = v

    def pass1(self):
        self.symbols['__passno__'] = 1
        self.addr = 0

        for line in self.flow_control():
            if line.label:
                self.assign(line.label, self.addr)
            if line.pseudo:
                line.pseudo[0](self, 1, line.label)
            if line.instruction:
                self.addr += line.instruction[0].length

    def pass2(self):
        self.symbols['__passno__'] = 2
        self.addr = 0

        for line in self.flow_control():
            if line.pseudo:
                line.pseudo[0](self, 2, line.label)
            if line.instruction:
                op = line.instruction[0].assemble(self)
                if isinstance(op, int): op = [op]
                for addr, opc in enumerate(op, self.addr):
                    self.rom[self.addr] = opc
                self.addr += len(op)
                print self.addr

    def read_table(self, tabname):
        def Insn(a, b, *args, **kw):
            def inner(*toks):
                if toks is None: return
                return b(*args + (a,) + toks,  **kw)
            inner.func_name = a
            a = a.split(None, 1)
            if len(a) == 1: a, o = a[0], ''
            else: a, o = a
            inner.pattern = o
            self.InstructionSet[a.lower()].append(inner)

        resolved_tabname = resolve(tabname, os.curdir, os.path.dirname(pta.__file__), os.path.dirname(__file__))
        ns = {'__name__': os.path.splitext(os.path.basename(tabname))[0],
              '__file__': resolved_tabname,
                'Insn': Insn, 'assembler': self, 'Value': self.value}
        execfile(resolved_tabname, ns)

        def key(inner):
            pattern = inner.pattern
            return -len(pattern), pattern.count("*"), pattern
        def order(v): return sorted(v, key=key)
        for k in sorted(self.InstructionSet.keys()):
            self.InstructionSet[k] = order(self.InstructionSet[k])

        self.irules.clear()

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

    assembler.read_table(tabname)

    assembler.run(program, filename)
    max_insn = max(assembler.rom.keys())
    rom = [assembler.rom.get(i) for i in range(max_insn + 1)]

    for i in range(0, len(rom), 8):
        print "%04x:" % i,
        for b in rom[i:i+8]:
            print "%04x" % (b or 0),
        print

if __name__ == '__main__': main()
