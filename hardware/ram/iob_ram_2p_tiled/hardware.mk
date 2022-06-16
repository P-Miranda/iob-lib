ifeq ($(filter iob_ram_2p_tiled, $(HW_MODULES)),)

# Add to modules list
HW_MODULES+=iob_ram_2p_tiled

# Submodules
include $(LIB_DIR)/hardware/ram/iob_ram_2p/hardware.mk

# Sources
VSRC+=$(BUILD_SRC_DIR)/iob_ram_2p_tiled.v

# Copy the sources to the build directory
$(BUILD_SRC_DIR)/iob_ram_2p_tiled.v:$(LIB_DIR)/hardware/ram/iob_ram_2p_tiled/iob_ram_2p_tiled.v
	cp $< $(BUILD_SRC_DIR)

endif
