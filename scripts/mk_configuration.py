#!/usr/bin/env python3
import os
import re

import iob_colors
from latex import write_table

def params_vh(params, top_module, out_dir):
    file2create = open(f"{out_dir}/{top_module}_params.vh", "w")
    file2create.write("//This file was generated by script mk_configuration.py\n")
    core_prefix = f"{top_module}_".upper()
    for parameter in params:
        if parameter['type'] in ['P','F']:
            p_name = parameter['name'].upper()
            file2create.write(f"\n\tparameter {p_name} = `{core_prefix}{p_name},")
    file2create.close()
    file2create = open(f"{out_dir}/{top_module}_params.vh", "rb+")
    file2create.seek(-1, os.SEEK_END)
    file2create.write(b'\n')
    file2create.close()

    file2create = open(f"{out_dir}/{top_module}_inst_params.vh", "w")
    file2create.write("//This file was generated by script mk_configuration.py\n")
    core_prefix = f"{top_module}_".upper()
    for parameter in params:
        if parameter['type'] in ['P','F']:
            p_name = parameter['name'].upper()
            file2create.write(f"\n\t.{p_name}(`{core_prefix}{p_name}),")
    file2create = open(f"{out_dir}/{top_module}_inst_params.vh", "rb+")
    file2create.seek(-1, os.SEEK_END)
    file2create.write(b'\n')
    file2create.close()

def conf_vh(macros, top_module, out_dir):
    file2create = open(f"{out_dir}/{top_module}_conf.vh", "w")
    file2create.write("//This file was generated by script mk_configuration.py\n\n")
    core_prefix = f"{top_module}_".upper()
    fname = f"{core_prefix}CONF"
    file2create.write(f"`ifndef VH_{fname}_VH\n")
    file2create.write(f"`define VH_{fname}_VH\n\n")
    for macro in macros:
        #Only insert macro if its is not a bool define, and if so only insert it if it is true
        if macro['val'] != 'NA':
            m_name = macro['name'].upper()
            m_default_val = macro['val']
            file2create.write(f"`define {core_prefix}{m_name} {m_default_val}\n")
    file2create.write(f"\n`endif // VH_{fname}_VH\n")

