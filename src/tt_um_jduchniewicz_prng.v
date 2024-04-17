/*
 * Copyright (c) 2024 Jakub Duchniewicz
 * SPDX-License-Identifier: Apache-2.0
 */

`define default_nettype none

module tt_um_jduchniewicz_prng (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // will go high when the design is enabled
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    // Set bidir pins all to output mode
    assign uio_oe = 8'hFF;

    // Set bidir output to always be equal to input
    assign uio_out = ui_in;

    // 8-bit LSFR with internal state of 16-bits where output is a XOR of
    // left-shifted lower 8-bits and right-shifted 8-bits basing on https:
    // //stackoverflow.com/questions/14497877/how-to-implement-a-pseudo-hardware-random-number-generator
    reg [15:0] lsfr;
    reg [7:0] out;
    assign uo_out = out;

    wire feedback = lsfr[15] ^ lsfr[14] ^ lsfr[12] ^ lsfr[3];

    always @(posedge clk or negedge rst_n) begin
        if (rst_n) begin
            lsfr <= {ui_in, ui_in};
        end else begin
            lsfr <= {lsfr[14:0], feedback}; // shift left with feedback
        end
    end

    // left shift the upper part, right shift the lower part and XOR them
    // together
    always @* begin
        out = (lsfr[15:8] << 1 | lsfr[15:8] >> 7) ^ (lsfr[7:0] >> 1 | lsfr[7:0] << 7);
    end

endmodule
