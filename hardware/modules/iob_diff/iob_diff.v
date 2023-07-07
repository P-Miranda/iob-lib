`timescale 1ns / 1ps

module iob_diff #(
   parameter DATA_W  = 32,
   parameter RST_VAL = 0
) (
   `include "iob_clkenrst_port.vs"

   input rst_i,

   input  [DATA_W-1:0] data_i,
   output [DATA_W-1:0] data_o
);

   wire [DATA_W-1:0] data_i_reg;
   iob_reg_r #(DATA_W, RST_VAL) reg0 (
      `include "iob_clkenrst_portmap.vs"

      .rst_i(rst_i),

      .data_i(data_i),
      .data_o(data_i_reg)
   );

   assign data_o = data_i - data_i_reg;

endmodule
