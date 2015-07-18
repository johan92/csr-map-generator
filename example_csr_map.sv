

// Generated using CSR map generator 
// https://github.com/johan92/csr-map-generator

module example_csr_map(
  // Register FLOW_GEN signals
  output       [7:0]      flow_num, 
  output       [0:0]      flow_en,  
  output       [0:0]      flow_reset,
  input        [0:0]      flow_error,

  // Register STAT signals
  output       [10:0]     stat_addr,
  output       [0:0]      stat_rd_en,
  input        [9:0]      stat_counter,


  // CSR interface
  input        [0:0]      reg_clk_i,
  input        [0:0]      reg_rst_i,
  input        [31:0]     reg_wr_data_i,
  input        [0:0]      reg_wr_en_i,
  input        [0:0]      reg_rd_en_i,
  input        [7:0]      reg_addr_i,
  output       [31:0]     reg_rd_data_o
);

// ******************************************
//        Register FLOW_GEN 
// ******************************************

logic [31:0] reg_0_flow_gen_read;
logic [7:0] reg_0_flow_gen___flow_num = 8'h0;
logic [0:0] reg_0_flow_gen___flow_en = 1'h0;
logic [0:0] reg_0_flow_gen___flow_reset = 1'h0;
logic [0:0] reg_0_flow_gen___flow_error = 1'h0;


always_ff @( posedge reg_clk_i or posedge reg_rst_i )
  if( reg_rst_i )
    reg_0_flow_gen___flow_num <= 8'h0;
  else 
    if( reg_wr_en_i && ( reg_addr_i == 8'h0 ) )
      reg_0_flow_gen___flow_num <= reg_wr_data_i[7:0];

always_ff @( posedge reg_clk_i or posedge reg_rst_i )
  if( reg_rst_i )
    reg_0_flow_gen___flow_en <= 1'h0;
  else 
    if( reg_wr_en_i && ( reg_addr_i == 8'h0 ) )
      reg_0_flow_gen___flow_en <= reg_wr_data_i[15:15];

always_ff @( posedge reg_clk_i or posedge reg_rst_i )
  if( reg_rst_i )
    reg_0_flow_gen___flow_reset <= 1'h0;
  else 
    if( reg_wr_en_i && ( reg_addr_i == 8'h0 ) )
      reg_0_flow_gen___flow_reset <= reg_wr_data_i[17:17];
    else
      reg_0_flow_gen___flow_reset <= 1'h0;
  

always_ff @( posedge reg_clk_i or posedge reg_rst_i )
  if( reg_rst_i )
    reg_0_flow_gen___flow_error <= 1'h0;
  else 
    if( reg_rd_en_i && ( reg_addr_i == 8'h0 ) )
      reg_0_flow_gen___flow_error <= 1'h0;
    else
      if( flow_error == '1 )
        reg_0_flow_gen___flow_error <= '1;




// assigning to output
assign flow_num = reg_0_flow_gen___flow_num;
assign flow_en = reg_0_flow_gen___flow_en;
assign flow_reset = reg_0_flow_gen___flow_reset;

// assigning to read data

always_comb
  begin
    reg_0_flow_gen_read        = 32'h0;
    reg_0_flow_gen_read[7:0]   = reg_0_flow_gen___flow_num;
    reg_0_flow_gen_read[15:15] = reg_0_flow_gen___flow_en;
    reg_0_flow_gen_read[17:17] = reg_0_flow_gen___flow_reset;
    reg_0_flow_gen_read[21:21] = reg_0_flow_gen___flow_error;
  end

// ******************************************
//        Register STAT 
// ******************************************

logic [31:0] reg_1_stat_read;
logic [10:0] reg_1_stat___stat_addr = 11'h15;
logic [0:0] reg_1_stat___stat_rd_en = 1'h0;
logic [1:0] reg_1_stat___stat_version = 2'h3;


always_ff @( posedge reg_clk_i or posedge reg_rst_i )
  if( reg_rst_i )
    reg_1_stat___stat_addr <= 11'h15;
  else 
    if( reg_wr_en_i && ( reg_addr_i == 8'h1 ) )
      reg_1_stat___stat_addr <= reg_wr_data_i[10:0];

always_ff @( posedge reg_clk_i or posedge reg_rst_i )
  if( reg_rst_i )
    reg_1_stat___stat_rd_en <= 1'h0;
  else 
    if( reg_wr_en_i && ( reg_addr_i == 8'h1 ) )
      reg_1_stat___stat_rd_en <= reg_wr_data_i[15:15];




// assigning to output
assign stat_addr = reg_1_stat___stat_addr;
assign stat_rd_en = reg_1_stat___stat_rd_en;

// assigning to read data

always_comb
  begin
    reg_1_stat_read        = 32'h0;
    reg_1_stat_read[10:0]  = reg_1_stat___stat_addr;
    reg_1_stat_read[15:15] = reg_1_stat___stat_rd_en;
    reg_1_stat_read[25:16] = stat_counter;
    reg_1_stat_read[31:30] = reg_1_stat___stat_version;
  end


// ******* Reading stuff *******
logic [31:0] reg_rd_data;

always_ff @( posedge reg_clk_i or posedge reg_rst_i )
  if( reg_rst_i )
    reg_rd_data <= 32'h0;
  else
    if( reg_rd_en_i )
      begin

        case( reg_addr_i )
        
        8'h0:
          begin
            reg_rd_data <= reg_0_flow_gen_read;
          end
        
        8'h1:
          begin
            reg_rd_data <= reg_1_stat_read;
          end
        
        default:
          begin
            reg_rd_data <= 32'h0;
          end

        endcase

      end

assign reg_rd_data_o = reg_rd_data;

endmodule