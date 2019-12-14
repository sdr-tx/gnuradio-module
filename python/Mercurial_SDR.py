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

import numpy as np
import subprocess
import shlex
import serial
#from math import pi, sin
#import argparse

from gnuradio import gr

class Mercurial_SDR(gr.sync_block):
    """
    docstring for block Mercurial_SDR
    """
    def __init__(self, modulation_key,psk_key,fc_key,fs_key,clk_key,pammethod_key,pamtype_key,duty_key):
        gr.sync_block.__init__(self,
            name="Mercurial_SDR",
            in_sig=[np.float32, np.float32],
            out_sig=[np.float32])

        # Atributos
        self.modulation  = modulation_key;
        self.fc = fc_key
        self.fs = fs_key
        self.duty = duty_key
        self.pam_methode = pammethod_key
        self.syntethize = True

        # subprocess.call('icepll')

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
        print("INIT")


        
        modulation_psk  = psk_key;      # ?
        parameter01 = 1;
        parameter02 = 255;
        parameter03 = 8;
        parameter04 = 4;

        try:
            f = open("check_syn","r")
            rl = f.readline()
            current = "{}{}{}{}{}{}{}{}".format(modulation_key,psk_key,fc_key,fs_key,clk_key,pammethod_key,pamtype_key,duty_key)
            print("TRY")

            if (rl == current):
                self.syntethize = False
            else:
              f.close()
              f = open("check_syn","w+")
              f.write("{}{}{}{}{}{}{}{}".format(modulation_key,psk_key,fc_key,fs_key,clk_key,pammethod_key,pamtype_key,duty_key))
   
        except:
            print("[DEBUG] | Running exception code: the \"check_syn\" file doesn't exist")
            f = open("check_syn","w+")
            f.write("{}{}{}{}{}{}{}{}".format(modulation_key,psk_key,fc_key,fs_key,clk_key,pammethod_key,pamtype_key,duty_key))
            f.close()
            print("except")

     #  HDL code
         #.PARAMETER01    (`PARAMETER01),
         #.PARAMETER02    (`PARAMETER02),
         #.PARAMETER03    (`PARAMETER03),
         #.PARAMETER04    (`PARAMETER04)

         #/*  AM_CLKS_PER_PWM_STEP    1
         # *  AM_PWM_STEP_PER_SAMPLE  255
         # *  AM_BITS_PER_SAMPLE      8
         # *  AM_REPEATED_SAMPLE      30
         # */

         #/*  AM_CLKS_PER_PWM_STEP    1
         # *  AM_PWM_STEP_PER_SAMPLE  255
         # *  AM_BITS_PER_SAMPLE      8
         # *  AM_REPEATED_SAMPLE      30
         # */

         #/*  PSK_CLKS_PER_BIT        4
         # *  PSK_BITS_PER_SYMBOL     4
         # *
         # *  PSK_REPEATED_SAMPLE     30
         # */
 
         #/*  PAM_CLKS_SAMPLING_FREQ  1200
         # *  PAM_CLKS_PER_BCLK       12
         # *  PAM_DATA_LENGHT         24
         # *  
         # */
        print("INIT 2")


        if(self.syntethize == True): 
            print("syntethize")

            if(self.modulation == "am"):
                parameter01 = 1
                parameter02 = 255
                parameter03 = 8
                parameter04 = np.round(fc_key/fs_key);
                print("[INFO] | AM modulation is set");
    
            elif(self.modulation == "ook"):
                parameter02 = 2;
                print("[INFO] | OOK modulation is set");
    
            elif(self.modulation == "pam"):
                parameter01 = 1200
                parameter02 = 24;
                parameter03 = 24;                               # bits del dac
                print("[INFO] | PAM modulation is set");
    
            elif(psk_key == "bpsk"):
                parameter01 = clk_key;
                parameter02 = 2;
                parameter04 = np.round(clk_key/fs_key);
                print("[INFO] | BPSK modulation is set");
    
            elif(psk_key == "qpsk"):
                parameter01 = clk_key;
                parameter02 = 4;
                parameter04 = np.round(clk_key/fs_key);
                print("[INFO] | QPSK modulation is set");
    
            elif(psk_key == "8psk"):
                parameter01 = clk_key;
                parameter02 = 8;
                parameter04 = np.round(clk_key/fs_key)        
                print("[INFO] | 8-PSK modulation is set");
    
            # Descomentar para programar la FPGA
            self.modulatorParametersGenerator(parameter01, parameter02, parameter03,parameter04)
            
            # Dos rutas diferentes de lo mismo. Depende si corrés desde docker o a pedal
            self.programFPGA("../../syn", "all")           # From docker
            #self.programFPGA("../../hdl/syn", "all")        # A pedal


