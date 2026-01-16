# SPDX-FileCopyrightText: © 2025 Christian Hoene
# SPDX-License-Identifier: Apache-2.0

import cocotb
import random
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_protocol_parity(dut):
    dut._log.info("protocol parity start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.debug("Reset")
    dut.ena.value = 1
    dut.rst_n.value = 0

    dut.protocol_parity_in_data.value = 1
    dut.protocol_parity_in_clk.value = 0
    dut.protocol_parity_in_sync.value = 0
    dut.protocol_parity_bits.value = 0

    await ClockCycles(dut.clk, 2)

    # check output signals
    assert dut.protocol_parity_error.value == 0

    # start
    dut._log.debug("Starting no sync")
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)

    for i in range(0, 64):
        dut.protocol_parity_bits.value = i & 0x1F
        await ClockCycles(dut.clk, 1)
        dut.protocol_parity_in_clk.value = 1
        await ClockCycles(dut.clk, 1)
        dut.protocol_parity_in_clk.value = 0
        await ClockCycles(dut.clk, 1)
        # check output signals

        assert dut.protocol_parity_error.value == 0

    # start
    dut._log.debug("with sync and 1s")
    dut.protocol_parity_in_sync.value = 1

    await ClockCycles(dut.clk, 1)

    for i in range(0, 64):
        dut.protocol_parity_bits.value = i & 0x1F
        await ClockCycles(dut.clk, 1)
        dut.protocol_parity_in_clk.value = 1
        await ClockCycles(dut.clk, 1)
        dut.protocol_parity_in_clk.value = 0
        await ClockCycles(dut.clk, 1)
        assert dut.protocol_parity_error.value == 0

    dut._log.debug("with sync and 0s")
    dut.protocol_parity_in_data.value = 0

    await ClockCycles(dut.clk, 1)

    for i in range(0, 64):
        dut.protocol_parity_bits.value = i & 0x1F
        await ClockCycles(dut.clk, 1)
        dut.protocol_parity_in_clk.value = 1
        await ClockCycles(dut.clk, 1)
        dut.protocol_parity_in_clk.value = 0
        await ClockCycles(dut.clk, 1)
        assert dut.protocol_parity_error.value == 0

    dut._log.debug("with sync and 0s")
    dut.protocol_parity_in_data.value = 0

    await ClockCycles(dut.clk, 1)

    for j in range(0, 32):
        value = random.randint(0, pow(2, 31) - 1)
        parity = 0
        for i in range(0, 31):
            parity ^= (value >> i) & 0x1
        if parity == 1:
            value |= 1 << 31

        dut._log.debug("test value: 0x%08X parity: %d" % (value, parity))
        for i in range(0, 32):
            dut.protocol_parity_bits.value = i & 0x1F
            dut.protocol_parity_in_data.value = (value >> i) & 0x1
            await ClockCycles(dut.clk, 1)
            dut.protocol_parity_in_clk.value = 1
            await ClockCycles(dut.clk, 1)
            dut.protocol_parity_in_clk.value = 0
            await ClockCycles(dut.clk, 1)
            assert dut.protocol_parity_error.value == 0

    value = random.randint(0, pow(2, 31) - 1)
    parity = 0
    for i in range(0, 31):
        parity ^= (value >> i) & 0x1
    if parity == 0:
        value |= 1 << 31

    dut._log.debug("test wrong value: 0x%08X parity: %d" % (value, parity))
    for i in range(0, 32):
        dut.protocol_parity_bits.value = i & 0x1F
        dut.protocol_parity_in_data.value = (value >> i) & 0x1
        await ClockCycles(dut.clk, 1)
        dut.protocol_parity_in_clk.value = 1
        await ClockCycles(dut.clk, 1)
        dut.protocol_parity_in_clk.value = 0
        await ClockCycles(dut.clk, 1)
        assert dut.protocol_parity_error.value == 0

    dut.protocol_parity_bits.value = 0
    await ClockCycles(dut.clk, 1)
    dut.protocol_parity_in_clk.value = 1
    await ClockCycles(dut.clk, 1)
    dut.protocol_parity_in_clk.value = 0
    await ClockCycles(dut.clk, 1)
    assert dut.protocol_parity_error.value == 1
