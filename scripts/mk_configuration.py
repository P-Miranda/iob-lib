#!/usr/bin/env python3
import os

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
        if macro['type'] != 'D':
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
        if macro['type'] != 'D':
            m_name = macro['name'].upper()
            m_default_val = macro['val']
            file2create.write(f"#define {m_name} {str(m_default_val).replace('`','')}\n") #Remove Verilog macros ('`')
    file2create.write(f"\n#endif // H_{fname}_H\n")

def config_build_mk(defines, meta_data, build_dir):
    file2create = open(f"{build_dir}/config_build.mk", "w")
    file2create.write("#This file was generated by script mk_configuration.py\n\n")
    file2create.write(f"NAME={meta_data['name']}\n")
    file2create.write(f"VERSION={meta_data['version']}\n")
    file2create.write(f"BUILD_DIR_NAME={build_dir.split('/')[-1]}\n")
    file2create.write(f"FLOWS={meta_data['flows']}\n\n")
    file2create.write(f"DEFINES=\n")

    for macro in defines:
        if macro['type'] == 'D':
            d_name = macro['name'].upper()
            d_val = macro['val']
            file2create.write(f"{d_name} ?= {d_val}\n")
            file2create.write(f"ifeq ($({d_name}),1)\n")
            file2create.write(f"DEFINES+= -D{d_name}\n")
            file2create.write(f"endif\n\n")

# Generate TeX table of confs
def generate_confs_tex(confs, out_dir):
    tex_table = []
    for conf in confs:
        tex_table.append([conf['name'].replace('_','\_'), conf['type'], conf['min'], conf['val'].replace('_','\_'), conf['max'], conf['descr'].replace('_','\_')])

    write_table(f"{out_dir}/confs",tex_table)
