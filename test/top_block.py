#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Sun Mar  1 03:08:53 2020
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
from gnuradio.wxgui import forms
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
        self.variable_slider_3 = variable_slider_3 = 500e-3
        self.variable_slider_1 = variable_slider_1 = 1
        self.variable_slider_0 = variable_slider_0 = 500
        self.samp_rate = samp_rate = 32e3

        ##################################################
        # Blocks
        ##################################################
        _variable_slider_3_sizer = wx.BoxSizer(wx.VERTICAL)
        self._variable_slider_3_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_variable_slider_3_sizer,
        	value=self.variable_slider_3,
        	callback=self.set_variable_slider_3,
        	label='slider_gain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._variable_slider_3_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_variable_slider_3_sizer,
        	value=self.variable_slider_3,
        	callback=self.set_variable_slider_3,
        	minimum=0,
        	maximum=1,
        	num_steps=10,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_variable_slider_3_sizer)
        _variable_slider_1_sizer = wx.BoxSizer(wx.VERTICAL)
        self._variable_slider_1_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_variable_slider_1_sizer,
        	value=self.variable_slider_1,
        	callback=self.set_variable_slider_1,
        	label='slider_amp',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._variable_slider_1_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_variable_slider_1_sizer,
        	value=self.variable_slider_1,
        	callback=self.set_variable_slider_1,
        	minimum=0,
        	maximum=1,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_variable_slider_1_sizer)
        _variable_slider_0_sizer = wx.BoxSizer(wx.VERTICAL)
        self._variable_slider_0_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_variable_slider_0_sizer,
        	value=self.variable_slider_0,
        	callback=self.set_variable_slider_0,
        	label='slider_freq',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._variable_slider_0_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_variable_slider_0_sizer,
        	value=self.variable_slider_0,
        	callback=self.set_variable_slider_0,
        	minimum=0,
        	maximum=25000,
        	num_steps=25,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_variable_slider_0_sizer)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('/home/leandro/Descargas/Rata Blanca - La Leyenda del Hada y el Mago(1).wav', True)
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_float*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((variable_slider_3, ))
        self.Mercurial_SDR_0 = Mercurial_SDR.Mercurial_SDR('am', 'bpsk', 468000, 32000, 2, 'natural_key', 'linear_key', 50,7,'pll_240','pll_240','pll_120','pll_60')

        ##################################################
        # Connections
        ##################################################
        self.connect((self.Mercurial_SDR_0, 0), (self.blocks_null_sink_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.Mercurial_SDR_0, 0))    
        self.connect((self.blocks_null_source_0, 0), (self.Mercurial_SDR_0, 1))    
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_multiply_const_vxx_0, 0))    

    def get_variable_slider_3(self):
        return self.variable_slider_3

    def set_variable_slider_3(self, variable_slider_3):
        self.variable_slider_3 = variable_slider_3
        self._variable_slider_3_slider.set_value(self.variable_slider_3)
        self._variable_slider_3_text_box.set_value(self.variable_slider_3)
        self.blocks_multiply_const_vxx_0.set_k((self.variable_slider_3, ))

    def get_variable_slider_1(self):
        return self.variable_slider_1

    def set_variable_slider_1(self, variable_slider_1):
        self.variable_slider_1 = variable_slider_1
        self._variable_slider_1_slider.set_value(self.variable_slider_1)
        self._variable_slider_1_text_box.set_value(self.variable_slider_1)

    def get_variable_slider_0(self):
        return self.variable_slider_0

    def set_variable_slider_0(self, variable_slider_0):
        self.variable_slider_0 = variable_slider_0
        self._variable_slider_0_slider.set_value(self.variable_slider_0)
        self._variable_slider_0_text_box.set_value(self.variable_slider_0)

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
