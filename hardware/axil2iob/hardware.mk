
VSRC+=axil2iob.v
axil2iob.v:$(LIB_DIR)/hardware/axil2iob/axil2iob.v
	cp $< $(BUILD_DIR)/vsrc
