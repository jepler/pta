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

def nbits(b, v):
    if v >= (1<<b) or (b > 1 and v <= -(1<<(b-1))):
        raise ValueError, "%d (0x%x) doesn't fit in %d bits" % (v, v, b)
    return v & ((1<<b) - 1)
_8 = lambda v: nbits(8)

def unbits(b, v):
    if v >= (1<<b) or v < 0:
        raise ValueError, "%d (0x%x) doesn't fit in %d bits" % (v, v, b)
    return v

class BasicInstruction:
    def __init__(self, hi8, _, arg=0):
        self.hi8 = hi8
        self.arg = arg

    @property
    def length(self): return 1

    def assemble(self, assembler):
        v = assembler.symval(self.arg)
        return [(self.hi8 << 8) | nbits(self.argwidth, v)]

class I0(BasicInstruction): argwidth=0
class I7(BasicInstruction): argwidth=7
class I8(BasicInstruction): argwidth=8
class I10(BasicInstruction): argwidth=10
class I11(BasicInstruction): argwidth=11
class I16(BasicInstruction): argwidth=16


