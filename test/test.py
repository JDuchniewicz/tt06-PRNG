# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: MIT
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge

#@cocotb.test()
#async def test_prng_basic_operation(dut):
#    """Test basic PRNG operation including reset and seed change."""
#    clock = Clock(dut.clk, 10, units="us")
#    cocotb.start_soon(clock.start())
#
#    # Apply synchronous reset
#    dut.rst_n.value = 0  # Assert reset
#    await ClockCycles(dut.clk, 5)
#    dut.rst_n.value = 1  # De-assert reset
#    await ClockCycles(dut.clk, 5)
#
#    # Enable the PRNG and set the initial seed
#    dut.ena.value = 1
#    dut.ui_in.value = 20
#    await ClockCycles(dut.clk, 10)  # Wait for the PRNG to process the initial seed
#
#    first_output = int(dut.uo_out.value)
#
#    # Apply reset again before changing the seed to ensure PRNG re-initialization
#    dut.rst_n.value = 0
#    await ClockCycles(dut.clk, 5)
#    dut.rst_n.value = 1
#    await ClockCycles(dut.clk, 5)
#
#    # Change the seed
#    dut.ui_in.value = 123  # Change to a new seed
#    await ClockCycles(dut.clk, 10)  # Wait for the PRNG to process the new seed
#
#    second_output = int(dut.uo_out.value)
#
#    # Assert that the output changes after setting the new seed
#    assert first_output != second_output, f"PRNG output did not change with new seed. First output: {first_output}, Second output: {second_output}"

@cocotb.test()
async def test_prng_output_variability(dut):
    """Test that PRNG outputs vary with different seeds."""
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    await ClockCycles(dut.clk, 5)

    output_set = set()
    for seed in range(5):  # Test a small range of seeds
        # Apply reset before setting each new seed
        dut.ena.value = 0
        dut.rst_n.value = 0
        await ClockCycles(dut.clk, 5)
        dut.rst_n.value = 1
        await ClockCycles(dut.clk, 5)

        # Enable and set seed
        dut.ena.value = 1
        dut.ui_in.value = seed
        await ClockCycles(dut.clk, 10)  # Wait for LFSR to process the seed

        # Collect output
        output_set.add(int(dut.uo_out.value))

    # Check if at least some outputs were different
    assert len(output_set) > 1, "PRNG did not produce varied output across different seeds."

