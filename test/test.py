# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge

@cocotb.test()
async def test_prng_basic_operation(dut):
    """Test basic PRNG operation including reset and seed change."""
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset the PRNG
    dut.ena.value = 0
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 0
    dut.ena.value = 1
    await ClockCycles(dut.clk, 5)

    # Set a seed and check for change in output
    dut.ui_in.value = 20
    await ClockCycles(dut.clk, 5)
    first_output = int(dut.uo_out.value)
    dut.ui_in.value = 123  # Example seed
    await ClockCycles(dut.clk, 5)
    second_output = int(dut.uo_out.value)

    # Assert that the output changes after setting the seed
    assert first_output != second_output, "PRNG output did not change with new seed."

@cocotb.test()
async def test_prng_output_variability(dut):
    """Test that PRNG outputs vary with different seeds."""
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    await ClockCycles(dut.clk, 5)

    dut.ena.value = 0
    output_set = set()
    for seed in range(5):  # Test a small range of seeds
        dut.rst_n.value = 1
        await ClockCycles(dut.clk, 5)
        dut.rst_n.value = 0
        dut.ena.value = 1
        await ClockCycles(dut.clk, 5)

        dut.ui_in.value = seed
        await ClockCycles(dut.clk, 10)  # Wait a bit for PRNG to process

        # Collect output
        output_set.add(int(dut.uo_out.value))

    # Check if at least some outputs were different
    assert len(output_set) > 1, "PRNG did not produce varied output across different seeds."

