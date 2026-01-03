# SPDX-FileCopyrightText: © 2025 Christian Hoene
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_led_pwm(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    for loops in (0, 1, 2, 3, 10, 25, 50, 100, 200, 400, 800, 1021, 1022, 1023):
        # Reset
        dut._log.info("Reset %d", loops)
        dut.ena.value = 1
        dut.rst_n.value = 0
        dut.led_pwm_data_red.value = loops
        dut.led_pwm_data_green.value = loops
        dut.led_pwm_data_blue.value = loops

        await ClockCycles(dut.clk, 2)

        # check output signals
        assert dut.led_pwm_out_red.value == 0
        assert dut.led_pwm_out_green.value == 0
        assert dut.led_pwm_out_blue.value == 0

        # start
        dut._log.info("Starting")
        dut.rst_n.value = 1
        await ClockCycles(dut.clk, 1)

        # check output signals
        assert dut.led_pwm_out_red.value == 0
        assert dut.led_pwm_out_green.value == 0
        assert dut.led_pwm_out_blue.value == 0

        red = 0
        green = 0
        blue = 0
        for clks in range(0, 1024):
            await ClockCycles(dut.clk, 1)
            if dut.led_pwm_out_red.value == 1:
                red += 1
            if dut.led_pwm_out_green.value == 1:
                green += 1
            if dut.led_pwm_out_blue.value == 1:
                blue += 1
        dut._log.info(
            "LED PWM Red 1: %d Green: %d Blue: %d for data %d", red, green, blue, loops
        )
        assert red == loops
        assert green == loops
        assert blue == loops

        red = 0
        green = 0
        blue = 0
        for clks in range(0, 1024):
            await ClockCycles(dut.clk, 1)
            if dut.led_pwm_out_red.value == 1:
                red += 1
            if dut.led_pwm_out_green.value == 1:
                green += 1
            if dut.led_pwm_out_blue.value == 1:
                blue += 1
        dut._log.info(
            "LED PWM Red 2: %d Green: %d Blue: %d for data %d", red, green, blue, loops
        )
        assert red == loops
        assert green == loops
        assert blue == loops
