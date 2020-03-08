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

from numpy import log, zeros, abs, sign
#from math import pi, sin
#import argparse

from gnuradio import gr

# Some constants to make the code performancer
A = 87.6
INV_A = np.float32(1/A)
INV_DIV_A = 1/(1+log(A))

MU = 255
INV_ULAW_DEN = 1/log(1+MU)

class Mercurial_SDR(gr.sync_block):
    """
    docstring for block Mercurial_SDR
    """
    def __init__(self, modulation_key, psk_key, fc_key, fs_key, pammethod_key, pamtype_key, duty_key, 
                nbits_key, am_fc_8bits_key, am_fc_7bits_key, am_fc_6bits_key, am_fc_5bits_key, psk_fc_key, psk_fs5M_key, psk_fs1M_key):
        gr.sync_block.__init__(self,
            name="Mercurial_SDR",
            in_sig=[np.float32, np.float32],
            out_sig= [np.float32])

        # Atributos
        self.modulation  = modulation_key;
        self.psk_mod = psk_key
        self.fc = fc_key
        self.fs = int(fs_key)
        self.duty = duty_key
        self.pam_methode = pammethod_key
        self.pam_type = pamtype_key
        self.am_nbits = nbits_key
        self.am_fc_8bits = am_fc_8bits_key
        self.am_fc_7bits = am_fc_7bits_key
        self.am_fc_6bits = am_fc_6bits_key
        self.am_fc_5bits = am_fc_5bits_key
        self.psk_fc = psk_fc_key
        self.psk_fs = 25e3
        self.psk_fs5M = psk_fs5M_key
        self.psk_fs1M = psk_fs1M_key
        self.pll = 120
        self.synthesize = True


        # Dafault values for configuration parameters.
        parameter01 = 1;
        parameter02 = 255;
        parameter03 = 8;
        parameter04 = 4;
        modulation_number  = 0;



        # Choosing PLL
        if(self.modulation == "am"):
            if(self.am_nbits == 8):
                if(self.am_fc_8bits == "pll_50.25"):
                    self.pll = 50.25
                elif(self.am_fc_8bits == "pll_100.5"):
                    self.pll = 100.5
                elif(self.am_fc_8bits == "pll_201"):
                    self.pll = 201

            elif(self.am_nbits == 7):
                if(self.am_fc_7bits == "pll_50.25"):
                    self.pll = 50.25
                elif(self.am_fc_7bits == "pll_100.5"):
                    self.pll = 100.5
                elif(self.am_fc_7bits == "pll_201"):
                    self.pll = 201

            elif(self.am_nbits == 6):
                if(self.am_fc_6bits == "pll_50.25"):
                    self.pll = 50.25
                elif(self.am_fc_6bits == "pll_100.5"):
                    self.pll = 100.5
                elif(self.am_fc_6bits == "pll_201"):
                    self.pll = 201

            elif(self.am_nbits == 5):
                if(self.am_fc_5bits == "pll_50.25"):
                    self.pll = 50.25
                elif(self.am_fc_5bits == "pll_100.5"):
                    self.pll = 100.5

            print("[INFO] | PLL: {} MHz \n[INFO] | Bits: {}".format(self.pll, self.am_nbits))
        
        else:
            self.pll = 120
            print("[INFO] | PLL: {} MHz".format(self.pll))



        if(self.modulation == "psk"):
            if(self.psk_fc == 5e6):
                self.psk_fs = self.psk_fs5M 
            else:
                self.psk_fs = self.psk_fs1M 

        # Check routine for re-synthesis

        try:
            f = open("check_syn","r")
            rl = f.readline()
            # current = "{}{}{}{}{}{}{}{}".format(modulation_key,psk_key,fc_key,fs_key,ammethod_key,pamtype_key,duty_key)
            current = "{}{}{}{}{}{}{}{}{}".format(modulation_key, psk_key, fc_key, fs_key, nbits_key, self.pll, psk_fc_key, psk_fs5M_key , psk_fs1M_key)

            if (rl == current):
                self.synthesize = False
            else:
              f.close()
              f = open("check_syn", "w+")
              # f.write("{}{}{}{}{}{}{}{}".format(modulation_key,psk_key,fc_key,fs_key,ammethod_key,pamtype_key,duty_key))
              f.write("{}{}{}{}{}{}{}{}{}".format(modulation_key, psk_key, fc_key, fs_key, nbits_key, self.pll, psk_fc_key, psk_fs5M_key , psk_fs1M_key))
   
        except:
            print("[DEBUG] | Running exception code: the \"check_syn\" file doesn't exist")
            f = open("check_syn", "w+")
            # f.write("{}{}{}{}{}{}{}{}".format(modulation_key, psk_key, fc_key, fs_key, pammethod_key, pamtype_key, duty_key))
            f.write("{}{}{}{}{}{}{}{}{}".format(modulation_key, psk_key, fc_key, fs_key, nbits_key, self.pll, psk_fc_key, psk_fs5M_key , psk_fs1M_key))
            f.close()

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


        if(self.synthesize == True): 

            if(self.modulation == "am"):
                parameter01 = 1
                parameter02 = pow(2,self.am_nbits) -1 ;
                parameter03 = self.am_nbits;                
                modulation_number  = 1

                
                parameter04 = np.round(self.pll * 1e6 / (parameter02+1) / fs_key)-1;
                
                print("[INFO] | AM modulation is set");
    
            elif(self.modulation == "ook"):
                parameter02 = 2;

                print("[INFO] | OOK modulation is set");
    
            elif(self.modulation == "pam"):
                parameter01 = 1250                              # Divisor de frecuencia: fs = f_pll/parameter01 = 120MHz/1200 = 100kHz
                parameter02 = 12;   # VER!!!!!!!  NO SÉ SI ERA 12 O 24!!!!!!!!  Con 24 anda bien. Ver comportamiento con 12.
                parameter03 = 24;                               # Bits del DAC
                modulation_number  = 2

                print("[INFO] | PAM modulation is set");
    
            elif(self.modulation == "psk"):

                parameter04 = self.psk_fc/self.psk_fs;

                if(psk_key == "bpsk"):
                    parameter01 = 120e6/(2*self.psk_fc);
                    parameter02 = 2;
                    modulation_number = 3

                    print("[INFO] | BPSK modulation is set");
        
                elif(psk_key == "qpsk"):
                    parameter01 = 120e6/(4*self.psk_fc);
                    parameter02 = 4;
                    modulation_number = 4
                    print("[INFO] | QPSK modulation is set");
        
                elif(psk_key == "8psk"):
                    parameter01 = 120e6/(8*self.psk_fc);
                    parameter02 = 8;
                    modulation_number = 5
       
                    print("[INFO] | 8-PSK modulation is set");
    

            # Genera el archivo con los parámetros configurables de los .v
            self.modulatorParametersGenerator(parameter01, parameter02, parameter03, parameter04, modulation_number)
            
            # Descomentar para programar la FPGA
            # Dos rutas diferentes de lo mismo. Depende si corrés desde docker o a pedal
            self.programFPGA("../../syn", "all")           # From docker
            # self.programFPGA("../../hdl/syn", "all")        # A pedal


        self.tty = serial.Serial('/dev/ttyUSB1')
        

    def work(self, input_items, output_items):
        in0 = input_items[0]
        in1 = input_items[1]
        out = output_items[0]
        #out[:] = in0 + in1

        if(self.modulation == "pam"):
           b = self.pam_processing(in0, in1)

        elif(self.modulation == "psk"):
            b = self.psk_processing(in0)
        else:
            b = np.uint8(in0*127-128)
        
        self.tty.write(b.tobytes())

        # print(type(in0),  " | ", in0)
        # out = output_items[0]
        # # <+signal processing here+>
        # out[:] = in0
        # tty.write(input_items)
        #return

        return len(out)


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
        subprocess.call(['make', '-C', pathMakefileHDL, target, 'MOD={}'.format(self.modulation), 'PLL={}'.format(self.pll)])
        subprocess.call(['make', '-C', pathMakefileHDL, target, 'prog'])

    ####
    # modulatorParametersGenerator
    #
    # Used to write the necessary defines to build every modulator
    ####
    def modulatorParametersGenerator(self, parameter01, parameter02, parameter03, parameter04, modulation_number):
        # open file and write header
        f = open("../../inc/module_params.v","w+")
        #f = open("../../hdl/inc/module_params.v","w+")
        f.write("`ifndef __PROJECT_CONFIG_V\n`define __PROJECT_CONFIG_V\n\n")
        f.write("`define PARAMETER01 %d\n" % parameter01)
        f.write("`define PARAMETER02 %d\n" % parameter02)
        f.write("`define PARAMETER03 %d\n" % parameter03)
        f.write("`define PARAMETER04 %d\n" % parameter04)
        f.write("`define MODULATION %d\n" % modulation_number)
        f.write("`define CLK_PERIOD %d\n" % 4)
        f.write("\n`endif")
        f.close()



    def pam_processing(self, in0, in1):
        '''
        Método para procesar PAM. Realiza filtrado linea, ley-A, ley-u y muestreo natural o instantáneo.
        Si el duty ingresado es mayor al 50%, sólo se utilizará el canal de entrada 1.
        Recibe las dos señales de entrada en float
        Devuelve la señal PAM en uint16
        '''

        if(self.pam_type == "ulaw"):        # u-Law
            x1 = self.lin2ulaw(in0)
            x2 = self.lin2ulaw(in1)

        elif(self.pam_type == "alaw"):      # A-Law
            x1 = self.lin2alaw(in0)
            x2 = self.lin2alaw(in1)

        else:                               # Linear
            x1 = in0
            x2 = in1

        if(self.duty > 50):
            b = self.pam_processing_for_1signal(x1)
        else:
            b = self.pam_processing_for_2signals(x1,x2)

        return b                                         


    def lin2alaw(self, x):
        '''
        Método para aplicarle ley-a a la señal de entrada x
        Recibe un vector de floats.
        Devuelve un vector de floats
        '''
        
        abs_x = abs(x)                              # Obtengo el módulo de la entrada
        
        opt1 = A * abs_x * INV_DIV_A                # Obtengo un vector con los valores para los casos en que mod_x < 1/A
        opt2 = 1 + log(abs_x) * INV_DIV_A           # Obtengo un vector con los valores para los casos en que mod_x > 1/A

        y = zeros(len(x), dtype = np.float32)       # Creo un vector de ceros para guardar la salida

        i=0                                         # Seteo un contador para indexar
        for n in abs_x:                             # Inicio el algoritmo de ley-a
            if(n < INV_A):
                y[i] = opt1[i]
            else:
                y[i] = opt2[i]
            i+=1
        
        return y*sign(x)


    def lin2ulaw(self,x):
        '''
        Método para aplicarle ley-u a la señal de entrada x
        Recibe un vector de floats.
        Devuelve un vector de floats
        '''
        ulaw_num = log(1 + MU * abs(x)) 
        return sign(x) * ulaw_num * INV_ULAW_DEN


    def pam_processing_for_1signal(self, x):
        '''
        Modulación PAM para una única señal de entrada. Sale con muestreo natural o instantáneo (Flat-Top).
        Recibe un vector de floats con la señal de entrada natural o filtrada con ley-A o ley-u.
        Devuelve un vector en uint16 con la entrada en PAM.
        '''

        if(self.pam_methode == "natural_key"):              # Procesamiento para muestreo natural

            b = np.uint16(x*32767 + 32768)                  # Creo el vector de salida: es la señal de entrada de float a uint16
            for n in range(len(b)):                         
                if(n%12 > 12*self.duty/100):                # 12 <-- 12.5 = Tframe / Ts = 125us / 10us = 125us * 100kHz = 125us * fs
                    b[n] = 0                                # Si n%12 es mayor que el duty, el resto de los valores de ese fram 
                                                            # debe ser 0 
                 
        else:                                               # Procesamiento para muestreo Flat-top
            b = zeros(len(x), dtype=np.uint16)              # Creo el vector de salida (vector de 0s)
            for n in range(len(b)):                        
                if(n%12 == 0):                              # Tomo el valor instantáneo para cada frame
                    instant_sample = np.uint16(x[n]*32767+32768)
                if(n%12 < 12*self.duty/100):                # Si estoy por debajo del duty, inserto la muestra instantánea
                    b[n] = instant_sample

        return b                                            # Retorno el vector de salida



    def pam_processing_for_2signals(self,x1,x2):
        '''
        Modulación PAM para dos señales de entrada. Salen con muestreo natural o instantáneo (Flat-Top).
        Recibe dos vectores de floats con la señal de entrada natural o filtrada con ley-A o ley-u.
        Devuelve un vector en uint16 con las entradas en PAM.

        NOTA: si se compara el procesamiento que se hace para el muestro natural de una sola señal de entrada
        vs el de este método notará que aquí el código es más crudo: en vez de utilizar el operador módulo (%) se
        utiliza un contador que se resetea en cada frame. Esto fue necesario ya que al correr el código para dos señales
        con operadores módulo (%) generaba mucha demora, quedano vacía en buffer de recepción del dispositivo.
        '''

        duty = int(12*self.duty/100)                            # Tamaño del frame: utilizada para aumentar la performance en tiempo
    
        if(self.pam_methode == "natural_key"):                  # Procesamiento para muestro natural
            b1 = np.uint16(x1*32767 + 32768)                    # Convierto la señal 1 de float a int16
            b = np.uint16(x2*32767 + 32768)                     # Convierto la señal 2 de float a int16. Ese vector será la salida
            
            for n in range(len(b)):                         
                if(n%12 < duty):                                # Si por debajo del duty, pongo la señal 1 a la salida
                    b[n] = b1[n]
                elif(n%12 >= duty *2):                          # Si estoy por arriba de dos duty, la salida es 0
                    b[n] = 0
                                                                # Para los valores intermedios, la salida es la señal 2
        else:                                                   # Procesamiento para muestreo Flat-Top
            b = zeros(max(len(x1),len(x2)), dtype=np.uint16)    # Creo el vector de salida (vector de 0s)
            instant_sample_1 = np.uint16(x1[0]*32767+32768)     # Muestra instantánea de la entrada 1
            instant_sample_2 = np.uint16(x2[duty]*32767+32768)  # Muestra instantáneo de la entrada 2 (un duty después)
            
            i = 0                                               # Creo el contador
            for n in range(len(b)):                       
                if( i == 12):                                   # Si el contador llegó al ancho de frame, reseteo y tomo una nueva
                    instant_sample_1 = np.uint16(x1[n]*32767+32768)     # muestra instantánea del canal 1
                    i = 0

                elif( i == duty):                               # Si el contador llegó al ancho de duty, tomo una muestra instantánea
                    instant_sample_2 = np.uint16(x2[n]*32767+32768)     # del canal 2
                
                if(i < duty):                                   # Si el contador está por debajo del duty, la salida es la muestra
                    b[n] = instant_sample_1                     # instantánea 1
                elif(i < duty *2):                              # Si el contador está por arriba del duty y por debajo de dos dutys
                    b[n] = instant_sample_2                     # la salida es la muestra instantánea 2
                i +=1 
                                                                # En otro caso, ya está en 0 la salida
        return b



    def psk_processing(self, x):

        i = 0
        b = np.empty(len(x), dtype = np.uint8)

        if(self.psk_mod == "bpsk"):
            for n in x:
                b[i] = 0x01 if(n == 0) else 0x02
                i += 1

        elif(self.psk_mod == "qpsk"):
            for n in x:
                if(n == 0):
                    b[i] = 0x3
                elif(n == 1):
                    b[i] = 0x9
                elif(n == 2):
                    b[i] = 0xC
                else:
                    b[i] =0x6
                i +=1
        
        else:   # 8-PSK
            for n in x:
                if(n == 0):
                    b[i] = 0x0F
                elif(n == 1):
                    b[i] = 0x1E
                elif(n == 2):
                    b[i] = 0x3C
                elif(n == 3):
                    b[i] =0x78
                elif(n == 4):
                    b[i] = 0xF0
                elif(n == 5):
                    b[i] = 0xE1
                elif(n == 6):
                    b[i] =0xC3
                else:
                    b[i] =0x87
                i +=1

        return b