#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Thu Mar  5 01:20:21 2020
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import Mercurial_SDR
import wx


class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32e3

        ##################################################
        # Blocks
        ##################################################
        self.blocks_vector_source_x_0 = blocks.vector_source_i((0, 1,2,3), True, 1, [])
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_float*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_int_to_float_0 = blocks.int_to_float(1, 1)
        self.Mercurial_SDR_0 = Mercurial_SDR.Mercurial_SDR('psk', 'qpsk', 468000, 32000, 'natural_key', 'linear_key', 50,8,'pll_120','pll_120','pll_120','pll_60',5000000,50000,50000)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.Mercurial_SDR_0, 0), (self.blocks_null_sink_0, 0))    
        self.connect((self.blocks_int_to_float_0, 0), (self.Mercurial_SDR_0, 0))    
        self.connect((self.blocks_null_source_0, 0), (self.Mercurial_SDR_0, 1))    
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_int_to_float_0, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
