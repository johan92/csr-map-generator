#!/usr/bin/env python

from jinja2 import Template

class Reg( ):

  def __init__( self, num, name ):
    self.num          = '{:X}'.format( num )
    self.name         = name
    self.name_lowcase = self.name.lower()
    self.bits         = []
  
  def add_bits( self, reg_bits ):
    self.bits.append( reg_bits )

class RegBits( ):

  def __init__( self, bit_msb, bit_lsb, name, mode = "RW", init_value = 0 ):
    self.bit_msb      = bit_msb
    self.bit_lsb      = bit_lsb
    self.width        = bit_msb - bit_lsb + 1
    self.name         = name
    self.name_lowcase = self.name.lower()
    self.mode         = mode
    self.init_value   = '{:X}'.format( init_value )
    
    # bit modes:
    # RO       - read only
    # RO_CONST - read only, constant value 
    # RO_LH    - read only, latch high
    # RO_LL    - read only, latch low
    # RW       - read and write
    # RW_SC    - read and write, self clear
    assert self.mode in ["RO", "RO_CONST", "RO_LH", "RO_LL", "RW", "RW_SC" ], "Unknown bit mode" 
    
    if self.mode in ["RO_LH", "RO_LL", "RW_SC"]:
      assert self.width == 1, "Wrong width for this bit mod" 

    self.port_signal_input  = self.mode in ["RO", "RO_LH", "RO_LL"]
    self.port_signal_output = self.mode in ["RW", "RW_SC"]
    self.need_port_signal   = self.port_signal_input or self.port_signal_output

