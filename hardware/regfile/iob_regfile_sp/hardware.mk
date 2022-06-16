
ifeq ($(filter iob_regfile_sp, $(HW_MODULES)),)

# Add to modules list
HW_MODULES+=iob_regfile_sp

# Sources
VSRC+=$(BUILD_SRC_DIR)/iob_regfile_sp.v

# Copy sources to build directory
$(BUILD_SRC_DIR)/iob_regfile_sp.v: hardware/regfile/iob_regfile_sp/iob_regfile_sp.v
	cp $< $(BUILD_SRC_DIR)

endif
