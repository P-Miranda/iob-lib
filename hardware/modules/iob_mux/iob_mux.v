`timescale 1ns / 1ps


module iob_mux
  #(
    parameter DATA_W = 21,
    parameter N = 21
  )
  (
    input [($clog2(N)+($clog2(N)==0))-1:0] sel_i,
    input [(N*DATA_W)-1:0] data_i,
    output reg [DATA_W-1:0] data_o
  );

  integer i;
  always @* begin
    data_o = {DATA_W{1'b0}};
    for (i=0; i<N; i=i+1) begin : gen_mux
      if (i==sel_i)
        data_o = data_i[i*DATA_W+:DATA_W];
    end
  end

endmodule
