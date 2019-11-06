#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
import subprocess
import shlex
import serial

from gnuradio import gr

class Mercurial_SDR(gr.sync_block):
    """
    docstring for block Mercurial_SDR
    """
    def __init__(self,bits_key):
        gr.sync_block.__init__(self,
            name="Mercurial_SDR",
            in_sig=[numpy.float32],
            out_sig=[numpy.float32])

        # subprocess.call('icepll')
        # subprocess.call('echo "HOLA\n"', shell=True)

        #ser = serial.Serial('/dev/pts/13')  # open serial port
        #print(ser.name)         # check which port was really used
        #ser.write(b'hello')     # write a string
        #ser.close()             # close port
        #ser.baudrate = 9600
        #print(ser.baudrate)
        # subprocess.call(['echo', 'sin invocar shell\n'])
        #self.modulation = modulation_key
        #print(self.modulation)
        #print("MOD")
        var ='hola'
        value = 10

        # open file and write header
        f = open("/home/agustin/Dropbox/0_2019/PF_2019/sdr-tx/hdl/inc/module_params.v","w+")
        f.write("`ifndef __PROJECT_CONFIG_V\n`define __PROJECT_CONFIG_V\n\n")
        f.write("`define AM_CLKS_PER_PWM_STEP %d\n" % 1)
        f.write("`define AM_PWM_STEP_PER_SAMPLE %d\n" % 63)
        f.write("`define AM_BITS_PER_SAMPLE %d\n" % bits_key)
        f.write("\n`endif")
        f.close()

        subprocess.call('/home/agustin/Dropbox/0_2019/PF_2019/sdr-tx/hdl/syn/run_in_docker.sh make')
        subprocess.call('/home/agustin/Dropbox/0_2019/PF_2019/sdr-tx/hdl/syn/run_in_docker.sh make prog')



    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>
        out[:] = in0

        return len(output_items[0])

    def set_modulation(self,modulation_key):
        self.modulation = modulation_key
        print("modulationaaaa")
        print(self.modulation)

        