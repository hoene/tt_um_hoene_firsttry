/*
 * Copyright (c) 2026 Christian Hoene
 * SPDX-License-Identifier: Apache-2.0
 */


`default_nettype none

// a 3 bit low pass filter

module tt_um_hoene_led_pwm (
    input      [9:0] data_red,    // red values 10 bit
    input      [9:0] data_green,  // green values 10 bit 
    input      [9:0] data_blue,   // blue values 10 bit 
    input            rst_n,       // device reset
    input            clk,         // global clock
    output reg       out_red,     // output signal
    output reg       out_green,   // green channel enable
    output reg       out_blue     // blue channel enable
);
  reg [9:0] counter;
  reg next_green;

  always @(posedge clk) begin
    if (!rst_n) begin
      counter <= 0;
      out_red <= 0;
      out_green <= 0;
      out_blue <= 0;
      next_green <= 0;
    end else begin
      counter <= counter + 1;

      if (counter == data_red) out_red <= 1'b0;
      else if (counter == 0) out_red <= 1'b1;

      if (counter == 10'h3ff) out_blue <= 1'b0;
      else if (counter == ~data_blue) out_blue <= 1'b1;

      if (counter == {1'b0, ~data_green[9:1]}) begin
        if (data_green[0] == 1) out_green <= 1'b1;
        else next_green <= 1'b1;
      end else if (counter == {1'b1, data_green[9:1]}) begin
        out_green  <= 1'b0;
        next_green <= 1'b0;
      end else if (next_green == 1) out_green <= 1'b1;
    end
  end

endmodule