#        data = [6 0]#, 3, 9, 12] 
        print("BEFORE SERIAL 2")

        self.tty = serial.Serial('/dev/ttyUSB1')
        
        print("AFTER SERIAL 2")


    def work(self, input_items, output_items):
        in0 = input_items[0]
        in1 = input_items[1]
        #print("[DEBUG] | fc = {}, fs = {} fc/fs = {}".format(self.fc, self.fs, self.fc/self.fs))
        
        if(self.modulation == "pam"):
            self.pam_processing(in0, in1)

        else:
            print("[DEBUG] | in0 len = ", len(in0))
            b = np.uint8(in0*127-128)
            self.tty.write(b.tobytes())

        # print(type(in0),  " | ", in0)
        # out = output_items[0]
        # # <+signal processing here+>
        # out[:] = in0
        # tty.write(input_items)
        #return

        return len(output_items[0])


    def set_modulation(self, modulation_key):
        self.modulation = modulation_key
        print("Modulacion seleccionada:")
        print(self.modulation)

    ####
    # programFPGA
    #
    # This function runs the Makefile to make the synthesys, place and route and
    # programmation of the FPGA
    ####
    def programFPGA(self, pathMakefileHDL, target):
        subprocess.call(['make', '-C', pathMakefileHDL,'clean'])
        subprocess.call(['make', '-C', pathMakefileHDL, target, 'MOD={}'.format(self.modulation)])
        subprocess.call(['make', '-C', pathMakefileHDL, target, 'prog'])

    ####
    # modulatorParametersGenerator
    #
    # Used to write the necessary defines to build every modulator
    ####
    def modulatorParametersGenerator(self, parameter01, parameter02, parameter03,parameter04):
        # open file and write header
        f = open("../../inc/module_params.v","w+")
        #f = open("../../hdl/inc/module_params.v","w+")
        f.write("`ifndef __PROJECT_CONFIG_V\n`define __PROJECT_CONFIG_V\n\n")
        f.write("`define PARAMETER01 %d\n" % parameter01)
        f.write("`define PARAMETER02 %d\n" % parameter02)
        f.write("`define PARAMETER03 %d\n" % parameter03)
        f.write("`define PARAMETER04 %d\n" % parameter04)
        f.write("`define CLK_PERIOD %d\n" % 4)
        f.write("\n`endif")
        f.close()



    def pam_processing(self, in0, in1):

        if(self.pam_methode == "natural_key"):

            # print("Corriendo código no optimizado")
            b = np.uint8(in0*127+128)
            for n in range(len(b)):                     # Esa relación creo que debería hacerse con un define
                if(n%12 > 12*self.duty/100):            # 12 <-- 12.5 = Tframe / Ts = 125us / 10us = 125us * 100kHz = 125us * fs
                    b[n] = 0           

            # print("Corriendo código optimizado")    # Ese código se supone que es más performante
            # b = np.zeros(len(in0), dtype=np.uint8)    # pero no anda correctamente: cada tanto salen por 
            # for n in range(len(b)):                   # el DAC valores constantes.
            #     if(n%12 <= 12*self.duty/100):
            #         b[n] = np.uint8(in0[n]*127+128)
                 
        else:                                           # Flat-top
            b = np.zeros(len(in0), dtype=np.uint8)    # pero no anda correctamente: cada tanto salen por 
            for n in range(len(b)):                   # el DAC valores constantes.
                if(n%12 == 0):
                    instant_sample = np.uint8(in0[n]*127+128)
                if(n%12 <= 12*self.duty/100):
                    b[n] = instant_sample

        self.tty.write(b.tobytes()) 