csr_map_template = Template(u"""
{%- macro reg_name( r ) -%}
reg_{{r.num}}_{{r.name_lowcase}}
{%- endmacro %}

{%- macro reg_name_bits( r, b ) -%}
reg_{{r.num}}_{{r.name_lowcase}}___{{b.name_lowcase}}
{%- endmacro %}

{%- macro bit_init_value( b ) -%}
{{b.width}}'h{{b.init_value}}
{%- endmacro %}

{%- macro signal( width ) -%}
[{{width-1}}:0]
{%- endmacro %}

{%- macro print_port_signal( dir, width, name, eol="," ) -%}
{{ "  %-12s %-10s %-10s" | format( dir,  signal( width ),  name+eol ) }}
{%- endmacro %}

// Generated using CSR map generator 
// https://github.com/johan92/csr-map-generator

module {{module_name}}(

{%- for p in data %}
  // Register {{p.name}} signals

{%- for b in p.bits %}
  {%- if b.port_signal_input %}
{{print_port_signal( "input", b.width, b.name_lowcase )}}
  {%- elif b.port_signal_output %}
{{print_port_signal( "output", b.width, b.name_lowcase )}}
  {%- endif %}
{%- endfor %}
{% endfor %}

  // CSR interface
{{print_port_signal( "input",  1,       "reg_clk_i"          ) }}
{{print_port_signal( "input",  1,       "reg_rst_i"          ) }}
{{print_port_signal( "input",  reg_d_w, "reg_wr_data_i"      ) }}
{{print_port_signal( "input",  1,       "reg_wr_en_i"        ) }}
{{print_port_signal( "input",  1,       "reg_rd_en_i"        ) }}
{{print_port_signal( "input",  reg_a_w, "reg_addr_i"         ) }}
{{print_port_signal( "output", reg_d_w, "reg_rd_data_o", ""  ) }}
);


{%- for p in data %}

// ******************************************
//        Register {{p.name}} 
// ******************************************

logic [{{reg_d_w-1}}:0] {{reg_name( p )}}_read;

{%- for b in p.bits %}
{%- if b.mode != "RO" %}
logic [{{b.width-1}}:0] {{reg_name_bits( p, b )}} = {{bit_init_value( b )}};
{%- endif %}      
{%- endfor %}

{% for b in p.bits %}
{%- if b.port_signal_output %}
always_ff @( posedge reg_clk_i or posedge reg_rst_i )
  if( reg_rst_i )
    {{reg_name_bits( p, b )}} <= {{bit_init_value( b )}};
  else 
    if( reg_wr_en_i && ( reg_addr_i == {{reg_a_w}}'h{{p.num}} ) )
      {{reg_name_bits( p, b )}} <= reg_wr_data_i[{{b.bit_msb}}:{{b.bit_lsb}}];
  {%-if b.mode == "RW_SC" %}
    else
      {{reg_name_bits( p, b )}} <= {{bit_init_value( b )}};
  {% endif %}
{%- endif %}

{%- if b.mode == "RO_LH" or b.mode == "RO_LL" %}
always_ff @( posedge reg_clk_i or posedge reg_rst_i )
  if( reg_rst_i )
    {{reg_name_bits( p, b )}} <= {{bit_init_value( b )}};
  else 
    if( reg_rd_en_i && ( reg_addr_i == {{reg_a_w}}'h{{p.num}} ) )
      {{reg_name_bits( p, b )}} <= {{bit_init_value( b )}};
    else
      {%- if b.mode == "RO_LL" %}
      if( {{b.name_lowcase}} == '0 )
        {{reg_name_bits( p, b )}} <= '1;
      {%- elif b.mode == "RO_LH" %}
      if( {{b.name_lowcase}} == '1 )
        {{reg_name_bits( p, b )}} <= '1;
      {%- endif %}

{% endif %}
{% endfor %}

// assigning to output
{%- for b in p.bits %}
{%- if b.port_signal_output %}
assign {{b.name_lowcase}} = {{reg_name_bits( p, b )}};
{%- endif %}
{%- endfor %}

// assigning to read data
{%- macro print_in_always_comb( r, b, _right_value ) -%}
{%- if b == "" -%}
{{ "  %s%-7s = %s;" | format( reg_name( r ) + "_read",  "",  _right_value ) }}
{%- else -%}
{{ "  %s%-7s = %s;" | format( reg_name( r ) + "_read", "["+b.bit_msb|string+":"+b.bit_lsb|string+"]" ,  _right_value ) }}
{%- endif %}
{%- endmacro %}

always_comb
  begin
  {{print_in_always_comb( p, "", reg_d_w|string+"'h0" ) }}

{%- for b in p.bits %}
  {%- if b.mode == "RO" %}
  {{print_in_always_comb( p, b, b.name_lowcase )}}
  {%- else %}
  {{print_in_always_comb( p, b, reg_name_bits( p, b ) )}}
  {%- endif %}
{%- endfor %}
  end

{%- endfor %}


// ******* Reading stuff *******
logic [{{reg_d_w-1}}:0] reg_rd_data;

always_ff @( posedge reg_clk_i or posedge reg_rst_i )
  if( reg_rst_i )
    reg_rd_data <= {{reg_d_w}}'h0;
  else
    if( reg_rd_en_i )
      begin

        case( reg_addr_i )
        {% for p in data %}
        {{reg_a_w}}'h{{p.num}}:
          begin
            reg_rd_data <= {{reg_name( p )}}_read;
          end
        {% endfor %}
        default:
          begin
            reg_rd_data <= {{reg_d_w}}'h0;
          end

        endcase

      end

assign reg_rd_data_o = reg_rd_data;

endmodule
""")

if __name__ == "__main__":
  
  MODULE_NAME = "example_csr_map"

  r0 = Reg( 0x0, "FLOW_GEN")
  r0.add_bits( RegBits( 7, 0,   "flow_num", "RW"      ) )
  r0.add_bits( RegBits( 15, 15, "flow_en" , "RW"      ) )
  r0.add_bits( RegBits( 17, 17, "flow_reset", "RW_SC" ) )
  r0.add_bits( RegBits( 21, 21, "flow_error", "RO_LH" ) )

  r1 = Reg( 0x1, "STAT" )
  r1.add_bits( RegBits( 10, 0,   "stat_addr",    "RW",       0x15  ) )
  r1.add_bits( RegBits( 15, 15,  "stat_rd_en",   "RW"              ) )
  r1.add_bits( RegBits( 25, 16,  "stat_counter", "RO"              ) )
  r1.add_bits( RegBits( 31, 30,  "stat_version", "RO_CONST", 0x3   ) )

  reg_l = [r0, r1]

  res = csr_map_template.render(
      module_name = MODULE_NAME,
      reg_d_w     = 32,
      reg_a_w     = 8,
      data        = reg_l 
  )

  print res

  # saving to systemverilog file
  try:
    out_file = open( MODULE_NAME+".sv", 'w')
  except Exception as ex:
    print "Error opening \"%s\": %s" %( out_name, ex.strerror )
    exit(1)

  out_file.write( res )

