/*
 * Copyright (c) 2025 Christian Hoene
 * SPDX-License-Identifier: Apache-2.0
 */


`default_nettype none

// a 3 bit low pass filter

module tt_um_hoene_protocol_insync (
    input in_data,   // input data
    input in_clk,    // input clock
    input in_error,  // input error
    input rst_n,     // device reset
    input clk,       // global clock

    output reg insync,    // bitstream is insync
    output reg out_data,  // the data if within a frame
    output reg out_clk    // the clock if within a frame
);
  reg last_in;

  always @(posedge clk) begin


    if (!rst_n || in_error) begin
      insync   <= 0;
      last_in  <= 0;
      out_data <= 0;
      out_clk  <= 0;
    end else if (in_clk) begin
      last_in <= in_data;

      // check for init state
      if (!insync) begin  // the first byte is 10101011b
        if (last_in == 1 && in_data == 1) begin
          insync   <= 1;
          out_data <= in_data;
          out_clk  <= in_clk;
        end else begin
          out_data <= 0;
          out_clk  <= 0;
        end
      end else begin
        out_data <= in_data;
        out_clk  <= in_clk;
      end
    end else begin
      out_data <= 0;
      out_clk  <= 0;
    end
  end
endmodule
