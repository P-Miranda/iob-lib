//IO
`define INPUT(NAME, WIDTH) input [WIDTH-1:0] NAME
`define OUTPUT(NAME, WIDTH) output [WIDTH-1:0] NAME
`define INOUT(NAME, WIDTH) inout [WIDTH-1:0] NAME

//SIGNAL
`define SIGNAL(NAME, WIDTH) reg [WIDTH-1:0] NAME
`define SIGNAL_SIGNED(NAME, WIDTH) reg signed [WIDTH-1:0] NAME

//REGISTER
`define REG(CLK, OUT, IN) always @(posedge clk) OUT <= IN
`define REG_E(CLK, EN, OUT, IN) always @(posedge clk) if(EN) OUT <= IN

`define REG_R(CLK, RST, RST_VAL, OUT, IN) always @(posedge CLK) if (RST) OUT <= RST_VAL; else OUT <= IN
`define REG_RE(CLK, RST, EN, RST_VAL, OUT, IN) always @(posedge CLK) if (RST) OUT <= RST_VAL; else if (EN) OUT <= IN

`define REG_AR(CLK, RST, RST_VAL, OUT, IN) always @(posedge CLK, posedge RST) if (RST) OUT <= RST_VAL; else OUT <= IN

`define REG_ARE(CLK, RST, EN, RST_VAL, OUT, IN) always @(posedge CLK, posedge RST) if (RST) OUT <= RST_VAL; else if (EN) OUT <= IN

//SOFTWARE ACCESSIBLE REGISTERS
`define SWREG_R(NAME, WIDTH, RST_VAL) reg [WIDTH-1:0] NAME
`define SWREG_W(NAME, WIDTH, RST_VAL) reg [WIDTH-1:0] NAME
`define SWREG_RW(NAME, WIDTH, RST_VAL) reg [WIDTH-1:0] NAME

//declare component output   
`define COMPONENT_OUT(NAME, WIDTH) wire [WIDTH-1:0] NAME
   
//convert signal to a module ou component output
`define SIGNAL2OUT(OUT, IN) assign OUT = IN;
   
//COMBINATORIAL CIRCUIT
`define COMB always @* begin
`define ENDCOMB end

//COUNTERS
`define COUNTER_AR(CLK, RST, NAME) \
   `REG_AR(CLK, RST, 0, NAME, NAME+1'b1)
`define WRAPCNT_AR(CLK, RST, NAME, WRAP) \
   `REG_AR(CLK, RST, 0, NAME, NAME==WRAP? 0: NAME+1'b1)
`define WRAPCNT_ARE(CLK, RST, EN, NAME, WRAP) \
   `REG_AR(CLK, RST, 0, NAME, NAME==WRAP? 0: EN? NAME+1'b1: NAME)

// SYNCRONIZERS
`define RESET_SYNC(CLK, RST_IN, RST_OUT) \
   wire  RST_OUT; \
   reg [1:0] RST_IN_sync; \
   always @(posedge CLK, posedge RST_IN) \
   if(IN) RST_IN_sync = 2'b0; else RST_IN_sync = {RST_IN_sync[0], 1'b0}; \
   assign RST_OUT = RST_IN_sync[1];
   
`define S2F_SYNC(CLK, rst, W, IN, OUT) \
   reg [W-1:0] IN_sync [1:0]; \
   always @(posedge CLK, posedge RST) \
   if(rst) begin \
   IN_sync[0] = W'b0; \
   IN_sync[1] = W'b0; \
   end else begin \
      IN_sync[0] = IN; \
      IN_sync[1] = IN_sync[0]; \
   end


//
// COMMON TESTBENCH UTILS
//
   
//CLOCK GENERATOR
`define CLOCK(CLK, PER) reg CLK=1; always #PER CLK = ~CLK

//RESET GENERATOR
`define RESET(RST, W) reg RST=1 initial #W RST=0; 

   
   
   
   
   