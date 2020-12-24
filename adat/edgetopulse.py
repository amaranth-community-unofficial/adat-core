#!/usr/bin/env python3
"""converts a rising edge to a single clock pulse"""
from nmigen import Elaboratable, Signal, Module

class EdgeToPulse(Elaboratable):
    """
        each rising edge of the signal edge_in will be
        converted to a single clock pulse on pulse_out
    """
    def __init__(self):
        self.rst_in           = Signal()
        self.edge_in          = Signal()
        self.pulse_out        = Signal()

    def elaborate(self, platform) -> Module:
        m = Module()

        edge_shift = Signal(2)

        with m.If(self.rst_in):
            m.d.sync += edge_shift.eq(0)
            m.d.comb += self.pulse_out.eq(0)

        with m.Else():
            m.d.sync += edge_shift.eq((edge_shift << 1) | self.edge_in)
            with m.If(self.edge_in & ~edge_shift):
                m.d.comb += self.pulse_out.eq(1)
            with m.Else():
                m.d.comb += self.pulse_out.eq(0)

        return m