def conf_h(macros, top_module, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    file2create = open(f"{out_dir}/{top_module}_conf.h", "w")
    file2create.write("//This file was generated by script mk_configuration.py\n\n")
    core_prefix = f"{top_module}_".upper()
    fname = f"{core_prefix}CONF"
    file2create.write(f"#ifndef H_{fname}_H\n")
    file2create.write(f"#define H_{fname}_H\n\n")
    for macro in macros:
        #Only insert macro if its is not a bool define, and if so only insert it if it is true
        if macro['val'] != 'NA':
            m_name = macro['name'].upper()
            # Replace any Verilog specific syntax by equivalent C syntax
            m_default_val = re.sub("\d+'h","0x",macro['val'])
            file2create.write(f"#define {m_name} {str(m_default_val).replace('`','')}\n") #Remove Verilog macros ('`')
    file2create.write(f"\n#endif // H_{fname}_H\n")

    file2create.close()

def config_build_mk(python_module, build_dir):
    file2create = open(f"{build_dir}/config_build.mk", "w")
    file2create.write("#This file was generated by script mk_configuration.py\n\n")
    file2create.write(f"NAME={python_module.name}\n")
    file2create.write(f"VERSION={python_module.version}\n")
    file2create.write(f"BUILD_DIR_NAME={build_dir.split('/')[-1]}\n")
    file2create.write(f"FLOWS={python_module.flows}\n\n")

    file2create.close()


# This function append a list of flows to the existing config_build.mk file
# Usually called by submodules that have flows not contained in the top core/system
#flows_list:  list of flows of module
#flows_filter: list of flows that should be appended if they exist in flows_list
#build_dir: build directory containing config_build.mk
def append_flows_config_build_mk(flows_list, flows_filter, build_dir):
    flows2append=""
    for flow in flows_filter:
        if flow in flows_list: flows2append += f"{flow} "

    if not flows2append: return
    file = open(f"{build_dir}/config_build.mk", "a")
    file.write(f"FLOWS+={flows2append}\n\n")
    file.close()

# Generate TeX table of confs
def generate_confs_tex(confs, out_dir):
    tex_table = []
    for conf in confs:
        tex_table.append([conf['name'].replace('_','\_'), conf['type'], conf['min'], conf['val'].replace('_','\_'), conf['max'], conf['descr'].replace('_','\_')])

    write_table(f"{out_dir}/confs",tex_table)


# Create build-time board/simulation configuration in config_build.mk
#top: Name of this core/system
#flows_list: list of flows of this core/system
#build_dir: path to build directory
def config_for_board(top, flows_list, build_dir):
    available_configs = {
        'CYCLONEV-GT-DK':{'BAUD':'115200', 'FREQ':'50000000', 'MEM_NO_READ_ON_WRITE':'1', 'DDR_DATA_W':'32', 'DDR_ADDR_W':'30'}, 
        'AES-KU040-DB-G':{'BAUD':'115200', 'FREQ':'100000000', 'DDR_DATA_W':'32', 'DDR_ADDR_W':'30'},
        'DE10-LITE':{'BAUD':'115200', 'FREQ':'50000000'},
        'BASYS3':{'BAUD':'115200', 'FREQ':'100000000'},
        'SIMULATION':{'BAUD':'3000000', 'FREQ':'100000000', 'DDR_DATA_W':'32', 'DDR_ADDR_W':'24'},
        }

    # Set config based on value of BOARD variable
    file = open(f"{build_dir}/config_build.mk", "a")

    file.write(f"\n#################### Script to generate build-time configuration files ####################\n")

    # Make script to select what configuration to use
    file.write("ifneq ($(GEN_CONFIG),)\n")
    file.write("ifneq ($(BOARD),)\n")
    file.write("CONFIG:=$(BOARD)\n")
    file.write("else\n")
    file.write("CONFIG:=SIMULATION\n")
    file.write("endif\n")

    # Make script to write 'build_configuration.vh' and 'build_configuration.h' files at build time
    for name, config in available_configs.items():
        file.write(f"ifeq ($(CONFIG),{name})\n")
        # Create 'build_configuration.vh'
        file.write(f"$(shell rm -f ../src/build_configuration.vh)\n")
        file.write(f"$(shell echo '//This file was generated by config_build.mk' >> ../src/build_configuration.vh)\n")
        for key, value in config.items():
            file.write(f"$(shell echo '`define {key} {value}' >> ../src/build_configuration.vh)\n")

        # Create 'build_configuration.h'
        if 'emb' in flows_list:
            file.write(f"$(shell rm -f ../../software/esrc/build_configuration.h)\n")
            file.write(f"$(shell echo '//This file was generated by config_build.mk' >> ../../software/esrc/build_configuration.h)\n")
            for key, value in config.items():
                file.write(f"$(shell echo '#define {key} {value}' >> ../../software/esrc/build_configuration.h)\n")

        file.write("endif\n")

    file.write("endif\n")
    file.write(f"################ End of script to generate build-time configuration files #################\n\n")
    file.close()

# Select if a define from the confs dictionary is set or not
# define_name: name of the macro in confs (its called define because it is unvalued, it is either set or unset)
# should_set: Select if define should be set or not
def update_define(confs, define_name, should_set):
    for macro in confs:
        if macro['name']==define_name:
            # Found macro. Unset it if not 'should_set'
            if should_set: 
                macro['val'] = '1'
            else:
                macro['val'] = 'NA'
            break
    else:
        # Did not find define. Set it if should_set.
        if should_set: 
            confs.append({'name':define_name,'type':'M', 'val':'1', 'min':'0', 'max':'1', 'descr':"Define"})
