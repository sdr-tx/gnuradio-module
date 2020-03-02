#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Mon Mar  2 19:11:41 2020
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

from gnuradio import analog
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
        self.samp_rate = samp_rate = 96000
        self.freq_sig2 = freq_sig2 = 1000
        self.freq_sig1 = freq_sig1 = 3000
        self.amp_sig2 = amp_sig2 = 1
        self.amp_sig1 = amp_sig1 = 1

        ##################################################
        # Blocks
        ##################################################
        _freq_sig2_sizer = wx.BoxSizer(wx.VERTICAL)
        self._freq_sig2_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_freq_sig2_sizer,
        	value=self.freq_sig2,
        	callback=self.set_freq_sig2,
        	label='Frequency 2',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._freq_sig2_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_freq_sig2_sizer,
        	value=self.freq_sig2,
        	callback=self.set_freq_sig2,
        	minimum=0,
        	maximum=16000,
        	num_steps=32,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_freq_sig2_sizer)
        _freq_sig1_sizer = wx.BoxSizer(wx.VERTICAL)
        self._freq_sig1_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_freq_sig1_sizer,
        	value=self.freq_sig1,
        	callback=self.set_freq_sig1,
        	label='Frequency 1',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._freq_sig1_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_freq_sig1_sizer,
        	value=self.freq_sig1,
        	callback=self.set_freq_sig1,
        	minimum=0,
        	maximum=100000,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_freq_sig1_sizer)
        _amp_sig2_sizer = wx.BoxSizer(wx.VERTICAL)
        self._amp_sig2_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_amp_sig2_sizer,
        	value=self.amp_sig2,
        	callback=self.set_amp_sig2,
        	label='Amplitud 2',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._amp_sig2_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_amp_sig2_sizer,
        	value=self.amp_sig2,
        	callback=self.set_amp_sig2,
        	minimum=-1,
        	maximum=1,
        	num_steps=200,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_amp_sig2_sizer)
        _amp_sig1_sizer = wx.BoxSizer(wx.VERTICAL)
        self._amp_sig1_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_amp_sig1_sizer,
        	value=self.amp_sig1,
        	callback=self.set_amp_sig1,
        	label='Amplitud 1',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._amp_sig1_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_amp_sig1_sizer,
        	value=self.amp_sig1,
        	callback=self.set_amp_sig1,
        	minimum=-1,
        	maximum=1,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_amp_sig1_sizer)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(samp_rate, analog.GR_SIN_WAVE, freq_sig2, amp_sig2, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_SIN_WAVE, freq_sig1, amp_sig1, 0)
        self.Mercurial_SDR_0 = Mercurial_SDR.Mercurial_SDR('pam', 'bpsk', 1000000, 100000, 2, 'natural_key', 'linear_key', 100,8,'pll_120','pll_120','pll_120','pll_60')

        ##################################################
        # Connections
        ##################################################
        self.connect((self.Mercurial_SDR_0, 0), (self.blocks_null_sink_0, 0))    
        self.connect((self.analog_sig_source_x_0, 0), (self.Mercurial_SDR_0, 0))    
        self.connect((self.analog_sig_source_x_0_0, 0), (self.Mercurial_SDR_0, 1))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_freq_sig2(self):
        return self.freq_sig2

    def set_freq_sig2(self, freq_sig2):
        self.freq_sig2 = freq_sig2
        self._freq_sig2_slider.set_value(self.freq_sig2)
        self._freq_sig2_text_box.set_value(self.freq_sig2)
        self.analog_sig_source_x_0_0.set_frequency(self.freq_sig2)

    def get_freq_sig1(self):
        return self.freq_sig1

    def set_freq_sig1(self, freq_sig1):
        self.freq_sig1 = freq_sig1
        self._freq_sig1_slider.set_value(self.freq_sig1)
        self._freq_sig1_text_box.set_value(self.freq_sig1)
        self.analog_sig_source_x_0.set_frequency(self.freq_sig1)

    def get_amp_sig2(self):
        return self.amp_sig2

    def set_amp_sig2(self, amp_sig2):
        self.amp_sig2 = amp_sig2
        self._amp_sig2_slider.set_value(self.amp_sig2)
        self._amp_sig2_text_box.set_value(self.amp_sig2)
        self.analog_sig_source_x_0_0.set_amplitude(self.amp_sig2)

    def get_amp_sig1(self):
        return self.amp_sig1

    def set_amp_sig1(self, amp_sig1):
        self.amp_sig1 = amp_sig1
        self._amp_sig1_slider.set_value(self.amp_sig1)
        self._amp_sig1_text_box.set_value(self.amp_sig1)
        self.analog_sig_source_x_0.set_amplitude(self.amp_sig1)


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
