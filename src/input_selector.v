/*
 * Copyright (c) 2025 Christian Hoene
 * SPDX-License-Identifier: Apache-2.0
 */


`default_nettype none

// selects input 0 or input 1 and forwards it to out depening on two conditions 
// 1) If input 0 receives bits, then input 0 is selected after 64 cycles, otherwise input 1 is taken.
// 2) Overwriting the decision of 1), if the test mode is selected, then the decision of 1) is swapped.

module tt_um_hoene_input_selector (
    input      in0,         // first input
    input      in1,         // second input
    input      rst_n,       // device reset
    input      clk,         // global clock
    input      testmode,    // high if the other input shall be chosen regardless
    output reg out,         // output signal
    output reg in0selected  //  high if in0 is selected, otherwise in1 is selected
);

  reg [5:0] counter0;
  reg [7:0] counter1;
  reg last_in0;
  reg last_in1;

  always @(posedge clk) begin
    if (!rst_n) begin
      in0selected <= 0;
      last_in0 <= 0;
      counter0 <= 0;
      last_in1 <= 0;
      counter1 <= 0;
      out <= 0;
    end else begin

      // count inputs from in1
      last_in1 <= in1;
      if (last_in1 == 0 && in1 == 1 && counter1 != 255) begin
        counter1 <= counter1 + 1;
      end

      // count inputs from in0
      last_in0 <= in0;
      if (last_in0 == 0 && in0 == 1 && counter0 != 63 && counter1 != 255) begin
        counter0 <= counter0 + 1;
      end

      // decide which input to select
      if ((counter0 == 63 & !testmode) || (counter0 != 63 & testmode)) begin
        in0selected <= 1;
        out <= in0;
      end else begin
        in0selected <= 0;
        out <= in1;
      end
    end
  end

endmodule
