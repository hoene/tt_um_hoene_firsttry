/*
 * Copyright (c) 2025 Christian Hoene
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

// select in the data stream which data is used for the LEDs and which data is modified if forwarded
// also, enabled test mode
module tt_um_hoene_protocol_parity (
    input            in_data,      // input data
    input            in_clk,       // input clock
    input            in_sync,      // input is valid
    input            clk,          // global clock
    input      [4:0] bit_counter,
    output reg       error         // error detected
);
  reg parity;  // error detected

  always @(posedge clk) begin
    // reset
    if (!in_sync) begin
      parity <= 0;
      error  <= 0;
    end else if (in_clk) begin
      parity <= parity ^ in_data;
      if (bit_counter == 0 && parity != 0) begin
        // check parity, output error
        error <= 1;
      end
    end
  end
endmodule
