/*
 * Copyright (c) 2025 Christian Hoene
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_hoene_mux (
    input  wire in0,        // first input 
    input  wire in1,        // second input
    input  wire rst_n,      // device reset
    input  wire clk,        // global clock
    input  wire testmode,   // high if the other input shall be chosen regardless
    output wire out,            // output signal
    output wire in0selected,  // Dedicated outputs
);

reg [5:0] counter;
reg last_in0;

// high if in0 is selected, otherwise in1 is selected
reg in0selected;
assign in0selected <= in0selected


always @(posedge clk) begin
    if (!rst_n) begin
        in0selected <= 1'b0;
        last_in0 = 0;
        counter = 0;
    end else begin   
        if (last_in0 == 0 && in0 == 1 && counter != 63) begin
            counter <= counter + 1;
        end
        last_in0 = in0;
        if (counter == 63 ^ testmode) begin
            in0selected <= 1;
            out <= in0;
        end else begin
            in0selected <= 0;
            out <= in1;
        end
    end
end