# -*- python coding: utf-8 -*-
#
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

from pyparsing import *

if not hasattr(Forward, "__ilshift__"):
    Forward.__ilshift__ = Forward.__lshift__
PLUS = (None, 1)
STAR = (None, None)

Identifier = Word( srange("[a-zA-Z_]"), srange("[a-zA-Z0-9_]") )

CharConstant = Regex(r"'(\\.|.)'").setParseAction(
    lambda toks: [str(ord(eval(toks[0])))])
BinaryNumberPrefix = Regex("%[01]+").setParseAction(
    lambda toks: [str(int(toks[0][1:], 2))])
BinaryNumberSuffix = Regex("[01]+[bB]").setParseAction(
    lambda toks: [str(int(toks[0][:-1], 2))])

OctalNumberPrefix = Regex("@[0-7]+").setParseAction(
    lambda toks: [str(int(toks[0][1:], 8))])
OctalNumberSuffix = Regex("[0-7]+[oO]").setParseAction(
    lambda toks: [str(int(toks[0][:-1], 8))])

DecimalNumberSuffix = Regex("[0-9]+").setParseAction(
    lambda toks: [str(int(toks[0], 10))])
DecimalNumberNeutral = Regex("[0-9]+[dD]").setParseAction(
    lambda toks: [str(int(toks[0][:-1], 10))])

HexNumberPrefix = Regex("\$[0-9a-fA-f]+").setParseAction(
    lambda toks: [str(int(toks[0][1:], 16))])
HexNumberSuffix = Regex("[0-9][0-9a-fA-F]*[hH]").setParseAction(
    lambda toks: [str(int(toks[0][:-1], 16))])

Number = (CharConstant ^ BinaryNumberPrefix ^ BinaryNumberSuffix ^ OctalNumberPrefix ^
    OctalNumberSuffix ^ DecimalNumberSuffix ^
    HexNumberPrefix ^ HexNumberSuffix ^ DecimalNumberNeutral)

Colon = Literal(":")
Label = Identifier.copy().setParseAction(
    lambda s, loc, toks: toks[0]).setResultsName("label")

Expression = Forward().setName("expression")
Value = Number | Identifier | ('(' + Expression + ')')
Product = Value + (Word('*/', max=1) + Value) * STAR
Sum = Product + (Word('-+', max=1) + Product) * STAR
PyExpression = QuotedString("`", escChar="\\", unquoteResults=True)
Expression <<= Sum | PyExpression

PyCode = QuotedString("```", escChar="\\", unquoteResults=True
    ).setResultsName("pycode")
Assignment = (Identifier.setResultsName("id") + "equ" + Combine(Expression).setResultsName("expr")
    ).setResultsName("assignment")

OpaquePart = Regex('[a-zA-Z0-9_]+|[^\s*,]')
Instruction = Identifier + (OpaquePart | "," | "*")*STAR

def CILiteral(s): return Keyword(s, "", True)

def InstructionPatternToParseElement(s, f):
    p = Instruction.parseString(s, True)
    indices = [0]
    parts = []
    for i, si in enumerate(p):
        if si == "*":
            indices.append(i)
            parts.append(Combine(Expression))
        elif i == 0:
            parts.append(Keyword(si, caseless=True))
        else:
            parts.append(CILiteral(si))

    def extractparts(s, l, toks):
        return f(*(toks[i] for i in indices))
    rule = And(parts)
    # setParseAction's wrapper balls us up real bad
    rule.parseAction = [extractparts]
    return rule
