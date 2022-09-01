# (c) 2022-Present IObundle, Lda, all rights reserved
#
# This makefile is used to setup a build directory for an IP core or to
# simulate the modules in this repository
#
# To create a build directory from any directory:
# > make -C /path/to/iob-lib setup
#
# To simulate a module in this:
# > make -C /path/to/iob-lib sim MODULE=<some module in the hardware directory>
#


SHELL=/bin/bash
export

#build here
LIB_DIR:=.
BUILD_VSRC_DIR:=.

# Default module
MODULE ?= iob_ram_2p
MODULE_DIR ?= $(shell find hardware -name $(MODULE))
ifneq ($(MODULE_DIR),)
include $(MODULE_DIR)/hardware.mk
else
$(info No such module $(MODULE))
endif

# Testbench
TB=$(wildcard $(MODULE_DIR)/*_tb.v)

# Defines
DEFINE=-DADDR_W=10 -DDATA_W=32
ifeq ($(VCD),1)
DEFINE+= -DVCD
endif

# Includes
INCLUDE=-Ibuild/hw/vsrc

# asymmetric memory present
IS_ASYM=$(shell echo $(SRC) | grep asym)

AXI_GEN:=./software/python/axi_gen.py

#
# Simulate with Icarus Verilog
#
VLOG=iverilog -W all -g2005-sv $(INCLUDE) $(DEFINE)

sim: $(SRC) $(TB)
	@echo "Simulating module $(MODULE)"
ifeq ($(IS_ASYM),)
	$(VLOG) $(SRC) $(TB)
	@./a.out $(TEST_LOG)
else
	$(VLOG) -DW_DATA_W=32 -DR_DATA_W=8 $(SRC) $(TB)
	@./a.out $(TEST_LOG)
	$(VLOG) -DW_DATA_W=8 -DR_DATA_W=32 $(SRC) $(TB)
	@./a.out $(TEST_LOG)
	$(VLOG) -DW_DATA_W=8 -DR_DATA_W=8 $(SRC) $(TB)
	@./a.out $(TEST_LOG)
endif
ifeq ($(VCD),1)
	@if [ ! `pgrep gtkwave` ]; then gtkwave uut.vcd; fi &
endif

clean:
	@rm -f *.v *.vh *.c *.h *.tex
	@rm -f *~ \#*\# a.out *.vcd *.pyc *.log

debug:

.PHONY: sim clean debug
