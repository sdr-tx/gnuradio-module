#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Hackrfone Am Rx 8Msps
# Generated: Sun Mar  1 23:20:28 2020
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
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import numbersink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import time
import wx


class HackRFOne_AM_Rx_8MSpS(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Hackrfone Am Rx 8Msps")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 8e6
        self.ppm = ppm = 0
        self.freq = freq = 472e3
        self.fi = fi = 200e3
        self.RF_Gain = RF_Gain = 0
        self.FI_Gain = FI_Gain = 10
        self.FI_BWD = FI_BWD = 10e3
        self.BandWidth = BandWidth = 0
        self.BB_Gain = BB_Gain = 20
        self.Audio_Gain = Audio_Gain = 5

        ##################################################
        # Blocks
        ##################################################
        _ppm_sizer = wx.BoxSizer(wx.VERTICAL)
        self._ppm_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_ppm_sizer,
        	value=self.ppm,
        	callback=self.set_ppm,
        	label='Freq. Corr. [ppm]',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._ppm_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_ppm_sizer,
        	value=self.ppm,
        	callback=self.set_ppm,
        	minimum=-10,
        	maximum=10,
        	num_steps=200,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_ppm_sizer, 1, 1, 1, 1)
        self.notebook_0 = self.notebook_0 = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "RF")
        self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "FI")
        self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "AF")
        self.Add(self.notebook_0)
        _freq_sizer = wx.BoxSizer(wx.VERTICAL)
        self._freq_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_freq_sizer,
        	value=self.freq,
        	callback=self.set_freq,
        	label='Frequency',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._freq_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_freq_sizer,
        	value=self.freq,
        	callback=self.set_freq,
        	minimum=400e3,
        	maximum=1.2e6,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_freq_sizer, 1, 0, 1, 1)
        self._RF_Gain_chooser = forms.button(
        	parent=self.GetWin(),
        	value=self.RF_Gain,
        	callback=self.set_RF_Gain,
        	label='RF Amp',
        	choices=[0, 8],
        	labels=['0 dB', '13 dB'],
        )
        self.GridAdd(self._RF_Gain_chooser, 0, 0, 1, 1)
        _FI_Gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._FI_Gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_FI_Gain_sizer,
        	value=self.FI_Gain,
        	callback=self.set_FI_Gain,
        	label='Rx FI Gain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._FI_Gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_FI_Gain_sizer,
        	value=self.FI_Gain,
        	callback=self.set_FI_Gain,
        	minimum=0,
        	maximum=47,
        	num_steps=47,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_FI_Gain_sizer, 0, 1, 1, 1)
        _FI_BWD_sizer = wx.BoxSizer(wx.VERTICAL)
        self._FI_BWD_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_FI_BWD_sizer,
        	value=self.FI_BWD,
        	callback=self.set_FI_BWD,
        	label='FI Bandwidth',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._FI_BWD_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_FI_BWD_sizer,
        	value=self.FI_BWD,
        	callback=self.set_FI_BWD,
        	minimum=500,
        	maximum=20e3,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_FI_BWD_sizer, 1, 3, 1, 1)
        self._BandWidth_chooser = forms.drop_down(
        	parent=self.GetWin(),
        	value=self.BandWidth,
        	callback=self.set_BandWidth,
        	label='Bandwidth',
        	choices=[0, 1.75e6, 20e6],
        	labels=['Auto', '1.75 MHz', '20 MHz'],
        )
        self.GridAdd(self._BandWidth_chooser, 0, 3, 1, 1)
        _BB_Gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._BB_Gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_BB_Gain_sizer,
        	value=self.BB_Gain,
        	callback=self.set_BB_Gain,
        	label='Base Band Gain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._BB_Gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_BB_Gain_sizer,
        	value=self.BB_Gain,
        	callback=self.set_BB_Gain,
        	minimum=0,
        	maximum=62,
        	num_steps=31,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_BB_Gain_sizer, 0, 2, 1, 1)
        _Audio_Gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._Audio_Gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_Audio_Gain_sizer,
        	value=self.Audio_Gain,
        	callback=self.set_Audio_Gain,
        	label='Audio Gain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._Audio_Gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_Audio_Gain_sizer,
        	value=self.Audio_Gain,
        	callback=self.set_Audio_Gain,
        	minimum=0,
        	maximum=10,
        	num_steps=50,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_Audio_Gain_sizer, 1, 2, 1, 1)
        self.wxgui_numbersink2_0 = numbersink2.number_sink_f(
        	self.GetWin(),
        	unit='Unidades',
        	minval=0,
        	maxval=2,
        	factor=1.0,
        	decimal_places=2,
        	ref_level=0,
        	sample_rate=samp_rate,
        	number_rate=2,
        	average=False,
        	avg_alpha=0.5,
        	label='RMS de Entrada',
        	peak_hold=False,
        	show_gauge=True,
        )
        self.GridAdd(self.wxgui_numbersink2_0.win, 2, 0, 1, 4)
        self.wxgui_fftsink2_0_1 = fftsink2.fft_sink_c(
        	self.notebook_0.GetPage(0).GetWin(),
        	baseband_freq=freq,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=True,
        	avg_alpha=0.5,
        	title='FFT Plot',
        	peak_hold=False,
        	size=(800,400),
        )
        self.notebook_0.GetPage(0).Add(self.wxgui_fftsink2_0_1.win)
        self.wxgui_fftsink2_0_0_0_0 = fftsink2.fft_sink_f(
        	self.notebook_0.GetPage(2).GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=32000,
        	fft_size=1024,
        	fft_rate=15,
        	average=True,
        	avg_alpha=0.2,
        	title='AF',
        	peak_hold=False,
        	size=(800,500),
        )
        self.notebook_0.GetPage(2).Add(self.wxgui_fftsink2_0_0_0_0.win)
        self.wxgui_fftsink2_0_0_0 = fftsink2.fft_sink_c(
        	self.notebook_0.GetPage(1).GetWin(),
        	baseband_freq=fi,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate/80,
        	fft_size=1024,
        	fft_rate=15,
        	average=True,
        	avg_alpha=0.2,
        	title='FI',
        	peak_hold=False,
        	size=(800,500),
        )
        self.notebook_0.GetPage(1).Add(self.wxgui_fftsink2_0_0_0.win)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=8,
                decimation=25,
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(freq+fi, 0)
        self.osmosdr_source_0.set_freq_corr(ppm, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(True, 0)
        self.osmosdr_source_0.set_gain(RF_Gain, 0)
        self.osmosdr_source_0.set_if_gain(FI_Gain, 0)
        self.osmosdr_source_0.set_bb_gain(BB_Gain, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(BandWidth, 0)
          
        self.low_pass_filter_0 = filter.fir_filter_ccf(80, firdes.low_pass(
        	1, samp_rate, FI_BWD/2, samp_rate/2500, firdes.WIN_HAMMING, 6.76))
        self.dc_blocker_xx_0 = filter.dc_blocker_ff(160, True)
        self.blocks_rms_xx_0 = blocks.rms_cf(0.0001)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((Audio_Gain, ))
        self.audio_sink_0 = audio.sink(32000, '', True)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, fi, 1, 0)
        self.analog_am_demod_cf_0 = analog.am_demod_cf(
        	channel_rate=samp_rate/80,
        	audio_decim=1,
        	audio_pass=5000,
        	audio_stop=7000,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_am_demod_cf_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.wxgui_fftsink2_0_1, 0))    
        self.connect((self.blocks_rms_xx_0, 0), (self.wxgui_numbersink2_0, 0))    
        self.connect((self.dc_blocker_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.dc_blocker_xx_0, 0), (self.wxgui_fftsink2_0_0_0_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_am_demod_cf_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.wxgui_fftsink2_0_0_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.blocks_rms_xx_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.dc_blocker_xx_0, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_fftsink2_0_1.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_0_0_0.set_sample_rate(self.samp_rate/80)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.FI_BWD/2, self.samp_rate/2500, firdes.WIN_HAMMING, 6.76))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_ppm(self):
        return self.ppm

    def set_ppm(self, ppm):
        self.ppm = ppm
        self._ppm_slider.set_value(self.ppm)
        self._ppm_text_box.set_value(self.ppm)
        self.osmosdr_source_0.set_freq_corr(self.ppm, 0)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self._freq_slider.set_value(self.freq)
        self._freq_text_box.set_value(self.freq)
        self.wxgui_fftsink2_0_1.set_baseband_freq(self.freq)
        self.osmosdr_source_0.set_center_freq(self.freq+self.fi, 0)

    def get_fi(self):
        return self.fi

    def set_fi(self, fi):
        self.fi = fi
        self.wxgui_fftsink2_0_0_0.set_baseband_freq(self.fi)
        self.osmosdr_source_0.set_center_freq(self.freq+self.fi, 0)
        self.analog_sig_source_x_0.set_frequency(self.fi)

    def get_RF_Gain(self):
        return self.RF_Gain

    def set_RF_Gain(self, RF_Gain):
        self.RF_Gain = RF_Gain
        self._RF_Gain_chooser.set_value(self.RF_Gain)
        self.osmosdr_source_0.set_gain(self.RF_Gain, 0)

    def get_FI_Gain(self):
        return self.FI_Gain

    def set_FI_Gain(self, FI_Gain):
        self.FI_Gain = FI_Gain
        self._FI_Gain_slider.set_value(self.FI_Gain)
        self._FI_Gain_text_box.set_value(self.FI_Gain)
        self.osmosdr_source_0.set_if_gain(self.FI_Gain, 0)

    def get_FI_BWD(self):
        return self.FI_BWD

    def set_FI_BWD(self, FI_BWD):
        self.FI_BWD = FI_BWD
        self._FI_BWD_slider.set_value(self.FI_BWD)
        self._FI_BWD_text_box.set_value(self.FI_BWD)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.FI_BWD/2, self.samp_rate/2500, firdes.WIN_HAMMING, 6.76))

    def get_BandWidth(self):
        return self.BandWidth

    def set_BandWidth(self, BandWidth):
        self.BandWidth = BandWidth
        self._BandWidth_chooser.set_value(self.BandWidth)
        self.osmosdr_source_0.set_bandwidth(self.BandWidth, 0)

    def get_BB_Gain(self):
        return self.BB_Gain

    def set_BB_Gain(self, BB_Gain):
        self.BB_Gain = BB_Gain
        self._BB_Gain_slider.set_value(self.BB_Gain)
        self._BB_Gain_text_box.set_value(self.BB_Gain)
        self.osmosdr_source_0.set_bb_gain(self.BB_Gain, 0)

    def get_Audio_Gain(self):
        return self.Audio_Gain

    def set_Audio_Gain(self, Audio_Gain):
        self.Audio_Gain = Audio_Gain
        self._Audio_Gain_slider.set_value(self.Audio_Gain)
        self._Audio_Gain_text_box.set_value(self.Audio_Gain)
        self.blocks_multiply_const_vxx_0.set_k((self.Audio_Gain, ))


def main(top_block_cls=HackRFOne_AM_Rx_8MSpS, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
