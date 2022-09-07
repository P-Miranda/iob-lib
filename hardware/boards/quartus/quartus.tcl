#extract cli args
set NAME [lindex $argv 0]
set TOP [lindex $argv 1]
set VSRC [lindex $argv 2]
set QIP [lindex $argv 3]

set project_name $NAME

project_new $TOP -overwrite


#------ Create or open project ------#
if [project_exists $project_name] {

    #------ Project already exists -- open project -------#
    project_open $project_name -force
} else {

    #------ Project does not exist -- create new project ------#
    project_new $project_name
}

set_global_assignment -name TOP_LEVEL_ENTITY $TOP

#device data
source device.tcl

#user io data 
source io.tcl

set_global_assignment -name PROJECT_OUTPUT_DIRECTORY output_files
set_global_assignment -name VERILOG_INPUT_VERSION SYSTEMVERILOG_2005

#verilog heders search path
set_global_assignment -name SEARCH_PATH ../vsrc

#quartus IPs
foreach file [split $QIP \ ] {
    if {$file != ""} {
        set_global_assignment -name QIP_FILE $file
    }
}


#verilog sources
foreach file [split $VSRC \ ] {
    if {$file != ""} {
        set_global_assignment -name VERILOG_FILE $file
    }
}


if {$TARGET == "IP"} {
set_global_assignment -name PARTITION_NETLIST_TYPE SOURCE -section_id Top
set_global_assignment -name PARTITION_FITTER_PRESERVATION_LEVEL PLACEMENT_AND_ROUTING -section_id Top
set_global_assignment -name PARTITION_COLOR 16764057 -section_id Top


set_global_assignment -name PARTITION_NETLIST_TYPE POST_SYNTH -section_id $TOP:$TOP

set_global_assignment -name PARTITION_FITTER_PRESERVATION_LEVEL PLACEMENT_AND_ROUTING -section_id $TOP:$TOP

set_global_assignment -name PARTITION_COLOR 39423 -section_id $TOP:$TOP

set_instance_assignment -name PARTITION_HIERARCHY root_partition -to | -section_id Top
}

set_global_assignment -name LAST_QUARTUS_VERSION "18.0.0 Standard Edition"
set_global_assignment -name SDC_FILE ../fpga/$NAME.sdc
set_global_assignment -name MIN_CORE_JUNCTION_TEMP 0
set_global_assignment -name MAX_CORE_JUNCTION_TEMP 85
set_global_assignment -name POWER_PRESET_COOLING_SOLUTION "23 MM HEAT SINK WITH 200 LFPM AIRFLOW"
set_global_assignment -name POWER_BOARD_THERMAL_MODEL "NONE (CONSERVATIVE)"

#------ Manually recompile and perform timing analysis again using qexec ------#

# Write these assignments to the
# Quartus Prime Settings File (.qsf) so that
# the Quartus Prime command-line executables
# can use these assignments during compilation

# random seed for fitting
set_global_assignment -name SEED 23

export_assignments

if [catch {qexec "[file join $::quartus(binpath) quartus_map] $project_name"} result] {
    qexit -error
}

if {file exists "postmap.tcl"} {
 source "postmap.tcl"
}

if [catch {qexec "[file join $::quartus(binpath) quartus_fit] $project_name"} result] {
    qexit -error
}

if [catch {qexec "[file join $::quartus(binpath) quartus_sta] $project_name"} result] {
    qexit -error
}


if {$TARGET == "IP"} {
    if [catch {qexec "[file join $::quartus(binpath) quartus_cdb] $project_name --incremental_compilation_export=$NAME.qxp --incremental_compilation_export_post_synth=on"} result] {
        qexit -error
    }
    else {
if [catch {qexec "[file join $::quartus(binpath) quartus_asm] $project_name"} result] {
    qexit -error
    }

project_close